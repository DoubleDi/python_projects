
import argparse
import aiomysql
import asyncio
import itertools
import logging
import os
import yaml

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

DEFAULT_TIMEOUT = 10
DEFAULT_ROWS_PER_ITER = 1000

class Job(object):

    def __init__(self, from_table, to_table, timeout=DEFAULT_TIMEOUT, rows_per_iter=DEFAULT_ROWS_PER_ITER):
        self.from_table = Table(from_table)
        self.to_table = Table(to_table)
        self.timeout = timeout
        self.rows_per_iter = rows_per_iter

        self.moved = 0

    async def run(self):
        await self.start()

        logging.info("Start moving data from {} to {}".format(self.from_table.full_name(), self.to_table.full_name()))
        await self.compare_columns()

        while True:
            await self.begin_tx()
            try:
                moved = await self.move_data()
                await self.compare_data()
                await self.delete_data()
            except StopAsyncIteration as e:
                logging.info("Finished moving from {} to {}. Moved {} rows".format(
                    self.from_table.full_name(), self.to_table.full_name(), self.moved))
                await self.rollback_tx()
                break
            except ValueError as e:
                logging.error("Got error: {}. Rollback".format(str(e)))
                await self.rollback_tx()
                await asyncio.sleep(self.timeout)
                continue
            else:
                await self.commit_tx()
                await asyncio.sleep(self.timeout)
                self.moved += moved

        await self.finish()

    async def compare_columns(self):
        from_columns = set([ c[0] for c in await self.from_table.get_columns() ])
        to_columns = set([ c[0] for c in await self.to_table.get_columns() ])
        self.columns = list(from_columns & to_columns)
        if len(self.columns) == 0:
            raise ValueError("Columns from {} and {} don't match".format(
                self.from_table.full_name(), self.to_table.full_name()))
        logging.info('Columns, that will be moved from {} to {} are "{}"'.format(
            self.from_table.full_name(), self.to_table.full_name(), ",".join(self.columns)))

    async def move_data(self):
        data = await self.from_table.get_data(self.columns, self.rows_per_iter)
        if len(data) == 0:
            raise StopAsyncIteration("No more data")
        await self.to_table.insert_data(self.columns, data)
        return len(data)

    async def compare_data(self):
        data = await self.from_table.get_data(self.columns, self.rows_per_iter)
        await self.to_table.check_data(self.columns, data)

    async def delete_data(self):
        await self.from_table.delete_data(self.rows_per_iter)

    async def start(self):
        await self.from_table.connect()
        await self.to_table.connect()

    async def begin_tx(self):
        await self.from_table.begin_tx()
        await self.to_table.begin_tx()

    async def commit_tx(self):
        await self.from_table.commit_tx()
        await self.to_table.commit_tx()

    async def rollback_tx(self):
        await self.from_table.rollback_tx()
        await self.to_table.rollback_tx()

    async def finish(self):
        await self.from_table.close()
        await self.to_table.close()
        logger.info('Finished data migration from {} to {}'.format(
            self.from_table.full_name(), self.to_table.full_name()))

class Table(object):
    def __init__(self, config):
        self.db = config['database']
        self.table = config['table']
        self.host = config['host']
        self.password = config['password']
        self.user = config['user']
        self.port = config.get('port', 3306)

    async def connect(self):
        self.conn = await aiomysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            loop=asyncio.get_event_loop(),
        )
        self.cursor = await self.conn.cursor()
        logging.info("Connected to {}".format(self.db))

    def full_name(self):
        return "{}.{}".format(self.db, self.table)

    async def get_columns(self):
        query = "SHOW FULL COLUMNS FROM {}".format(self.full_name())
        logger.debug(query)
        await self.cursor.execute(query)
        return await self.cursor.fetchall()

    async def get_data(self, columns, limit):
        query = "SELECT {} FROM {} LIMIT %s".format(", ".join(columns), self.full_name())
        logger.debug(query, limit)
        await self.cursor.execute(query, limit)
        return await self.cursor.fetchall()

    async def delete_data(self, limit):
        query = "DELETE FROM {} LIMIT %s".format(self.full_name())
        logger.debug(query, limit)
        await self.cursor.execute(query, limit)

    async def insert_data(self, columns, data):
        values = ["("+", ".join([ "%s" ] * len(columns)) +")"] * len(data)
        flat_data = list(itertools.chain(*data))
        query = "INSERT IGNORE INTO {} ({}) VALUES {}".format(self.full_name(), ", ".join(columns), ", ".join(values))
        logger.debug(query, *flat_data)
        await self.cursor.execute(query, flat_data)

    async def check_data(self, columns, data):
        query = "SELECT count(*) FROM {} where ".format(self.full_name())
        wheres = []
        rows = []
        for row in data:
            where = []
            for i in range(len(columns)):
                if row[i] is None:
                    where.append(columns[i] + " is NULL")
                else:
                    where.append(columns[i] + " = %s")
                    rows.append(row[i])
            wheres.append("(" + " AND ".join(where) + ")")
        query += " OR ".join(wheres)
        logger.debug(query, *rows)
        await self.cursor.execute(query, rows)
        count = await self.cursor.fetchone()
        if count[0] != len(data):
            logger.error("Data is not moved completely. Moved {} out of {}".format(count[0], len(data)))
            raise ValueError("Data is not moved completely")

    async def begin_tx(self):
        await self.conn.begin()

    async def commit_tx(self):
        await self.conn.commit()

    async def rollback_tx(self):
        await self.conn.rollback()

    async def close(self):
        await self.cursor.close()
        self.conn.close()


def init_jobs(config_path):
    jobs = []
    with open(config_path, 'r') as config:
        for job in yaml.load(config.read(), Loader=yaml.SafeLoader):
            jobs.append(
                Job(
                    job['job']['from'],
                    job['job']['to'],
                    job['job'].get('timeout'),
                    job['job'].get('rows_per_iter')
                )
            )

    return jobs


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config', default=None)
    args = parser.parse_args()

    jobs = init_jobs(args.config)
    states = await asyncio.gather(
        *[job.run() for job in jobs],
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

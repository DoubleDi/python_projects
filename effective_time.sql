-- init data
begin;

CREATE TABLE posts_stats (
    dttm TIMESTAMP,
    post_id INTEGER,
    views INTEGER,
    likes INTEGER,
    shares INTEGER,
    PRIMARY KEY (dttm, post_id)
);

INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:00:00', 1, 100, 10, 1);
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:01:00', 1, 100, 10, 1);
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:02:00', 1, 100, 11, 1);
-- Data for post 1 at 00:03:00 is lost
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:04:00', 1, 100, 11, 1);
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:00:00', 2, 200, 20, 2);
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:01:00', 2, 210, 21, 2);
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:02:00', 2, 220, 22, 3);
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:03:00', 2, 220, 21, 3);
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:04:00', 2, 250, 21, 3);
-- Post 3 was published at 00:02:00
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:02:00', 3, 0, 0, 0);
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:03:00', 3, 50, 1, 1);
INSERT INTO posts_stats VALUES (TIMESTAMP '2019-01-01 00:04:00', 3, 70, 5, 2);

commit;



-- to SCD type 2
begin;

create table if not exists posts_stats_new (
    post_id INTEGER,
    views INTEGER,
    likes INTEGER,
    shares INTEGER,
    effective_from TIMESTAMP,
    effective_to TIMESTAMP,
    PRIMARY KEY (post_id, effective_from, effective_to)
);

-- old
/*
insert into posts_stats_new (post_id, views, likes, shares, effective_from, effective_to) (
    with e_times as (
        select min(dttm) as effective_from, max(dttm) as e_to, post_id, views, likes, shares
        from posts_stats
        group by post_id, views, likes, shares
    )
    select t1.post_id, t1.views, t1.likes, t1.shares, t1.effective_from, min(t2.effective_from) as effective_to
    from e_times t1 inner join e_times t2 on t1.post_id = t2.post_id
    where t1.effective_from != t2.effective_from and t1.e_to != t2.e_to and t1.e_to < t2.effective_from
    group by t1.post_id, t1.views, t1.likes, t1.shares, t1.effective_from
    union (
        select post_id, views, likes, shares, effective_from, '9999-12-31 23:59:59' as effective_to
        from e_times
        where (post_id, effective_from) in (
            select post_id,  max(effective_from)
            from e_times
            group by post_id
        )
    )
);
*/

-- new
insert into posts_stats_new (post_id, views, likes, shares, effective_from, effective_to) (
    select t1.post_id, t1.views, t1.likes, t1.shares, min(t1.dttm) as effective_from,
        coalesce(min(t2.dttm), '9999-12-31 23:59:59') as effective_to
    from posts_stats t1 left join posts_stats t2 on
        t1.post_id = t2.post_id and t1.dttm < t2.dttm and
        (t1.views != t2.views or t1.likes != t2.likes or t1.shares != t2.shares)
    group by t1.post_id, t1.views, t1.likes, t1.shares
);

drop table posts_stats;

alter table posts_stats_new rename to posts_stats;

commit;

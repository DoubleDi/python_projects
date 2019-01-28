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

insert into posts_stats_new (post_id, views, likes, shares, effective_from, effective_to) (
    select distinct post_id, views, likes, shares, effective_from, effective_to
    from (
        select post_id, views, likes, shares,
            min(dttm) over(partition by views, likes, shares) as effective_from,
            max(dttm) over(partition by views, likes, shares) as effective_to
        from posts_stats
    ) as d
    order by post_id, effective_from
);

drop table posts_stats;

alter table posts_stats_new rename to posts_stats;

commit;
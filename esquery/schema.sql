create type status as enum ('STARTED', 'FAILED', 'SUCCESS');

create table file_processing_queue (
    id varchar(255) primary key,
    status status not null default 'STARTED',
    reason text null,
    content jsonb null,
    created_at timestamp not null default now ()
);

alter table file_processing_queue add constraint unique_id unique (id);

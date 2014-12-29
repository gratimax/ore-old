drop table files;

create table versions (
  id              serial primary key unique,
  project_id      integer references projects(id),
  name            varchar(64) unique not null,
  description     varchar(128),
  file_hash       varchar(64)
);

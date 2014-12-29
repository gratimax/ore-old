create table users (
  id              serial primary key unique,
  name            varchar(128) unique not null,
  email           varchar(128) not null,
  password        varchar(64) not null
);

create table orgs (
  id              serial primary key unique,
  name            varchar(128) unique not null,
  is_namespace    boolean not null,
  namespace       integer references users(id)
);

create table org_memberships (
  user_id         integer references users(id) not null,
  org_id          integer references orgs(id) not null,
  role            varchar(32)
);

create table projects (
  id              serial primary key unique,
  owner_id        integer references orgs(id),
  name            varchar(128) not null,
  description     varchar(512)
);

create table project_memberships (
  user_id         integer references users(id) not null,
  project_id      integer references projects(id) not null,
  role            varchar(32)
);

create table files (
  id              serial primary key unique,
  project_id      integer references projects(id),
  name            varchar(128) unique not null,
  description     varchar(512),
  hash            varchar(64) not null
);

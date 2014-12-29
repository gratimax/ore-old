create table sessions (
  sid             varchar(32) not null,
  user_id         integer references users(id) not null
)

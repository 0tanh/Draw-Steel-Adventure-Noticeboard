create table public.profiles (
  id uuid not null references auth.users on delete cascade,
  first_name text,
  last_name text,
  avatar_url text,
  primary key (id)
);
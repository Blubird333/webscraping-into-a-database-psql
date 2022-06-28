--these parameters are from jobs.txt.
drop table if exists job_openings;

create table job_openings(
  id serial primary key,
  title text,
  job_id text,
  company_name text,
  jd_url text,
  jd_text text
);

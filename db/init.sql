CREATE TABLE IF NOT EXISTS  snip_key (
    id          SERIAL PRIMARY KEY,
    key         TEXT UNIQUE,
    create_time TIMESTAMP,
    update_time TIMESTAMP,
    password    TEXT
);

CREATE TABLE IF NOT EXISTS  snip_value (
    id          SERIAL PRIMARY KEY,
    key_id      INTEGER REFERENCES snip_key (id),
    value       TEXT,
    update_time TIMESTAMP
);

CREATE TABLE  IF NOT EXISTS  public.snip_files (
	id SERIAL PRIMARY KEY,
	key_id int4 NULL,
	file bytea NULL,
	file_md5 bpchar(32) NULL,
	file_size int4 NULL,
	file_name varchar NULL,
	create_time TIMESTAMP,
	CONSTRAINT snip_files_snip_key_id_fk FOREIGN KEY (key_id) REFERENCES public.snip_key(id) ON DELETE CASCADE ON UPDATE cascade
);

CREATE TABLE  IF NOT EXISTS  public.snip_log (
	id SERIAL PRIMARY KEY,
	key_id int4 NULL,
	ip inet NULL,
	acction text NULL,
	CONSTRAINT snip_log_snip_key_id_fk FOREIGN KEY (key_id) REFERENCES public.snip_key(id)
);
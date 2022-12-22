CREATE TABLE requests (
    id integer CONSTRAINT firstkey PRIMARY KEY,
    date_application timestamp without time zone,
    family_name text,
    first_name text,
    father_name text,
    telephone int,
    requests_text text
);
CREATE TABLE requests (
    id integer CONSTRAINT firstkey PRIMARY KEY,
    date_application date,
    last_name text,
    first_name text,
    patronymic_name text,
    tel integer,
    request_text text
);
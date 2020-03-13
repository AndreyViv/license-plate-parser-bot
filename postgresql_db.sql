--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET default_tablespace = '';

SET default_with_oids = false;

---
--- drop table bot_data
---

DROP TABLE IF EXISTS bot_data;

--
-- create table bot_data
--

CREATE TABLE bot_data (
    data_id serial PRIMARY KEY,
    licence_plate text,
    photo bytea,
    user_id int,
    user_first_name text,
    user_last_name text,
    message_date date
);

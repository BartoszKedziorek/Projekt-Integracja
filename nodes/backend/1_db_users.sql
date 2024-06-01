--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE projekt_integracja;
ALTER ROLE projekt_integracja WITH NOSUPERUSER INHERIT NOCREATEROLE CREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:dGjIBZfJA95AQz/M2VeCYg==$e6AvB0nuEnbKa1c8/GQD1oAK6TPALbB7oIYd7jAtrKk=:MwaT72WUhw+WHebKXTXdJRV/NN291yHXnB2m3RP4h3M=';

--
-- User Configurations
--

--
-- User Config "projekt_integracja"
--

ALTER ROLE projekt_integracja SET search_path TO 'main', 'public';








--
-- PostgreSQL database cluster dump complete
--


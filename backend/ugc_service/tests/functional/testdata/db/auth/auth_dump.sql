--
-- PostgreSQL database dump
--

-- Dumped from database version 14.3
-- Dumped by pg_dump version 14.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: content; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA content;


ALTER SCHEMA content OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_token; Type: TABLE; Schema: content; Owner: admin
--

CREATE TABLE content.auth_token (
    id uuid NOT NULL,
    public_address text,
    user_agent text NOT NULL,
    refresh_token text NOT NULL
);


ALTER TABLE content.auth_token OWNER TO admin;

--
-- Name: login_history; Type: TABLE; Schema: content; Owner: admin
--

CREATE TABLE content.login_history (
    id uuid NOT NULL,
    public_address text,
    datetime timestamp without time zone,
    user_agent text NOT NULL
);


ALTER TABLE content.login_history OWNER TO admin;

--
-- Name: permissions; Type: TABLE; Schema: content; Owner: admin
--

CREATE TABLE content.permissions (
    id uuid NOT NULL,
    permission character varying(50) NOT NULL
);


ALTER TABLE content.permissions OWNER TO admin;

--
-- Name: profiles; Type: TABLE; Schema: content; Owner: admin
--

CREATE TABLE content.profiles (
    id uuid NOT NULL,
    public_address text,
    username character varying NOT NULL,
    phone integer,
    image character varying,
    created timestamp without time zone,
    updated timestamp without time zone
);


ALTER TABLE content.profiles OWNER TO admin;

--
-- Name: roles; Type: TABLE; Schema: content; Owner: admin
--

CREATE TABLE content.roles (
    id uuid NOT NULL,
    name character varying(64) NOT NULL,
    description text
);


ALTER TABLE content.roles OWNER TO admin;

--
-- Name: roles_permissions; Type: TABLE; Schema: content; Owner: admin
--

CREATE TABLE content.roles_permissions (
    id uuid NOT NULL,
    role_id uuid,
    permission_id uuid
);


ALTER TABLE content.roles_permissions OWNER TO admin;

--
-- Name: roles_users; Type: TABLE; Schema: content; Owner: admin
--

CREATE TABLE content.roles_users (
    id uuid NOT NULL,
    public_address text,
    role_id uuid
);


ALTER TABLE content.roles_users OWNER TO admin;

--
-- Name: users; Type: TABLE; Schema: content; Owner: admin
--

CREATE TABLE content.users (
    created timestamp without time zone,
    updated timestamp without time zone,
    public_address character varying(256) NOT NULL,
    nonce character varying(64) NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE content.users OWNER TO admin;


--
-- Data for Name: users; Type: TABLE DATA; Schema: content; Owner: admin
--

INSERT INTO content.users (created, updated, public_address, nonce, active) VALUES
('2022-10-09 21:11:21.044184', NULL, '0x45bcd9a9c4c8ebd2d8c7d9dba8107a6dd47768fa', 92182, TRUE),
('2022-10-09 21:11:21.044184', NULL, '0xc7753ce81b3389fc0bee367b875021637c3fff35', 21995, TRUE),
('2022-10-09 21:11:21.044185', NULL, '0xc4b643fc991352202cb5ad071d00ebc0a258ce56', 25970, TRUE);
--
-- Data for Name: roles; Type: TABLE DATA; Schema: content; Owner: admin
--

INSERT INTO content.roles (id, name, description) VALUES
('4542fd6a-b24e-4950-86b3-ae287a8fce22', 'admin', 'sdsd'),
('4542fd6a-b24e-4950-86b3-ae287a8fce33', 'superadmin', 'sdsd'),
('4542fd6a-b24e-4950-86b3-ae287a8fce44', 'moderator', 'sdsd'),
('4542fd6a-b24e-4950-86b3-ae287a8fce77', 'user', 'sdsd');
--
-- Data for Name: roles_users; Type: TABLE DATA; Schema: content; Owner: admin
--

INSERT INTO content.roles_users (id, public_address, role_id) VALUES
('85d6c9bc-5dd8-4e59-b368-9f546b1369ba', '0xc4b643fc991352202cb5ad071d00ebc0a258ce56', '4542fd6a-b24e-4950-86b3-ae287a8fce22'),
('4542fd6a-b24e-4950-86b3-ae287a8fce34', '0xc4b643fc991352202cb5ad071d00ebc0a258ce56', '4542fd6a-b24e-4950-86b3-ae287a8fce44'),
('235dfdb0-3106-4864-abea-f8de0d5e4896', '0xc4b643fc991352202cb5ad071d00ebc0a258ce56', '4542fd6a-b24e-4950-86b3-ae287a8fce77'),
('235dfdb0-3106-4864-abea-f8de0d5e4895', '0xc7753ce81b3389fc0bee367b875021637c3fff35', '4542fd6a-b24e-4950-86b3-ae287a8fce77'),
('797dd60f-dceb-479e-aeb2-147c33218a08', '0x45bcd9a9c4c8ebd2d8c7d9dba8107a6dd47768fa', '4542fd6a-b24e-4950-86b3-ae287a8fce77');

--
-- Data for Name: permissions; Type: TABLE DATA; Schema: content; Owner: admin
--

--
-- Data for Name: profiles; Type: TABLE DATA; Schema: content; Owner: admin
--

INSERT INTO content.profiles (id, public_address, username, phone, image, created, updated) VALUES
('b7da3b79-9571-48b6-8412-49a1845c6e6b', '0x45bcd9a9c4c8ebd2d8c7d9dba8107a6dd47768fa', 'test_user', NULL, 'haqoz_logosk2.png', '2022-10-09 21:11:21.044184', '2022-10-09 21:11:21.04516'),
('7f42f3df-833a-47b9-aaf7-81fb2be8b162', '0xc7753ce81b3389fc0bee367b875021637c3fff35', 'prosto_user', NULL, 'about-img3.png', '2022-10-09 21:11:21.044184', '2023-01-20 16:55:27.088224'),
('3ac51dae-449c-4a70-9a12-4b1a92cb613a', '0xc4b643fc991352202cb5ad071d00ebc0a258ce56', 'admin_syperadmin', NULL, 'Avatar.jpg', '2022-10-10 05:57:14.424528', '2023-01-20 16:55:27.088224');

--
-- Name: auth_token auth_token_pkey; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.auth_token
    ADD CONSTRAINT auth_token_pkey PRIMARY KEY (id);


--
-- Name: login_history login_history_pkey; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.login_history
    ADD CONSTRAINT login_history_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_permission_key; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.permissions
    ADD CONSTRAINT permissions_permission_key UNIQUE (permission);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_image_key; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.profiles
    ADD CONSTRAINT profiles_image_key UNIQUE (image);


--
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_username_key; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.profiles
    ADD CONSTRAINT profiles_username_key UNIQUE (username);


--
-- Name: roles_permissions role_permission_inx; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.roles_permissions
    ADD CONSTRAINT role_permission_inx UNIQUE (permission_id, role_id);


--
-- Name: roles_users role_user_inx; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.roles_users
    ADD CONSTRAINT role_user_inx UNIQUE (public_address, role_id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles_permissions roles_permissions_pkey; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.roles_permissions
    ADD CONSTRAINT roles_permissions_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: roles_users roles_users_pkey; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.roles_users
    ADD CONSTRAINT roles_users_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (public_address);


--
-- Name: users users_public_address_key; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.users
    ADD CONSTRAINT users_public_address_key UNIQUE (public_address);


--
-- Name: users users_public_address_key1; Type: CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.users
    ADD CONSTRAINT users_public_address_key1 UNIQUE (public_address);


--
-- Name: auth_token auth_token_public_address_fkey; Type: FK CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.auth_token
    ADD CONSTRAINT auth_token_public_address_fkey FOREIGN KEY (public_address) REFERENCES content.users(public_address);


--
-- Name: login_history login_history_public_address_fkey; Type: FK CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.login_history
    ADD CONSTRAINT login_history_public_address_fkey FOREIGN KEY (public_address) REFERENCES content.users(public_address);


--
-- Name: profiles profiles_public_address_fkey; Type: FK CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.profiles
    ADD CONSTRAINT profiles_public_address_fkey FOREIGN KEY (public_address) REFERENCES content.users(public_address);


--
-- Name: roles_permissions roles_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.roles_permissions
    ADD CONSTRAINT roles_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES content.permissions(id);


--
-- Name: roles_permissions roles_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.roles_permissions
    ADD CONSTRAINT roles_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES content.roles(id);


--
-- Name: roles_users roles_users_public_address_fkey; Type: FK CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.roles_users
    ADD CONSTRAINT roles_users_public_address_fkey FOREIGN KEY (public_address) REFERENCES content.users(public_address);


--
-- Name: roles_users roles_users_role_id_fkey; Type: FK CONSTRAINT; Schema: content; Owner: admin
--

ALTER TABLE ONLY content.roles_users
    ADD CONSTRAINT roles_users_role_id_fkey FOREIGN KEY (role_id) REFERENCES content.roles(id);


--
-- PostgreSQL database dump complete
--

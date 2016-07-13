--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.20
-- Dumped by pg_dump version 9.1.3
-- Started on 2016-06-29 15:13:08

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 225 (class 3079 OID 11645)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2342 (class 0 OID 0)
-- Dependencies: 225
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 168 (class 1259 OID 409600)
-- Dependencies: 6
-- Name: auth_group; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO app_tvof;

--
-- TOC entry 167 (class 1259 OID 409598)
-- Dependencies: 6 168
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO app_tvof;

--
-- TOC entry 2343 (class 0 OID 0)
-- Dependencies: 167
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- TOC entry 2344 (class 0 OID 0)
-- Dependencies: 167
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('auth_group_id_seq', 2, true);


--
-- TOC entry 170 (class 1259 OID 409610)
-- Dependencies: 6
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO app_tvof;

--
-- TOC entry 169 (class 1259 OID 409608)
-- Dependencies: 170 6
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO app_tvof;

--
-- TOC entry 2345 (class 0 OID 0)
-- Dependencies: 169
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- TOC entry 2346 (class 0 OID 0)
-- Dependencies: 169
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 14, true);


--
-- TOC entry 166 (class 1259 OID 409592)
-- Dependencies: 6
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO app_tvof;

--
-- TOC entry 165 (class 1259 OID 409590)
-- Dependencies: 6 166
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO app_tvof;

--
-- TOC entry 2347 (class 0 OID 0)
-- Dependencies: 165
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- TOC entry 2348 (class 0 OID 0)
-- Dependencies: 165
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('auth_permission_id_seq', 91, true);


--
-- TOC entry 172 (class 1259 OID 409618)
-- Dependencies: 6
-- Name: auth_user; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO app_tvof;

--
-- TOC entry 174 (class 1259 OID 409628)
-- Dependencies: 6
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO app_tvof;

--
-- TOC entry 173 (class 1259 OID 409626)
-- Dependencies: 6 174
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO app_tvof;

--
-- TOC entry 2349 (class 0 OID 0)
-- Dependencies: 173
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- TOC entry 2350 (class 0 OID 0)
-- Dependencies: 173
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 6, true);


--
-- TOC entry 171 (class 1259 OID 409616)
-- Dependencies: 172 6
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO app_tvof;

--
-- TOC entry 2351 (class 0 OID 0)
-- Dependencies: 171
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 2352 (class 0 OID 0)
-- Dependencies: 171
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('auth_user_id_seq', 4, true);


--
-- TOC entry 176 (class 1259 OID 409636)
-- Dependencies: 6
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO app_tvof;

--
-- TOC entry 175 (class 1259 OID 409634)
-- Dependencies: 176 6
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO app_tvof;

--
-- TOC entry 2353 (class 0 OID 0)
-- Dependencies: 175
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- TOC entry 2354 (class 0 OID 0)
-- Dependencies: 175
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- TOC entry 196 (class 1259 OID 409978)
-- Dependencies: 6
-- Name: cms_blogindexpage; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE cms_blogindexpage (
    page_ptr_id integer NOT NULL
);


ALTER TABLE public.cms_blogindexpage OWNER TO app_tvof;

--
-- TOC entry 197 (class 1259 OID 409983)
-- Dependencies: 6
-- Name: cms_blogpost; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE cms_blogpost (
    page_ptr_id integer NOT NULL,
    content text
);


ALTER TABLE public.cms_blogpost OWNER TO app_tvof;

--
-- TOC entry 193 (class 1259 OID 409942)
-- Dependencies: 6
-- Name: cms_homepage; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE cms_homepage (
    page_ptr_id integer NOT NULL,
    content text NOT NULL
);


ALTER TABLE public.cms_homepage OWNER TO app_tvof;

--
-- TOC entry 195 (class 1259 OID 409965)
-- Dependencies: 6
-- Name: cms_indexpage; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE cms_indexpage (
    page_ptr_id integer NOT NULL,
    content text NOT NULL
);


ALTER TABLE public.cms_indexpage OWNER TO app_tvof;

--
-- TOC entry 194 (class 1259 OID 409952)
-- Dependencies: 6
-- Name: cms_richtextpage; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE cms_richtextpage (
    page_ptr_id integer NOT NULL,
    content text NOT NULL
);


ALTER TABLE public.cms_richtextpage OWNER TO app_tvof;

--
-- TOC entry 178 (class 1259 OID 409696)
-- Dependencies: 2067 6
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO app_tvof;

--
-- TOC entry 177 (class 1259 OID 409694)
-- Dependencies: 6 178
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO app_tvof;

--
-- TOC entry 2355 (class 0 OID 0)
-- Dependencies: 177
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- TOC entry 2356 (class 0 OID 0)
-- Dependencies: 177
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- TOC entry 164 (class 1259 OID 409582)
-- Dependencies: 6
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO app_tvof;

--
-- TOC entry 163 (class 1259 OID 409580)
-- Dependencies: 164 6
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO app_tvof;

--
-- TOC entry 2357 (class 0 OID 0)
-- Dependencies: 163
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- TOC entry 2358 (class 0 OID 0)
-- Dependencies: 163
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('django_content_type_id_seq', 31, true);


--
-- TOC entry 162 (class 1259 OID 409571)
-- Dependencies: 6
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO app_tvof;

--
-- TOC entry 161 (class 1259 OID 409569)
-- Dependencies: 162 6
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO app_tvof;

--
-- TOC entry 2359 (class 0 OID 0)
-- Dependencies: 161
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- TOC entry 2360 (class 0 OID 0)
-- Dependencies: 161
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('django_migrations_id_seq', 91, true);


--
-- TOC entry 198 (class 1259 OID 409998)
-- Dependencies: 6
-- Name: django_session; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO app_tvof;

--
-- TOC entry 200 (class 1259 OID 410010)
-- Dependencies: 6
-- Name: taggit_tag; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE taggit_tag (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL
);


ALTER TABLE public.taggit_tag OWNER TO app_tvof;

--
-- TOC entry 199 (class 1259 OID 410008)
-- Dependencies: 200 6
-- Name: taggit_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE taggit_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taggit_tag_id_seq OWNER TO app_tvof;

--
-- TOC entry 2361 (class 0 OID 0)
-- Dependencies: 199
-- Name: taggit_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE taggit_tag_id_seq OWNED BY taggit_tag.id;


--
-- TOC entry 2362 (class 0 OID 0)
-- Dependencies: 199
-- Name: taggit_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('taggit_tag_id_seq', 1, false);


--
-- TOC entry 202 (class 1259 OID 410022)
-- Dependencies: 6
-- Name: taggit_taggeditem; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE taggit_taggeditem (
    id integer NOT NULL,
    object_id integer NOT NULL,
    content_type_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.taggit_taggeditem OWNER TO app_tvof;

--
-- TOC entry 201 (class 1259 OID 410020)
-- Dependencies: 6 202
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE taggit_taggeditem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taggit_taggeditem_id_seq OWNER TO app_tvof;

--
-- TOC entry 2363 (class 0 OID 0)
-- Dependencies: 201
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE taggit_taggeditem_id_seq OWNED BY taggit_taggeditem.id;


--
-- TOC entry 2364 (class 0 OID 0)
-- Dependencies: 201
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('taggit_taggeditem_id_seq', 1, false);


--
-- TOC entry 190 (class 1259 OID 409892)
-- Dependencies: 2076 2077 6
-- Name: wagtailcore_collection; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailcore_collection (
    id integer NOT NULL,
    path character varying(255) COLLATE pg_catalog."C" NOT NULL,
    depth integer NOT NULL,
    numchild integer NOT NULL,
    name character varying(255) NOT NULL,
    CONSTRAINT wagtailcore_collection_depth_check CHECK ((depth >= 0)),
    CONSTRAINT wagtailcore_collection_numchild_check CHECK ((numchild >= 0))
);


ALTER TABLE public.wagtailcore_collection OWNER TO app_tvof;

--
-- TOC entry 189 (class 1259 OID 409890)
-- Dependencies: 6 190
-- Name: wagtailcore_collection_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailcore_collection_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailcore_collection_id_seq OWNER TO app_tvof;

--
-- TOC entry 2365 (class 0 OID 0)
-- Dependencies: 189
-- Name: wagtailcore_collection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailcore_collection_id_seq OWNED BY wagtailcore_collection.id;


--
-- TOC entry 2366 (class 0 OID 0)
-- Dependencies: 189
-- Name: wagtailcore_collection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailcore_collection_id_seq', 1, true);


--
-- TOC entry 192 (class 1259 OID 409908)
-- Dependencies: 6
-- Name: wagtailcore_groupcollectionpermission; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailcore_groupcollectionpermission (
    id integer NOT NULL,
    collection_id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.wagtailcore_groupcollectionpermission OWNER TO app_tvof;

--
-- TOC entry 191 (class 1259 OID 409906)
-- Dependencies: 192 6
-- Name: wagtailcore_groupcollectionpermission_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailcore_groupcollectionpermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailcore_groupcollectionpermission_id_seq OWNER TO app_tvof;

--
-- TOC entry 2367 (class 0 OID 0)
-- Dependencies: 191
-- Name: wagtailcore_groupcollectionpermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailcore_groupcollectionpermission_id_seq OWNED BY wagtailcore_groupcollectionpermission.id;


--
-- TOC entry 2368 (class 0 OID 0)
-- Dependencies: 191
-- Name: wagtailcore_groupcollectionpermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailcore_groupcollectionpermission_id_seq', 8, true);


--
-- TOC entry 182 (class 1259 OID 409750)
-- Dependencies: 6
-- Name: wagtailcore_grouppagepermission; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailcore_grouppagepermission (
    id integer NOT NULL,
    permission_type character varying(20) NOT NULL,
    group_id integer NOT NULL,
    page_id integer NOT NULL
);


ALTER TABLE public.wagtailcore_grouppagepermission OWNER TO app_tvof;

--
-- TOC entry 181 (class 1259 OID 409748)
-- Dependencies: 6 182
-- Name: wagtailcore_grouppagepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailcore_grouppagepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailcore_grouppagepermission_id_seq OWNER TO app_tvof;

--
-- TOC entry 2369 (class 0 OID 0)
-- Dependencies: 181
-- Name: wagtailcore_grouppagepermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailcore_grouppagepermission_id_seq OWNED BY wagtailcore_grouppagepermission.id;


--
-- TOC entry 2370 (class 0 OID 0)
-- Dependencies: 181
-- Name: wagtailcore_grouppagepermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailcore_grouppagepermission_id_seq', 6, true);


--
-- TOC entry 180 (class 1259 OID 409733)
-- Dependencies: 2069 2070 6
-- Name: wagtailcore_page; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailcore_page (
    id integer NOT NULL,
    path character varying(255) COLLATE pg_catalog."C" NOT NULL,
    depth integer NOT NULL,
    numchild integer NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    live boolean NOT NULL,
    has_unpublished_changes boolean NOT NULL,
    url_path text NOT NULL,
    seo_title character varying(255) NOT NULL,
    show_in_menus boolean NOT NULL,
    search_description text NOT NULL,
    go_live_at timestamp with time zone,
    expire_at timestamp with time zone,
    expired boolean NOT NULL,
    content_type_id integer NOT NULL,
    owner_id integer,
    locked boolean NOT NULL,
    latest_revision_created_at timestamp with time zone,
    first_published_at timestamp with time zone,
    CONSTRAINT wagtailcore_page_depth_check CHECK ((depth >= 0)),
    CONSTRAINT wagtailcore_page_numchild_check CHECK ((numchild >= 0))
);


ALTER TABLE public.wagtailcore_page OWNER TO app_tvof;

--
-- TOC entry 179 (class 1259 OID 409731)
-- Dependencies: 6 180
-- Name: wagtailcore_page_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailcore_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailcore_page_id_seq OWNER TO app_tvof;

--
-- TOC entry 2371 (class 0 OID 0)
-- Dependencies: 179
-- Name: wagtailcore_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailcore_page_id_seq OWNED BY wagtailcore_page.id;


--
-- TOC entry 2372 (class 0 OID 0)
-- Dependencies: 179
-- Name: wagtailcore_page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailcore_page_id_seq', 30, true);


--
-- TOC entry 184 (class 1259 OID 409760)
-- Dependencies: 6
-- Name: wagtailcore_pagerevision; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailcore_pagerevision (
    id integer NOT NULL,
    submitted_for_moderation boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    content_json text NOT NULL,
    approved_go_live_at timestamp with time zone,
    page_id integer NOT NULL,
    user_id integer
);


ALTER TABLE public.wagtailcore_pagerevision OWNER TO app_tvof;

--
-- TOC entry 183 (class 1259 OID 409758)
-- Dependencies: 184 6
-- Name: wagtailcore_pagerevision_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailcore_pagerevision_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailcore_pagerevision_id_seq OWNER TO app_tvof;

--
-- TOC entry 2373 (class 0 OID 0)
-- Dependencies: 183
-- Name: wagtailcore_pagerevision_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailcore_pagerevision_id_seq OWNED BY wagtailcore_pagerevision.id;


--
-- TOC entry 2374 (class 0 OID 0)
-- Dependencies: 183
-- Name: wagtailcore_pagerevision_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailcore_pagerevision_id_seq', 53, true);


--
-- TOC entry 186 (class 1259 OID 409771)
-- Dependencies: 6
-- Name: wagtailcore_pageviewrestriction; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailcore_pageviewrestriction (
    id integer NOT NULL,
    password character varying(255) NOT NULL,
    page_id integer NOT NULL
);


ALTER TABLE public.wagtailcore_pageviewrestriction OWNER TO app_tvof;

--
-- TOC entry 185 (class 1259 OID 409769)
-- Dependencies: 6 186
-- Name: wagtailcore_pageviewrestriction_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailcore_pageviewrestriction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailcore_pageviewrestriction_id_seq OWNER TO app_tvof;

--
-- TOC entry 2375 (class 0 OID 0)
-- Dependencies: 185
-- Name: wagtailcore_pageviewrestriction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailcore_pageviewrestriction_id_seq OWNED BY wagtailcore_pageviewrestriction.id;


--
-- TOC entry 2376 (class 0 OID 0)
-- Dependencies: 185
-- Name: wagtailcore_pageviewrestriction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailcore_pageviewrestriction_id_seq', 1, false);


--
-- TOC entry 188 (class 1259 OID 409779)
-- Dependencies: 6
-- Name: wagtailcore_site; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailcore_site (
    id integer NOT NULL,
    hostname character varying(255) NOT NULL,
    port integer NOT NULL,
    is_default_site boolean NOT NULL,
    root_page_id integer NOT NULL,
    site_name character varying(255)
);


ALTER TABLE public.wagtailcore_site OWNER TO app_tvof;

--
-- TOC entry 187 (class 1259 OID 409777)
-- Dependencies: 188 6
-- Name: wagtailcore_site_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailcore_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailcore_site_id_seq OWNER TO app_tvof;

--
-- TOC entry 2377 (class 0 OID 0)
-- Dependencies: 187
-- Name: wagtailcore_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailcore_site_id_seq OWNED BY wagtailcore_site.id;


--
-- TOC entry 2378 (class 0 OID 0)
-- Dependencies: 187
-- Name: wagtailcore_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailcore_site_id_seq', 2, true);


--
-- TOC entry 204 (class 1259 OID 410046)
-- Dependencies: 6
-- Name: wagtaildocs_document; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtaildocs_document (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    file character varying(100) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    uploaded_by_user_id integer,
    collection_id integer NOT NULL
);


ALTER TABLE public.wagtaildocs_document OWNER TO app_tvof;

--
-- TOC entry 203 (class 1259 OID 410044)
-- Dependencies: 204 6
-- Name: wagtaildocs_document_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtaildocs_document_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtaildocs_document_id_seq OWNER TO app_tvof;

--
-- TOC entry 2379 (class 0 OID 0)
-- Dependencies: 203
-- Name: wagtaildocs_document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtaildocs_document_id_seq OWNED BY wagtaildocs_document.id;


--
-- TOC entry 2380 (class 0 OID 0)
-- Dependencies: 203
-- Name: wagtaildocs_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtaildocs_document_id_seq', 1, false);


--
-- TOC entry 206 (class 1259 OID 410087)
-- Dependencies: 6
-- Name: wagtailembeds_embed; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailembeds_embed (
    id integer NOT NULL,
    url character varying(200) NOT NULL,
    max_width smallint,
    type character varying(10) NOT NULL,
    html text NOT NULL,
    title text NOT NULL,
    author_name text NOT NULL,
    provider_name text NOT NULL,
    thumbnail_url character varying(200),
    width integer,
    height integer,
    last_updated timestamp with time zone NOT NULL
);


ALTER TABLE public.wagtailembeds_embed OWNER TO app_tvof;

--
-- TOC entry 205 (class 1259 OID 410085)
-- Dependencies: 206 6
-- Name: wagtailembeds_embed_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailembeds_embed_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailembeds_embed_id_seq OWNER TO app_tvof;

--
-- TOC entry 2381 (class 0 OID 0)
-- Dependencies: 205
-- Name: wagtailembeds_embed_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailembeds_embed_id_seq OWNED BY wagtailembeds_embed.id;


--
-- TOC entry 2382 (class 0 OID 0)
-- Dependencies: 205
-- Name: wagtailembeds_embed_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailembeds_embed_id_seq', 1, false);


--
-- TOC entry 208 (class 1259 OID 410100)
-- Dependencies: 6
-- Name: wagtailforms_formsubmission; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailforms_formsubmission (
    id integer NOT NULL,
    form_data text NOT NULL,
    submit_time timestamp with time zone NOT NULL,
    page_id integer NOT NULL
);


ALTER TABLE public.wagtailforms_formsubmission OWNER TO app_tvof;

--
-- TOC entry 207 (class 1259 OID 410098)
-- Dependencies: 6 208
-- Name: wagtailforms_formsubmission_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailforms_formsubmission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailforms_formsubmission_id_seq OWNER TO app_tvof;

--
-- TOC entry 2383 (class 0 OID 0)
-- Dependencies: 207
-- Name: wagtailforms_formsubmission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailforms_formsubmission_id_seq OWNED BY wagtailforms_formsubmission.id;


--
-- TOC entry 2384 (class 0 OID 0)
-- Dependencies: 207
-- Name: wagtailforms_formsubmission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailforms_formsubmission_id_seq', 1, false);


--
-- TOC entry 210 (class 1259 OID 410117)
-- Dependencies: 6
-- Name: wagtailimages_filter; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailimages_filter (
    id integer NOT NULL,
    spec character varying(255) NOT NULL
);


ALTER TABLE public.wagtailimages_filter OWNER TO app_tvof;

--
-- TOC entry 209 (class 1259 OID 410115)
-- Dependencies: 210 6
-- Name: wagtailimages_filter_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailimages_filter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailimages_filter_id_seq OWNER TO app_tvof;

--
-- TOC entry 2385 (class 0 OID 0)
-- Dependencies: 209
-- Name: wagtailimages_filter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailimages_filter_id_seq OWNED BY wagtailimages_filter.id;


--
-- TOC entry 2386 (class 0 OID 0)
-- Dependencies: 209
-- Name: wagtailimages_filter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailimages_filter_id_seq', 9, true);


--
-- TOC entry 212 (class 1259 OID 410125)
-- Dependencies: 2086 2087 2088 2089 2090 6
-- Name: wagtailimages_image; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailimages_image (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    file character varying(100) NOT NULL,
    width integer NOT NULL,
    height integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    focal_point_x integer,
    focal_point_y integer,
    focal_point_width integer,
    focal_point_height integer,
    uploaded_by_user_id integer,
    file_size integer,
    collection_id integer NOT NULL,
    CONSTRAINT wagtailimages_image_file_size_check CHECK ((file_size >= 0)),
    CONSTRAINT wagtailimages_image_focal_point_height_check CHECK ((focal_point_height >= 0)),
    CONSTRAINT wagtailimages_image_focal_point_width_check CHECK ((focal_point_width >= 0)),
    CONSTRAINT wagtailimages_image_focal_point_x_check CHECK ((focal_point_x >= 0)),
    CONSTRAINT wagtailimages_image_focal_point_y_check CHECK ((focal_point_y >= 0))
);


ALTER TABLE public.wagtailimages_image OWNER TO app_tvof;

--
-- TOC entry 211 (class 1259 OID 410123)
-- Dependencies: 212 6
-- Name: wagtailimages_image_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailimages_image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailimages_image_id_seq OWNER TO app_tvof;

--
-- TOC entry 2387 (class 0 OID 0)
-- Dependencies: 211
-- Name: wagtailimages_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailimages_image_id_seq OWNED BY wagtailimages_image.id;


--
-- TOC entry 2388 (class 0 OID 0)
-- Dependencies: 211
-- Name: wagtailimages_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailimages_image_id_seq', 63, true);


--
-- TOC entry 214 (class 1259 OID 410137)
-- Dependencies: 6
-- Name: wagtailimages_rendition; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailimages_rendition (
    id integer NOT NULL,
    file character varying(100) NOT NULL,
    width integer NOT NULL,
    height integer NOT NULL,
    focal_point_key character varying(255) NOT NULL,
    filter_id integer NOT NULL,
    image_id integer NOT NULL
);


ALTER TABLE public.wagtailimages_rendition OWNER TO app_tvof;

--
-- TOC entry 213 (class 1259 OID 410135)
-- Dependencies: 214 6
-- Name: wagtailimages_rendition_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailimages_rendition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailimages_rendition_id_seq OWNER TO app_tvof;

--
-- TOC entry 2389 (class 0 OID 0)
-- Dependencies: 213
-- Name: wagtailimages_rendition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailimages_rendition_id_seq OWNED BY wagtailimages_rendition.id;


--
-- TOC entry 2390 (class 0 OID 0)
-- Dependencies: 213
-- Name: wagtailimages_rendition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailimages_rendition_id_seq', 107, true);


--
-- TOC entry 216 (class 1259 OID 410200)
-- Dependencies: 6
-- Name: wagtailredirects_redirect; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailredirects_redirect (
    id integer NOT NULL,
    old_path character varying(255) NOT NULL,
    is_permanent boolean NOT NULL,
    redirect_link character varying(200) NOT NULL,
    redirect_page_id integer,
    site_id integer
);


ALTER TABLE public.wagtailredirects_redirect OWNER TO app_tvof;

--
-- TOC entry 215 (class 1259 OID 410198)
-- Dependencies: 216 6
-- Name: wagtailredirects_redirect_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailredirects_redirect_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailredirects_redirect_id_seq OWNER TO app_tvof;

--
-- TOC entry 2391 (class 0 OID 0)
-- Dependencies: 215
-- Name: wagtailredirects_redirect_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailredirects_redirect_id_seq OWNED BY wagtailredirects_redirect.id;


--
-- TOC entry 2392 (class 0 OID 0)
-- Dependencies: 215
-- Name: wagtailredirects_redirect_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailredirects_redirect_id_seq', 1, false);


--
-- TOC entry 218 (class 1259 OID 410245)
-- Dependencies: 6
-- Name: wagtailsearch_editorspick; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailsearch_editorspick (
    id integer NOT NULL,
    sort_order integer,
    description text NOT NULL,
    page_id integer NOT NULL,
    query_id integer NOT NULL
);


ALTER TABLE public.wagtailsearch_editorspick OWNER TO app_tvof;

--
-- TOC entry 217 (class 1259 OID 410243)
-- Dependencies: 6 218
-- Name: wagtailsearch_editorspick_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailsearch_editorspick_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailsearch_editorspick_id_seq OWNER TO app_tvof;

--
-- TOC entry 2393 (class 0 OID 0)
-- Dependencies: 217
-- Name: wagtailsearch_editorspick_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailsearch_editorspick_id_seq OWNED BY wagtailsearch_editorspick.id;


--
-- TOC entry 2394 (class 0 OID 0)
-- Dependencies: 217
-- Name: wagtailsearch_editorspick_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailsearch_editorspick_id_seq', 1, false);


--
-- TOC entry 220 (class 1259 OID 410256)
-- Dependencies: 6
-- Name: wagtailsearch_query; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailsearch_query (
    id integer NOT NULL,
    query_string character varying(255) NOT NULL
);


ALTER TABLE public.wagtailsearch_query OWNER TO app_tvof;

--
-- TOC entry 219 (class 1259 OID 410254)
-- Dependencies: 220 6
-- Name: wagtailsearch_query_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailsearch_query_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailsearch_query_id_seq OWNER TO app_tvof;

--
-- TOC entry 2395 (class 0 OID 0)
-- Dependencies: 219
-- Name: wagtailsearch_query_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailsearch_query_id_seq OWNED BY wagtailsearch_query.id;


--
-- TOC entry 2396 (class 0 OID 0)
-- Dependencies: 219
-- Name: wagtailsearch_query_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailsearch_query_id_seq', 1, false);


--
-- TOC entry 222 (class 1259 OID 410266)
-- Dependencies: 6
-- Name: wagtailsearch_querydailyhits; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailsearch_querydailyhits (
    id integer NOT NULL,
    date date NOT NULL,
    hits integer NOT NULL,
    query_id integer NOT NULL
);


ALTER TABLE public.wagtailsearch_querydailyhits OWNER TO app_tvof;

--
-- TOC entry 221 (class 1259 OID 410264)
-- Dependencies: 6 222
-- Name: wagtailsearch_querydailyhits_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailsearch_querydailyhits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailsearch_querydailyhits_id_seq OWNER TO app_tvof;

--
-- TOC entry 2397 (class 0 OID 0)
-- Dependencies: 221
-- Name: wagtailsearch_querydailyhits_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailsearch_querydailyhits_id_seq OWNED BY wagtailsearch_querydailyhits.id;


--
-- TOC entry 2398 (class 0 OID 0)
-- Dependencies: 221
-- Name: wagtailsearch_querydailyhits_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailsearch_querydailyhits_id_seq', 1, false);


--
-- TOC entry 224 (class 1259 OID 410300)
-- Dependencies: 6
-- Name: wagtailusers_userprofile; Type: TABLE; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE TABLE wagtailusers_userprofile (
    id integer NOT NULL,
    submitted_notifications boolean NOT NULL,
    approved_notifications boolean NOT NULL,
    rejected_notifications boolean NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.wagtailusers_userprofile OWNER TO app_tvof;

--
-- TOC entry 223 (class 1259 OID 410298)
-- Dependencies: 6 224
-- Name: wagtailusers_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: app_tvof
--

CREATE SEQUENCE wagtailusers_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wagtailusers_userprofile_id_seq OWNER TO app_tvof;

--
-- TOC entry 2399 (class 0 OID 0)
-- Dependencies: 223
-- Name: wagtailusers_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_tvof
--

ALTER SEQUENCE wagtailusers_userprofile_id_seq OWNED BY wagtailusers_userprofile.id;


--
-- TOC entry 2400 (class 0 OID 0)
-- Dependencies: 223
-- Name: wagtailusers_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_tvof
--

SELECT pg_catalog.setval('wagtailusers_userprofile_id_seq', 1, false);


--
-- TOC entry 2061 (class 2604 OID 409603)
-- Dependencies: 168 167 168
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- TOC entry 2062 (class 2604 OID 409613)
-- Dependencies: 169 170 170
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 2060 (class 2604 OID 409595)
-- Dependencies: 165 166 166
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- TOC entry 2063 (class 2604 OID 409621)
-- Dependencies: 172 171 172
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 2064 (class 2604 OID 409631)
-- Dependencies: 173 174 174
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- TOC entry 2065 (class 2604 OID 409639)
-- Dependencies: 175 176 176
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- TOC entry 2066 (class 2604 OID 409699)
-- Dependencies: 177 178 178
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- TOC entry 2059 (class 2604 OID 409585)
-- Dependencies: 164 163 164
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- TOC entry 2058 (class 2604 OID 409574)
-- Dependencies: 162 161 162
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- TOC entry 2079 (class 2604 OID 410013)
-- Dependencies: 199 200 200
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY taggit_tag ALTER COLUMN id SET DEFAULT nextval('taggit_tag_id_seq'::regclass);


--
-- TOC entry 2080 (class 2604 OID 410025)
-- Dependencies: 202 201 202
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY taggit_taggeditem ALTER COLUMN id SET DEFAULT nextval('taggit_taggeditem_id_seq'::regclass);


--
-- TOC entry 2075 (class 2604 OID 409895)
-- Dependencies: 189 190 190
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_collection ALTER COLUMN id SET DEFAULT nextval('wagtailcore_collection_id_seq'::regclass);


--
-- TOC entry 2078 (class 2604 OID 409911)
-- Dependencies: 192 191 192
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_groupcollectionpermission ALTER COLUMN id SET DEFAULT nextval('wagtailcore_groupcollectionpermission_id_seq'::regclass);


--
-- TOC entry 2071 (class 2604 OID 409753)
-- Dependencies: 182 181 182
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_grouppagepermission ALTER COLUMN id SET DEFAULT nextval('wagtailcore_grouppagepermission_id_seq'::regclass);


--
-- TOC entry 2068 (class 2604 OID 409736)
-- Dependencies: 180 179 180
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_page ALTER COLUMN id SET DEFAULT nextval('wagtailcore_page_id_seq'::regclass);


--
-- TOC entry 2072 (class 2604 OID 409763)
-- Dependencies: 184 183 184
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_pagerevision ALTER COLUMN id SET DEFAULT nextval('wagtailcore_pagerevision_id_seq'::regclass);


--
-- TOC entry 2073 (class 2604 OID 409774)
-- Dependencies: 185 186 186
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_pageviewrestriction ALTER COLUMN id SET DEFAULT nextval('wagtailcore_pageviewrestriction_id_seq'::regclass);


--
-- TOC entry 2074 (class 2604 OID 409782)
-- Dependencies: 187 188 188
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_site ALTER COLUMN id SET DEFAULT nextval('wagtailcore_site_id_seq'::regclass);


--
-- TOC entry 2081 (class 2604 OID 410049)
-- Dependencies: 204 203 204
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtaildocs_document ALTER COLUMN id SET DEFAULT nextval('wagtaildocs_document_id_seq'::regclass);


--
-- TOC entry 2082 (class 2604 OID 410090)
-- Dependencies: 205 206 206
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailembeds_embed ALTER COLUMN id SET DEFAULT nextval('wagtailembeds_embed_id_seq'::regclass);


--
-- TOC entry 2083 (class 2604 OID 410103)
-- Dependencies: 207 208 208
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailforms_formsubmission ALTER COLUMN id SET DEFAULT nextval('wagtailforms_formsubmission_id_seq'::regclass);


--
-- TOC entry 2084 (class 2604 OID 410120)
-- Dependencies: 210 209 210
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailimages_filter ALTER COLUMN id SET DEFAULT nextval('wagtailimages_filter_id_seq'::regclass);


--
-- TOC entry 2085 (class 2604 OID 410128)
-- Dependencies: 212 211 212
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailimages_image ALTER COLUMN id SET DEFAULT nextval('wagtailimages_image_id_seq'::regclass);


--
-- TOC entry 2091 (class 2604 OID 410140)
-- Dependencies: 213 214 214
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailimages_rendition ALTER COLUMN id SET DEFAULT nextval('wagtailimages_rendition_id_seq'::regclass);


--
-- TOC entry 2092 (class 2604 OID 410203)
-- Dependencies: 216 215 216
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailredirects_redirect ALTER COLUMN id SET DEFAULT nextval('wagtailredirects_redirect_id_seq'::regclass);


--
-- TOC entry 2093 (class 2604 OID 410248)
-- Dependencies: 217 218 218
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailsearch_editorspick ALTER COLUMN id SET DEFAULT nextval('wagtailsearch_editorspick_id_seq'::regclass);


--
-- TOC entry 2094 (class 2604 OID 410259)
-- Dependencies: 220 219 220
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailsearch_query ALTER COLUMN id SET DEFAULT nextval('wagtailsearch_query_id_seq'::regclass);


--
-- TOC entry 2095 (class 2604 OID 410269)
-- Dependencies: 222 221 222
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailsearch_querydailyhits ALTER COLUMN id SET DEFAULT nextval('wagtailsearch_querydailyhits_id_seq'::regclass);


--
-- TOC entry 2096 (class 2604 OID 410303)
-- Dependencies: 224 223 224
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailusers_userprofile ALTER COLUMN id SET DEFAULT nextval('wagtailusers_userprofile_id_seq'::regclass);


--
-- TOC entry 2305 (class 0 OID 409600)
-- Dependencies: 168
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY auth_group (id, name) FROM stdin;
1	Moderators
2	Editors
\.


--
-- TOC entry 2306 (class 0 OID 409610)
-- Dependencies: 170
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
1	1	1
2	2	1
3	1	2
4	1	3
5	1	4
6	2	2
7	2	3
8	2	4
9	1	5
10	1	6
11	1	7
12	2	5
13	2	6
14	2	7
\.


--
-- TOC entry 2304 (class 0 OID 409592)
-- Dependencies: 166
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can access Wagtail admin	3	access_admin
2	Can add document	4	add_document
3	Can change document	4	change_document
4	Can delete document	4	delete_document
5	Can add image	5	add_image
6	Can change image	5	change_image
7	Can delete image	5	delete_image
8	Can add form submission	6	add_formsubmission
9	Can change form submission	6	change_formsubmission
10	Can delete form submission	6	delete_formsubmission
11	Can add redirect	7	add_redirect
12	Can change redirect	7	change_redirect
13	Can delete redirect	7	delete_redirect
14	Can add embed	8	add_embed
15	Can change embed	8	change_embed
16	Can delete embed	8	delete_embed
17	Can add user profile	9	add_userprofile
18	Can change user profile	9	change_userprofile
19	Can delete user profile	9	delete_userprofile
20	Can add filter	10	add_filter
21	Can change filter	10	change_filter
22	Can delete filter	10	delete_filter
23	Can add rendition	11	add_rendition
24	Can change rendition	11	change_rendition
25	Can delete rendition	11	delete_rendition
26	Can add query	12	add_query
27	Can change query	12	change_query
28	Can delete query	12	delete_query
29	Can add Query Daily Hits	13	add_querydailyhits
30	Can change Query Daily Hits	13	change_querydailyhits
31	Can delete Query Daily Hits	13	delete_querydailyhits
32	Can add site	14	add_site
33	Can change site	14	change_site
34	Can delete site	14	delete_site
35	Can add page	1	add_page
36	Can change page	1	change_page
37	Can delete page	1	delete_page
38	Can add page revision	15	add_pagerevision
39	Can change page revision	15	change_pagerevision
40	Can delete page revision	15	delete_pagerevision
41	Can add group page permission	16	add_grouppagepermission
42	Can change group page permission	16	change_grouppagepermission
43	Can delete group page permission	16	delete_grouppagepermission
44	Can add page view restriction	17	add_pageviewrestriction
45	Can change page view restriction	17	change_pageviewrestriction
46	Can delete page view restriction	17	delete_pageviewrestriction
47	Can add collection	18	add_collection
48	Can change collection	18	change_collection
49	Can delete collection	18	delete_collection
50	Can add group collection permission	19	add_groupcollectionpermission
51	Can change group collection permission	19	change_groupcollectionpermission
52	Can delete group collection permission	19	delete_groupcollectionpermission
53	Can add Tag	20	add_tag
54	Can change Tag	20	change_tag
55	Can delete Tag	20	delete_tag
56	Can add Tagged Item	21	add_taggeditem
57	Can change Tagged Item	21	change_taggeditem
58	Can delete Tagged Item	21	delete_taggeditem
59	Can add log entry	22	add_logentry
60	Can change log entry	22	change_logentry
61	Can delete log entry	22	delete_logentry
62	Can add permission	23	add_permission
63	Can change permission	23	change_permission
64	Can delete permission	23	delete_permission
65	Can add group	24	add_group
66	Can change group	24	change_group
67	Can delete group	24	delete_group
68	Can add user	25	add_user
69	Can change user	25	change_user
70	Can delete user	25	delete_user
71	Can add content type	26	add_contenttype
72	Can change content type	26	change_contenttype
73	Can delete content type	26	delete_contenttype
74	Can add session	27	add_session
75	Can change session	27	change_session
76	Can delete session	27	delete_session
77	Can add home page	2	add_homepage
78	Can change home page	2	change_homepage
79	Can delete home page	2	delete_homepage
80	Can add index page	28	add_indexpage
81	Can change index page	28	change_indexpage
82	Can delete index page	28	delete_indexpage
83	Can add rich text page	29	add_richtextpage
84	Can change rich text page	29	change_richtextpage
85	Can delete rich text page	29	delete_richtextpage
86	Can add blog index page	30	add_blogindexpage
87	Can change blog index page	30	change_blogindexpage
88	Can delete blog index page	30	delete_blogindexpage
89	Can add blog post	31	add_blogpost
90	Can change blog post	31	change_blogpost
91	Can delete blog post	31	delete_blogpost
\.


--
-- TOC entry 2307 (class 0 OID 409618)
-- Dependencies: 172
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
3	pbkdf2_sha256$24000$GyZY31UWYZ7b$NjaMe/TaC2/XHvFqEKk5Q4wFfxdtpht5ogC17mb11J8=	\N	t	sgaunt	Simon	Gaunt	simon.gaunt@kcl.ac.uk	t	t	2016-05-24 15:29:23.298621+01
4	pbkdf2_sha256$24000$wsAQa30A6ne8$wq9nbVCPPO9uJHw8rRp4SWYjZ4CQEIkrXvISrwT8oZ8=	\N	t	sventura	Simone	Ventura	simone.ventura@kcl.ac.uk	t	t	2016-05-24 15:29:51.280862+01
2	pbkdf2_sha256$24000$K13eN27D0BNp$0zejFkgmUquP32+7LKCfvPaC6ntVuv6Yryj2L/qUMPw=	2016-05-26 15:24:05.745326+01	t	hmorcos	Hannah	Morcos	hannah.j.morcos@kcl.ac.uk	t	t	2016-05-24 15:17:59.535662+01
1	pbkdf2_sha256$24000$VsyH1fHhsiJc$aQT2336u721L6im3uYa+A0kVSusEWuGSSGH1gtCWcjI=	2016-06-16 12:28:12.826968+01	t	njakeman			neil.jakeman@kcl.ac.uk	t	t	2016-05-16 11:54:53.655261+01
\.


--
-- TOC entry 2308 (class 0 OID 409628)
-- Dependencies: 174
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
1	2	1
2	2	2
3	3	1
4	3	2
5	4	1
6	4	2
\.


--
-- TOC entry 2309 (class 0 OID 409636)
-- Dependencies: 176
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2321 (class 0 OID 409978)
-- Dependencies: 196
-- Data for Name: cms_blogindexpage; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY cms_blogindexpage (page_ptr_id) FROM stdin;
15
20
\.


--
-- TOC entry 2322 (class 0 OID 409983)
-- Dependencies: 197
-- Data for Name: cms_blogpost; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY cms_blogpost (page_ptr_id, content) FROM stdin;
26	[{"type": "paragraph", "value": "<p>We are delighted to announce that we have appointed Henry Ravenhall as the project\\u2019s PhD student. Henry was selected from a strong field of applicants, and we thank all those who took the time to apply.</p><p>Henry discusses his research interests and PhD proposal below.</p><p>\\u2018I completed a BA in French and History at KCL in 2015, focussing on late antique and medieval history. My undergraduate dissertation concerned a piece of medieval Latin historiography entitled\\u00a0<i>Historia Comitum Ghisnensium</i>\\u00a0(\\u2018History of the Counts of Guines\\u2019) in which by applying a quantitative approach I sought to ascertain how descriptions of character (\\u2018being\\u2019) and conduct (\\u2018doing\\u2019) changed according to the historical chronology presented within the text. I have therefore been very much interested in applying linguistic methods to answer historical questions.\\u00a0I am currently studying for an MA in French Literature and Culture also at KCL, which I will complete in September 2016. I am also taking bi-weekly classes in Latin and have been attending palaeography sessions. I have become increasingly interested in how medieval languages interact and develop over time, particularly in relation to processes of vernacularisation.\\u00a0</p>"}, {"type": "image_and_text", "value": {"text": "<p>My research proposal essentially seeks to question the divide between \\u2018Fiction\\u2019 and \\u2018History\\u2019 that as modern readers we impose upon medieval texts. Our simplistic attribution of these categories appears to belie contemporary consideration of the texts. It is my belief that we should attempt to identify firstly whether these categories can be kept at all, and secondly, if they are indeed problematic, what we may use to take their place. I\\u2019d like to ask: What can manuscript dissemination and compilation tell us about how medieval authors and audiences conceived of their texts? How does the choice of language (in regard to the local context) affect the textual discourse? What can notions of orality and spoken-ness communicate about how texts were initially formed and then received? And then, perhaps most crucially: how static or fluid are any such generic distinctions and how may they have changed over time and space in Europe between 1100\\u20131450?\\u2019</p>", "image": 41, "alignment": "right", "caption": "<p>Henry Ravenhall</p>"}}]
27	[{"type": "paragraph", "value": "<p><em>The Values of French Language and Literature in the European Middle Ages</em>\\u00a0is pleased to announce one three-year fully-funded PhD studentship, to begin on 1 September 2016 and to be held in the Department of French at King\\u2019s College London. The student\\u2019s primary supervisor will be Professor\\u00a0<a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/gaunt/index.aspx\\">Simon Gaunt</a>, with Dr\\u00a0<a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/venturas.aspx\\">Simone Ventura</a>\\u00a0as secondary supervisor.</p><p>The studentship will pay home/EU fees (currently \\u00a34,600) and a maintenance allowance equivalent to an AHRC studentship (currently \\u00a316,057). Applicants are expected to have a first degree demonstrating competence in medieval and modern French at the level of at least a 2.1 and would normally be expected to have an MA (or to be in the process of completing an MA) in a relevant subject, or equivalent, to the level of at least a Merit. Applicants also need to meet the standard English-language entry requirements for\\u00a0<a href=\\"http://www.kcl.ac.uk/study/postgraduate/apply/entry-requirements/english-language.aspx\\">King\\u2019s College London</a>, and should note that theses must normally be written in English (only under exceptional circumstances are PhD students in the Department of French permitted to write theses in French).</p><p>The student will undertake a programme of doctoral research on a topic that falls broadly within one of the projects three strands: for further details see\\u00a0<a href=\\"http://blogs.kcl.ac.uk/tvof/about-tvof/more-about-the-project/\\">more about the project</a>. Candidates wishing to discuss an application informally may contact either\\u00a0<a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/gaunt/index.aspx\\">Simon Gaunt</a>\\u00a0or\\u00a0<a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/venturas.aspx\\">Simone Ventura</a>\\u00a0and should submit an application to simon.gaunt@kcl.ac.uk by midnight on 29 January 2016 consisting of the following:</p><ul><li>A research proposal consisting of no more than 2 sides of A4</li><li>A Curriculum Vitae that includes details of all academic qualifications</li><li>Two references: you should ask your referees to send these independently to\\u00a0<a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/gaunt/index.aspx\\">Simon Gaunt</a>\\u00a0by the deadline</li></ul>"}, {"type": "image_and_text", "value": {"text": "<p>The successful candidate will subsequently be asked to submit a formal application for a place on the PhD programme at King\\u2019s College London if s/he has not already done so.</p><p>The project student will be a full member of the project team and be expected to take part in team meetings, seminars, and conferences. S/he will receive training in working with manuscripts, will be provided with his/her own laptop, and will be eligible for the project\\u2019s travel funds.</p>", "image": 31, "alignment": "right", "caption": "<p>Detail of a miniature of Troy, from London, British Library, Royal 20 D I, f. 67r. Reproduced with the permission of the British Library Board.</p>"}}]
28	[{"type": "paragraph", "value": "<p>The\\u00a0<i>Histoire ancienne\\u00a0</i>is a text obsessed with origins, whether tracing back the evolution of cultural and intellectual customs (as explored in this\\u00a0<a href=\\"http://www.tvof.ac.uk/blog/medieval-present-and-biblical-past-continuity-change-and-doubt/\\">post</a>), or, perhaps more significantly, attempting to establish the genealogical roots of contemporary medieval society. Questions concerning how origins affect behaviour and (il)legitimate heirs abound throughout. One rogue example, however, complicates this message. It is the longest secular \\u2018anecdote\\u2019 inserted into the Genesis section, introduced by the perplexing rubric: \\u2018C\\u2019on ne doit faire en chambre de haut home nulle laide figure\\u2019\\u00a0 (Why a nobleman shouldn\\u2019t have [images of] ugly figures in his bedroom) (Paris, BNF, f. fr. 20125, f. 48vb). Whilst much of the other supplementary material can be traced back to Peter Comestor\\u2019s\\u00a0<i>Historia scholastica</i>\\u00a0amongst other sources, this intervention represents the author\\u2019s development of an unusual theological commentary.\\u00a0</p>"}, {"type": "image_and_caption", "value": {"images": 38, "caption": "<p>Miniature of Jacob kneeling\\u00a0before Isaac,\\u00a0pretending to be his brother Esau, from Paris, BnF, f. fr. 20125, f. 43v.\\u00a0Source:\\u00a0<a href=\\"http://gallica.bnf.fr/\\">Gallica.BnF.fr</a>.</p>"}}, {"type": "paragraph", "value": "<p>The episode that precedes this anecdote concerns Jacob\\u2019s request to leave Laban, his father-in-law and uncle, after many years of service, the acquisition of two wives and multiple children. Laban refuses to let him go and instead offers to pay him for tending his flock. Jacob then proposes the speckled animals as payment. Laban agrees to this, and the flock is thus divided. We then hear how Jacob miraculously causes the speckled flock to increase. Jacob\\u2019s \\u2018engin\\u2019 (ruse) is described as \\u2018une merveillouse chose\\u2019 which works\\u00a0\\u2018contre nature\\u2019 (f. 48ra). It involves peeling back some of the bark from branches of poplar, almond, and plane trees, and then placing them in front of the animals\\u2019 drinking place, with the intention that the plain females look at the multi-coloured branches whilst copulating. This plan works out successfully for Jacob, and soon the speckled flock increases significantly. When Laban's sons perceive what has happened, they let their father know, who then asks Jacob to swap the speckled flock for the animals of a single colour. Jacob agrees, and uses the same ruse to increase the plain animals, making the branches by \\u00a0the water a single colour (black or white with all the bark peeled off). \\u00a0His\\u00a0bewildered\\u00a0uncle gives up, realising that Jacob's flock will somehow always increase.\\u00a0</p>"}, {"type": "image_and_caption", "value": {"images": 57, "caption": "<p>Miniature from the 'Rochester Bestiary', London, British Library, Royal 12 F XIII, f. 35r. Source:\\u00a0<a href=\\"http://www.bl.uk/catalogues/illuminatedmanuscripts/ILLUMIN.ASP?Size=mid&amp;IllID=33635\\">British Library, Catalogue of Illuminated Manuscripts</a>.</p>"}}, {"type": "paragraph", "value": "<p>At first, the inserted secular tale that follows seems incongruous after the outcome of the episode. However, the narrator explains \\u2018de la semblance de ces verges deffendent li plusor sage home encore qu\\u2019en chambre a haut home ne a haute dame ne doit on paindre ne portraire diverse forme d\\u2019ome ne laide samblance\\u2019 (in the same manner as the branches, many wise men advise against painting portraits of different types of men of ugly appearance in the bedrooms of noblemen and noblewomen) (f. 48vb). So, just as the different coloured branches affected the progeny of the flock, the same could happen when \\u2018la dame concoive en l\\u2019esgardance [et] en la pensee de la semblance de la figure\\u2019 (the woman conceives whilst looking at and thinking about the appearance of the [painted] figure) (f. 48vb). After setting out its moral, the narrator tells the tale of an incredibly beautiful noblewoman and her equally attractive husband, who were very much in love. They lived in a richly adorned mansion, and their bedroom was \\u2018mout vaillans de grant maniere,\\u00a0painte [et] portraite a or [et] a asur de chief en chief tote de riches estories ancieines\\u2019 (extremely opulent, painted and decorated in gold and azure, [and] from top to bottom depicted magnificent stories of ancient times\\u2019 (ff. 48vb-49ra). In the lady\\u2019s eyeline, whilst lying in her bed, was a portrait of a figure \\u2018samblant a un noir home d\\u2019Ethiope\\u2019 (resembling a black man from Ethiopia) (f. 49ra), whose appearance is described in abhorrently racist terms. This figure greatly appealed to the lady, who looked at it constantly (\\u2018au main [et] au soir\\u2019). After being impregnated by her husband (\\u2018co[n]ciut un fiz de son baron\\u2019 (f. 49ra)), she then gives birth to a child \\u2018sambla[n]s a l\\u2019image\\u2019 ([which] resembled the image).\\u00a0</p>"}, {"type": "image_and_caption", "value": {"images": 39, "caption": "<p>Paris, BnF, f. fr. 20125, f. 48v.\\u00a0Source:\\u00a0<a href=\\"http://gallica.bnf.fr/\\">Gallica.BnF.fr</a>.</p>"}}, {"type": "paragraph", "value": "<p>It is not uncommon to find the basic principle of this tale in commentaries on how Jacob increased the speckled flock in the writings of the Church Fathers and contemporary medieval authors. In St Jerome\\u2019s\\u00a0<i>Liber quaestionum hebraicarum in Genesim</i>, immediately after describing Jacob\\u2019s ruse, he explains how it demonstrates \\u2018the nature of females in the act of conception\\u2019 (\\u2018in conceptu feminarum esse naturam\\u2019) and cites how Quintilian used it in defence of a white woman who gave birth to an Ethiopian baby. Similar comments in relation to the offspring of animals and women reflecting what they saw (or imagined) are found in Isidore of Seville\\u2019s\\u00a0<i>Etymologies</i>\\u00a0(12.58-60), amongst many others.</p><p>In the\\u00a0<i>HA</i>, the precept is developed into a short narrative insertion, an act justified by the author in his final words on the topic: \\u2018en plusors aventures que su[n]t avenues puet on prendre aucun bon essample qui veut oir retenir [et] aprendre\\u2019 (one can take good examples from many past events/adventures, [as long as you are open to] remembering and learning [from them]) (f. 49ra).\\u00a0</p><p>Yet, this narrative elaboration simultaneously reveals not only abhorrent views on racial difference, but also anxiety about the effects of female desire, which risks destabilising genealogical legitimacy. Moreover, it illustrates how the reception of penetrating depictions of \\u2018riches estories ancieines\\u2019 cannot necessarily be controlled.</p><p><br/></p><p>Bibliography</p><p>For an overview of material related to Jacob\\u2019s use of the different coloured branches, see\\u00a0<br/>Irven Resnick,\\u00a0<i>Marks of Distinctions: Christian Perceptions of Jews in the High Middle Ages</i>\\u00a0(Washington, DC: The Catholic University of America Press, 2012), pp. 291-300.</p>"}]
29	[{"type": "paragraph", "value": "<p>Last week for the first time I was able to work on the manuscript BnF f.fr. 20125 itself. With its 375 neatly written folios, it\\u2019s a substantial and impressive book. Everything about it indicates a lot of money, care and labour were invested in making it: some of the corrections made by the scribe, the rubricator and a contemporary editor bespeak attention to detail, the quality and gold decoration of the images are astonishing, and even the regularity of the quire structure suggests a meticulously executed project (see the\\u00a0description by the\\u00a0<a href=\\"http://www.medievalfrancophone.ac.uk/browse/mss/47/manuscript.html\\">MFLCOF</a>\\u00a0project). One can also tell that the book has been both read and treasured. On the one hand, the writing on some pages is badly effaced through use; on the other it is by and large in excellent condition.</p><p>As the physical structure of the manuscript is already well-documented, I spent most of my time deciphering passages from the 100 or so folios we have already transcribed that we have been unable to read from the digitisation. Another key task was the transcription of the 45 marginal annotations in a later medieval hand (late 14th\\u00a0or early 15th-c.): we had been able to make sense of only a few of these using the digitisation, partly because of the unfamiliar cursive hand, partly because a good number disappear into the gutter of the manuscript in its current 18th-c. binding and are not fully visible on the digitisation (which suggests that the original binding must have been much looser).</p><p>I guess we medievalists don\\u2019t get out much as I found the process of learning how to read this handwriting strangely exhilarating. My breakthrough came when staring for the fifth or sixth time at folio 7r and more particularly at the first annotation:</p>"}, {"type": "image_and_caption", "value": {"images": 17, "caption": "<p>BnF f.fr. 20125, f. 7r. Source: Gallica.BnF.fr.</p>"}}, {"type": "paragraph", "value": "<p>When one looks at all the annotations, one quickly realises they all begin with an abbreviated \\u2018nota\\u2019 (indeed some consist simply of \\u2018nota\\u2019), though some, as here, are hastily written. Of course context helped me here, as it did with reading the other annotations. The passage that is glossed is about the foundation of the city of Ephraim, and a few lines later we are told by the text \\u2018Ceste cite fu la premiere qui onques fu estoree\\u2019. This annotation reads \\u2018no[ta] p[ri]ma cjutat\\u2019:</p>"}, {"type": "image_and_caption", "value": {"images": 37, "caption": "<p>BnF f.fr. 20125, f. 7r detail. The beginning of 'p[ri]ma' is not visible on the digitisation. Source: Gallica.BnF.fr.</p>"}}, {"type": "paragraph", "value": "<p>Deciphering the word \\u2018cjutat\\u2019 allowed me to identify some common letters, which in turn gave me the key to reading the other annotations. A better paleographer would have got there more quickly, but small victories in research are always a pleasure!</p><p>The annotations or glosses have not attracted much attention. However, they give us an idea of what at least one later medieval reader thought worthy of remark in the\\u00a0<i>Histoire ancienne</i>,\\u00a0which in itself is of great interest to our project, as is the language in which they are written.\\u00a0Earlier scholarship deemed them to be written in Occitan, or to be the work of \\u2018someone of Spanish origin\\u2019. However, Fabio Zinelli has recently argued they are written in Catalan, and we agree. As Zinelli also suggests, this does not necessarily mean they were written in Catalonia, since our Catalan friend (as I have come to think of him) could easily have been somewhere else with a Catalan presence in the Middle Ages: Rhodes, Cyprus, or the Greek mainland.</p><p>So what was our Catalan friend interested in? The short answer is (and in this order) origins, places and people. It\\u2019s not possible to know why he stopped annotating the book after one hundred folios (perhaps a librarian caught him writing in the margins and told him off!), but one of the dominant themes of the earlier sections of the\\u00a0<i>Histoire ancienne</i>\\u00a0is the foundation of cities, the origin of customs, technologies, languages and so on: 19 of the annotations concern the foundation of cities, the first kings of significant kingdoms, the origin of different languages, of the cultivation of olives, or of music, necromancy, astronomy, of iron and copper work. While origins are a dominant theme of the text, the rubrics tend to focus on events and the names of people. Perhaps our reader stopped annotating the book when the theme he was most interested in and wanted to be able to locate quickly ceased to be so important? In any event, his annotations suggest an interest in history focussed on beginnings.</p><p>He also frequently marks places, either with \\u2018nota\\u2019 signs, or with glosses like \\u2018d[e]la yla d[e] xpre\\u2019 (f. 16v) or \\u2018no[ta]: d[e]la ploblacjio d[e]la jla d[e] rod[e]s\\u2019 (f. 85v) (which incidentally contain several characteristically Catalan forms). Some of the places he picks out are biblical, but the majority are Eastern Mediterranean and are not mentioned in rubrics. Thus our Catalan friend also approached the\\u00a0<i>Histoire ancienne\\u00a0</i>with a cultural geography of the Mediterranean in mind. It is probably coincidental that two of his annotations concern Rhodes (see also f. 18r), but the prevalence of places in the Eastern Mediterranean that are picked out by glosses may support Zinelli\\u2019s suggestion that the annotations were made there.\\u00a0</p>"}, {"type": "image_and_caption", "value": {"images": 19, "caption": "<p>BnF f.fr. 20125, f. 18r. The reference to Rhodes is the second in the left margin. Source: Gallica.BnF.fr.</p>"}}, {"type": "paragraph", "value": "<p>That this Catalan speaker (aka our man in Rhodes?) was reading and reacting to a book written in French to satisfy his interest in history is of course vital to our project. If he was (quite rightly) told off for defacing the book, we at least are grateful to him for doing so!</p><p>Simon Gaunt</p>"}]
30	[{"type": "paragraph", "value": "<p>For Horace poets had either to be useful (<i>prodesse</i>) or to delight (<i>delectare</i>). The\\u00a0<i>Histoire ancienne jusqu\\u2019\\u00e0 C\\u00e9sar</i>, our object of study, fulfils both objectives. On the one hand, the\\u00a0<i>HA</i>\\u00a0conveys serious, edifying accounts of how crucial events for humanity took place (the creation, the flood, the foundation of Troy, Rome, Paris): in this respect, the\\u00a0<i>HA</i>\\u00a0is \\u2018history\\u2019 providing the audience with useful knowledge. On the other hand, the\\u00a0<i>HA</i>\\u00a0presents a showcase of the most delectable stories on the market: the tales that everybody had heard of or wanted to know about. How did the angel stop the arm of Abraham on the verge of killing Isaac, his beloved son? How was Rome founded? How about the story of the twins, Romulus and Remus? And, of course, what happened between Eneas and Dido? Did he really leave her on the shores of Carthage? Did she kill herself without his knowing so that he might not feel regret or shame? (Needless to say the anonymous redactor of the\\u00a0<i>HA</i>fuelled Eneas\\u2019 bad press, well-deserved according to many).</p><p>We all know how attractive gruesome stories can be. There are tales we always return to\\u2013\\u2013no matter how many times we hear them and no matter how violent they are. The legend of Oedipus is one of these stories. Not\\u00a0<i>a</i>\\u00a0tragedy, of course, but rather\\u00a0<i>the</i>\\u00a0tragedy. This story, part of the Theban saga, works so well that it is invariably successful in fascinating us with its bloodthirsty and vicious little charm: even when narrated in medieval French, in the thirteenth century, on the basis of some obscure as yet unidentified source, which in turn reworked the first- and second-century Latin versions of the Theban myth (Seneca and Statius), which in turn had rewritten the drama that crystallised in its most famous version (for us), the one that penned by Sophocles in Pericles\\u2019 Athens (fifth century BC).</p>"}, {"type": "image_and_caption", "value": {"images": 35, "caption": "<p>The brief retelling of the Oedipus story in the\\u00a0<i>HA</i>\\u00a0is often richly illustrated, with particular attention paid to two key episodes in Oedipus\\u2019s tragic trajectory: his childhood exposure and his encounter with the sphinx. Two-compartment miniature of Laius and Jocasta (above) and Oedipus hanging from a tree (below), from Paris, BnF, f. fr. 20125, f. 88v. Source:\\u00a0<a href=\\"http://gallica.bnf.fr/\\">Gallica.BnF.fr</a>.</p>"}}, {"type": "paragraph", "value": "<p>The redactor of the\\u00a0<i>HA</i>\\u00a0was aware of Oedipus\\u2019s fate, yet provided his own version of the story, peculiar both in terms of plot development and in tone. One crucial moment in the tragedy illustrates this: Oedipus\\u2019s murder of Laius, his father. The red title or \\u2018rubric\\u2019 of the passage in Paris, BnF, f. fr. 20125 summarises the episode as follows: \\u2018Que Edippus quist respons a Apollin qui estoit ses peres et coment il l\\u2019ocist\\u2019 (f. 90va) (How Oedipus consulted (the oracle of) Apollo about whom his father was, and how he killed him).</p><p>As we all remember, Oedipus, having discovered he is not the son of the king Polybus, leaves to look for his parents. The oracle tells him he will find out if he goes to Thebes. On his way to Thebes, however, Oedipus arrives at the city of Daulis, in the Greek region of Phocis\\u2013\\u2013the castle of \\u2018Phoce\\u2019 in the French text. According to the\\u00a0<i>HA</i>, Oedipus stops at the outskirts of the city to attend some jousts. Unfortunately, a terrible fight breaks out. Misfortune after misfortune, Oedipus finds himself crushed by the mob against the city gates. Precisely at this point, Laius, the king of Thebes, who was also there to watch, comes out of the gates and is killed by Oedipus in rather opaque circumstances. No account of the murderous fight over who had right of way at the crossroad near Daulis. Famously, Oedipus kills Laius, and then encounters the sphinx, before finally getting to Thebes.</p>"}, {"type": "image_and_caption", "value": {"images": 25, "caption": "<p>Oedipus encounters the sphinx, from\\u00a0<a href=\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Add_MS_15268\\">London, British Library,\\u00a0Add. 15268</a>, f. 77v.\\u00a0Reproduced with the permission of the British Library Board.</p>"}}, {"type": "paragraph", "value": "<p>According to the French narrator, Oedipus kills his father in a chaotic general mel\\u00e9e not in an individual encounter. This means that the trigger for the tragic fate of Oedipus and that of his lineage is quite different. This final gloss on how Oedipus actually killed his father is not without irony:</p><p><i>Teus ia qui dient qu\\u2019il l\\u2019ocist au clore dou flael de la porte, [et] teus i a que dient de s\\u2019espee. Or vos en tenes au quel que uos voudres, mes ensi fu mors li rois de Thebes, mes ne sot nus de ses gens qui cil estoit qui l\\u2019avoit mort, quar tost se refu Edippus mis entre les autres.\\u00a0(Paris, BnF, fr. 20125, f. 91ra)</i></p><p>(Some people say that he (Oedipus) killed his father while the doors (of the city) were closing down [literally: while the bar was locking down the doors of the city], and some others say he did it with his sword. Now, you choose whichever you like, thus the king of Thebes was killed, and no one among the king\\u2019s people knew who killed him, as Oedipus quickly returned to the crowd.)</p><p>The narrator here seems humorously to give up: unable to provide a consistent report of the facts, he leaves the decision to his audience. It is then up to us to decide whether Oedipus killed his father brandishing a sword, as a coldblooded but noble murderer, or as a vulgar hooligan who allowed his father to die ridiculously, crushed by the heavy gates of\\u00a0<i>Phoce</i>.</p><p>Simone Ventura</p>"}]
\.


--
-- TOC entry 2318 (class 0 OID 409942)
-- Dependencies: 193
-- Data for Name: cms_homepage; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY cms_homepage (page_ptr_id, content) FROM stdin;
3	[{"type": "image_and_caption", "value": {"images": 63, "caption": "<p>Miniature of Noah and the ark, from London, British Library, Add. 15268, f. 7v. Reproduced with the permission of the British Library Board.</p>"}}, {"type": "paragraph", "value": "<p><em>The Values of French Language and Literature in the European Middle Ages</em>\\u00a0is a five-year research project running from 2015 to 2020 in the Department of French at King\\u2019s College London, funded by the European Research Council within the framework of an Advanced Grant.<em>The Values of French</em>\\u00a0examines the nature and value of the use of French in Europe during a crucial period, 1100-1450, less in terms of its cultural prestige (the traditional focus of scholarship) than of its role as a supralocal, transnational language, particularly in Western Europe and the Eastern Mediterranean. The project fosters collaboration between, and cuts across, different intellectual and national scholarly traditions, drawing on expertise in codicology, critical theory, linguistics, literature, and philology; it involves scholars from a range of European countries and North America, entailing empirical research around a complex and widely disseminated textual tradition vital to medieval understandings of European history and identity,\\u00a0<em>L\\u2019Histoire ancienne jusqu\\u2019\\u00e0 C\\u00e9sar</em>. This case study grounds and stimulates broader speculative reflection on two questions concerning linguistic identity. What is the relation historically between language and identity in Europe? How are cognate languages demarcated from each other? Indeed, its final aim, through and beyond its consideration of French as a\\u00a0<em>lingua franca</em>, is to interrogate that language\\u2019s role in the emergence of a European identity in the Middle Ages. To:\\u00a0<a href=\\"http://www.tvof.ac.uk/values-french/\\">More about the project</a></p>"}]
\.


--
-- TOC entry 2320 (class 0 OID 409965)
-- Dependencies: 195
-- Data for Name: cms_indexpage; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY cms_indexpage (page_ptr_id, content) FROM stdin;
10	[{"type": "paragraph", "value": "<p>An integral part of the project is an international seminar that meets in London three times a year to discuss the project findings and engage with\\u00a0<em>The Value of French</em>\\u2019s\\u00a0<a href=\\"http://www.tvof.ac.uk/more-about-project/\\">main objectives</a>.</p>"}, {"type": "image_and_text", "value": {"text": "<p><b>Seminar 1</b></p><p>18th and 19th March 2016</p><p><b>Seminar 2</b></p><p>24th and 25th June 2016</p><p><b>Seminar 3</b></p><p>16th and 17th December 2016</p>", "image": 59, "alignment": "right", "caption": "<p>Miniature of the Temple of Janus with senators dining, from London, British Library, Add. 15268, f. 242v. Reproduced with the permission of the British Library Board.</p>"}}]
19	[{"type": "paragraph", "value": "<p><b>Upcoming Events</b></p><p><b>11 May 2016</b></p><p><b><a href=\\"https://www.literatur.hu-berlin.de/de/events/einladung-zum-gastvortrag-simon-gaunt-110516prof-joerg-kreienbrock-020516\\">Simon Gaunt, 'Manuscripts as Agents: The\\u00a0<i>Histoire ancienne jusqu'\\u00e0 C\\u00e9sar</i>'</a></b><br/>Institut f\\u00fcr deutsche Literatur<br/>Humboldt-Universit\\u00e4t, Berlin</p>"}, {"type": "image", "value": 34}, {"type": "image_and_caption", "value": {"images": 56, "caption": "<p><i>Miniature of the Wheel of Fortune, from London, British Library, Royal 20 D I, f. 168v. Reproduced with the permission of the British Library Board.</i></p>"}}]
5	[{"type": "paragraph", "value": "<p><em>The Values of French Language and Literature in the European Middle Ages</em>\\u00a0is a five-year research project running from 2015 to 2020 in the Department of French at King\\u2019s College London, funded by the European Research Council within the framework of an Advanced Grant.\\u00a0</p><p><em>The Values of French</em>\\u00a0examines the nature and value of the use of French in Europe during a crucial period, 1100-1450, less in terms of its cultural prestige (the traditional focus of scholarship) than of its role as a supralocal, transnational language, particularly in Western Europe and the Eastern Mediterranean.</p><p>The project fosters collaboration between, and cuts across, different intellectual and national scholarly traditions, drawing on expertise in codicology, critical theory, linguistics, literature, and philology; it involves scholars from a range of European countries and North America, entailing empirical research around a complex and widely disseminated textual tradition vital to medieval understandings of European history and identity,\\u00a0<em>L'Histoire ancienne jusqu'\\u00e0 C\\u00e9sar</em>.</p>"}, {"type": "image_and_text", "value": {"text": "This case study grounds and stimulates broader speculative reflection on two questions concerning linguistic identity. What is the relation historically between language and identity in Europe? How are cognate languages demarcated from each other? Indeed, its final aim, through and beyond its consideration of French as a\\u00a0<em>lingua franca</em>, is to interrogate that language's role in the emergence of a European identity in the Middle Ages.\\u00a0<p></p><p></p><p>To:\\u00a0<a href=\\"http://www.tvof.ac.uk/more-about-project/\\">More about the project</a></p>", "image": 28, "alignment": "right", "caption": "<p>Miniature of the construction of Rome, from London, British Library, Add. 15268, f. 156r. Reproduced with the permission of the British Library Board.</p>"}}]
9	[{"type": "paragraph", "value": "<p>The main objectives of\\u00a0<em>The Values of French\\u00a0</em>are:</p><p></p><ol><li>To develop a better understanding of the values of the use of French as a transnational and supralocal language in the Middle Ages (1100-1450).</li><li>To investigate the role that French played in the emergence of a European, transnational and supralocal identity (as opposed to a specific French national identity) at a crucial point in history (i.e. 1100-1450).</li><li>To conduct empirical research on a sizeable body of under-researched material that is central to the writing of European history in the Middle Ages, the so-called\\u00a0<em>Histoire ancienne jusqu\\u2019\\u00e0 C\\u00e9sar</em>, in order to make this material available digitally.</li><li>To engage in more speculative, theoretical, and genuinely interdisciplinary enquiry about the contours of individual languages and linguistic definition, using medieval French as a case study.</li><li>To engage in more speculative, theoretical, and interdisciplinary enquiry about the nature of the \\u2018literary\\u2019 and its relation to the conception and practice of historical writing.</li></ol>"}, {"type": "image_and_caption", "value": {"images": 42, "caption": "<p>Illustration of the voyage of the Cretans and battle between the Cretans and Athenians, from London, British Library, Royal 20 D I, f. 21v. Reproduced with the permission of the British Library Board.</p>"}}]
\.


--
-- TOC entry 2319 (class 0 OID 409952)
-- Dependencies: 194
-- Data for Name: cms_richtextpage; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY cms_richtextpage (page_ptr_id, content) FROM stdin;
22	[{"type": "image_and_text", "value": {"text": "<p>The extensive and complex manuscript transmission\\u00a0<em>L\\u2019Histoire ancienne jusqu\\u2019\\u00e0 C\\u00e9sar\\u00a0</em>will be the focus here, both because of its origin and wide dissemination outside France and because of its centrality to the diffusion of ideas about European history and identity. The aim here, on the one hand, is to produce digital editions of hitherto unedited but widely disseminated material that was highly influential for Western Europe\\u2019s construction of its own past from the mid-thirteenth century through to the mid-fifteenth; on the other hand, to reflect upon method. How does a consideration of language and geography impact upon our understanding of a text\\u2019s evolution through time and how in turn does this affect how we choose to edit a text? We will produce digital editions of two key manuscripts of the text:\\u00a0<a href=\\"http://gallica.bnf.fr/ark:/12148/btv1b52505677c.r=20125\\">Biblioth\\u00e8que nationale de France, f. fr. 20125</a>, possibly made in Acre in the second half of the thirteenth century and one of the earliest surviving witnesses, and\\u00a0<a href=\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Royal_MS_20_D_I\\">British Library,\\u00a0Royal 20 D I</a>, the earliest manuscript of the so-called second redaction made in Naples in the early fourteenth-century. Both manuscripts contain large amounts of hitherto unedited material written in non-standard forms of French. We will also edit a third manuscript we are still in the process of selecting. Lead:\\u00a0<a href=\\"http://www.tvof.ac.uk/values-french/project-team/\\">Hannah Morcos</a>.</p><p><br/></p><p>To:\\u00a0<a href=\\"http://www.tvof.ac.uk/more-about-project/history-and-literature-middle-ages/\\">History and literature in the Middle Ages</a><br/></p>", "image": 55, "alignment": "right", "caption": "<p>Miniature of the sack of Troy, from London, British Library, Royal 20 D I, f. 169r. Reproduced with the permission of the British Library Board.</p>"}}]
21	[{"type": "image_and_text", "value": {"text": "<p>How useful is it to think of French as \\u2018a language\\u2019 in the Middle Ages? Or are we dealing rather with a set of mutually intelligible\\u00a0<em>koines</em>, of which \\u2018standard\\u2019 French from France was but one?\\u00a0 Who used this language or these idioms now known as French? Were there norms and if so how did they arise? If not, how might this be accounted for in our understanding of medieval texts written in French? Lead:\\u00a0<a href=\\"http://www.tvof.ac.uk/values-french/project-team/\\">Simone Ventura</a></p><p></p><p><br/></p><p>To:\\u00a0<a href=\\"http://www.tvof.ac.uk/more-about-project/editions-histoire-ancienne-jusqu-cesar/\\">Editions of the\\u00a0<i>Histoire ancienne jusqu\\u2019\\u00e0 C\\u00e9sar</i></a></p>", "image": 44, "alignment": "right", "caption": "<p>Miniature of Jason and the Argonauts, from London, British Library, Add. 15268, f. 105v. Reproduced with the permission of the British Library Board.</p>"}}]
6	[{"type": "paragraph", "value": "<p><a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/gaunt/index.aspx\\">Simon Gaunt</a>\\u00a0(Principal Investigator) is Professor of French Language and Literature at King\\u2019s College London where he has previously been Head of the Department of French and Head of the School of Arts and Humanities. His most recent books are\\u00a0<em>Marco Polo\\u2019s</em>\\u00a0Le Devisement du Monde:\\u00a0<em>Narrative Voice, Language and Diversity</em>\\u00a0(2013),\\u00a0<em>The Cambridge Companion to Medieval French Literature</em>\\u00a0(2008), which he edited with Sarah Kay, and\\u00a0<em>Martyrs to Love: Love and Death in Medieval French and Occitan Courtly Literature</em>\\u00a0(2006). He was previously PI on the AHRC-funded project\\u00a0<a href=\\"http://mflc-stg.cch.kcl.ac.uk/\\"><em>Medieval Francophone Literary Culture outside France</em></a>.</p><p><a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/morcosh.aspx\\">Hannah Morcos</a>\\u00a0completed her PhD thesis at King\\u2019s College London. Her research on the compilation and reception of medieval francophone story collections in multi-text codices formed part of the cross-European Hera-funded project\\u00a0<a href=\\"http://dynamicsofthemedievalmanuscript.eu/\\"><i>The Dynamics of the Medieval Manuscript: Text Collections from a European Perspective</i></a>. After completing her PhD, she worked in the British Library\\u2019s Section of Ancient, Medieval and Early Modern Manuscripts\\u00a0as post-graduate intern. Her research interests centre on medieval French literature and manuscript studies.</p><p><a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/rachettamt.aspx\\">Maria Teresa Rachetta</a>\\u00a0obtained her PhD at the University of Rome \\u2018La Sapienza\\u2019 in 2015. She also studied at the University of Paris 4 \\u2018Sorbonne\\u2019 and at the University of Cambridge and was research fellow at the\\u00a0<em>Istituto Italiano per gli Studi Storici</em>\\u00a0in Naples. She specialises in Romance languages and literatures from 1100 to 1400. Her approach is interdisciplinary, centred on textual criticism, but also making use of linguistics and literary theory, with an interest too in cultural history. Her research has focussed particularly on Old French prose historiography and Biblical verse adaptations, as well as on sermons, verse romances, and lyric poetry in French and Occitan.</p><p><a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/venturas.aspx\\">Simone Ventura</a>\\u00a0specialises in Romance languages and literatures (esp. Catalan, French, Italian, Occitan) from 1100 to 1500. His work ranges across linguistics, manuscript studies, digital humanities, and the broad field of comparative literary studies, including translation studies. His publications are mainly in the following areas: troubadour lyric; medieval Latin and vernacular grammaticography and rhetoric; medieval encyclopaedic texts in translation; Boccaccio and translations of Boccaccio\\u2019s works. Dr Ventura\\u2019s most recent publications include two books on the manuscript tradition of the lyric of the troubadours and on vernacular encyclopaedism, and various contributions on Boccaccio.</p>"}, {"type": "image_and_caption", "value": {"images": 30, "caption": "<p>Miniature of the construction of Rome, from London, British Library, Add. 15268, f. 156r. Reproduced with the permission of the British Library Board.</p>"}}]
7	[{"type": "paragraph", "value": "<p><a href=\\"http://www.kcl.ac.uk/artshums/digitallab/index.aspx\\">King's Digital Laboratory</a>\\u00a0</p>"}, {"type": "image_and_text", "value": {"text": "<p><i><a href=\\"http://www.medievalfrancophone.ac.uk/\\">Medieval Francophone Literary Culture Outside France</a>\\u00a0</i></p><p><i><br/></i></p><p>Full colour digitisations of manuscripts containing the\\u00a0<i>Histoire ancienne jusqu'\\u00e0 C\\u00e9sar</i>:<i>\\u00a0\\u00a0</i></p><p><a href=\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Add_MS_15268\\">London, British Library, Additional 15268</a></p><p><a href=\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Add_MS_19669\\">London, British Library, Additional 19669</a></p><p><a href=\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Royal_MS_20_D_I\\">London, British Library, Royal 20 D I</a></p><p><a href=\\"http://gallica.bnf.fr/ark:/12148/btv1b52505677c.r=20125\\">Paris, Biblioth\\u00e8que nationale de France, f. fr. 20125</a>\\u00a0</p><p><a href=\\"http://data.onb.ac.at/rec/AL00167906#\\">Vienna, \\u00d6sterreichische Nationalbibliothek, Cod. 2576</a></p>", "image": 61, "alignment": "right", "caption": "<p>Miniature of Theseus attacking Crete, from London, British Library, Add. 15268, f.136v. Reproduced with the permission of the British Library Board.</p>"}}]
8	[{"type": "image_and_text", "value": {"text": "<p>Professor Simon Gaunt</p>Department of French<br/>King's College London<br/>Room 4.35 Virginia Woolf Building<br/>22 Kingsway<br/>London WC2B 6LE<p></p><p></p><p><a href=\\"mailto:simon.gaunt@kcl.ac.uk\\">simon.gaunt@kcl.ac.uk</a>\\u00a0</p><p>You can also find us on\\u00a0<a href=\\"https://www.facebook.com/thevaluesoffrench/?ref=hl\\">Facebook</a>\\u00a0and\\u00a0<a href=\\"https://twitter.com/ValuesOfFrench\\">Twitter</a>.</p>", "image": 46, "alignment": "right", "caption": "<p>Miniature of Jason, the Greeks and Trojans, from London, British Library, Add. 19669, f. 77r. Reproduced with the permission of the British Library Board.</p>"}}]
23	[{"type": "paragraph", "value": "<p>Our third seam will be a theoretical reflection on literary history, in particular on the question of genre and of our understanding of the literary. Much of the textual material transmitted in French outside France (such as the\\u00a0<em>Histoire ancienne jusqu\\u2019\\u00e0 C\\u00e9sar</em>) can only loosely be considered \\u2018literary\\u2019 according to modern understandings of the term, yet this material resembles more \\u2018literary\\u2019 material closely\\u2014both stylistically and linguistically\\u2014and has much to tell us about European cultural identity, concerned as it is with the foundation and history of Europe as both a cultural and a political entity. While modern understandings of the \\u2018literary\\u2019 and \\u2018genre\\u2019 are often anachronistic, how is literary history affected once we consider the vast body of material in French that has not been deemed \\u2018great literature\\u2019 in the modern period? More particularly: how useful are the generic categories of modern scholarship for understanding this material, and, if they turn out not to be useful, what other categories can we deploy in their place?</p>"}, {"type": "image_and_text", "value": {"text": "Lead:\\u00a0<a href=\\"http://www.tvof.ac.uk/values-french/project-team/\\">Maria Teresa Rachetta</a>.<p></p><p>To:\\u00a0<a href=\\"http://www.tvof.ac.uk/more-about-project/\\">More about the project</a></p>", "image": 60, "alignment": "right", "caption": "<p>Miniature of Theseus and the Giant, from London, British Library, Royal 20 D I, f. 26r. Reproduced with the permission of the British Library Board.</p>"}}]
24	[{"type": "paragraph", "value": "<p><em>The Values of French</em>\\u00a0will organise two international conferences to be held in London in 2018 and 2019.</p>"}, {"type": "image_and_caption", "value": {"images": 29, "caption": "<p>Historiated initial with 7 medallions depicting Creation, from London, British Library, Add. 19669, f. 4r. Reproduced with the permission of the British Library Board.</p>"}}]
25	[{"type": "paragraph", "value": "<p>Apart from the project team, the members of this seminar are as follows:</p>"}, {"type": "image_and_text", "value": {"text": "<p><a href=\\"http://www.unige.ch/lettres/mela/enseignant/philologie/barbieri/\\">Luca Barbieri</a>\\u00a0(Geneva)</p><p><a href=\\"http://unimap.unipi.it/cercapersone/dettaglio.php?ri=4049\\">Fabrizio Cigni</a>\\u00a0(Pisa)</p><p><a href=\\"http://www.deaf-page.de/fr/sd.php\\">Stephen D\\u00f6rr</a>\\u00a0(Heidelberg)</p><p><a href=\\"http://french.as.nyu.edu/object/sarahkay.html\\">Sarah Kay</a>\\u00a0(NYU)</p><p><a href=\\"https://kclpure.kcl.ac.uk/portal/en/persons/matt-lampitt(6408c45a-e418-4820-9d44-3d7a2518b5b8).html\\">Matthew Lampitt</a>\\u00a0(King's College London)</p><p><a href=\\"http://www.mml.cam.ac.uk/anl21\\">Adam Ledgeway</a>\\u00a0(Cambridge)</p><p><a href=\\"http://www.columbia.edu/cu/french/department/fac_bios/lefevre.htm\\">Sylvie Lef\\u00e8vre</a>\\u00a0(Paris 4/Sorbonne)</p><p><a href=\\"http://www.dfclam.unisi.it/it/dipartimento/persone/docenti/leonardi-lino\\">Lino Leonardi</a>\\u00a0(Florence/Sienna)</p><p><a href=\\"http://www.bbk.ac.uk/linguistics/our-staff/academic-staff/marjorie-lorch\\">Marjorie Lorch</a>\\u00a0(Birkbeck)</p><p><a href=\\"http://users.ox.ac.uk/~fmml0059/Site/About_Me.html\\">Sophie Marnette</a>\\u00a0(Oxford)</p><p><a href=\\"https://www.docenti.unina.it/laura.minervini\\">Laura Minervini</a>\\u00a0(Naples)</p><p><a href=\\"http://web.philo.ulg.ac.be/transitions/nicola-morato/\\">Nicola Morato</a>\\u00a0(Li\\u00e8ge)</p><p><a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/mortonj.aspx\\">Jonathan Morton</a>\\u00a0(King\\u2019s College London)</p><p><a href=\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/samuelsonc.aspx\\">Charles Samuelson</a>\\u00a0(King\\u2019s College London)</p><p><a href=\\"https://lettres.unifr.ch/fr/langues-litteratures/francais/collaborateurs/marion-vuagnoux-uhlig.html\\">Marion Uhlig</a>\\u00a0(Fribourg)</p><p><a href=\\"http://saprat.ephe.sorbonne.fr/enseignants-chercheurs/fabio-zinelli-68.htm\\">Fabio Zinelli</a>\\u00a0(Paris)</p>", "image": 50, "alignment": "right", "caption": "<p>Miniature of Noah and the ark, from London, British Library, Add. 15268, f. 7v. Reproduced with the permission of the British Library Board.</p>"}}]
\.


--
-- TOC entry 2310 (class 0 OID 409696)
-- Dependencies: 178
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- TOC entry 2303 (class 0 OID 409582)
-- Dependencies: 164
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	wagtailcore	page
2	cms	homepage
3	wagtailadmin	admin
4	wagtaildocs	document
5	wagtailimages	image
6	wagtailforms	formsubmission
7	wagtailredirects	redirect
8	wagtailembeds	embed
9	wagtailusers	userprofile
10	wagtailimages	filter
11	wagtailimages	rendition
12	wagtailsearch	query
13	wagtailsearch	querydailyhits
14	wagtailcore	site
15	wagtailcore	pagerevision
16	wagtailcore	grouppagepermission
17	wagtailcore	pageviewrestriction
18	wagtailcore	collection
19	wagtailcore	groupcollectionpermission
20	taggit	tag
21	taggit	taggeditem
22	admin	logentry
23	auth	permission
24	auth	group
25	auth	user
26	contenttypes	contenttype
27	sessions	session
28	cms	indexpage
29	cms	richtextpage
30	cms	blogindexpage
31	cms	blogpost
\.


--
-- TOC entry 2302 (class 0 OID 409571)
-- Dependencies: 162
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2016-05-16 11:49:07.274117+01
2	auth	0001_initial	2016-05-16 11:49:07.491638+01
3	admin	0001_initial	2016-05-16 11:49:07.553772+01
4	admin	0002_logentry_remove_auto_add	2016-05-16 11:49:07.594348+01
5	contenttypes	0002_remove_content_type_name	2016-05-16 11:49:07.674235+01
6	auth	0002_alter_permission_name_max_length	2016-05-16 11:49:07.725455+01
7	auth	0003_alter_user_email_max_length	2016-05-16 11:49:07.795648+01
8	auth	0004_alter_user_username_opts	2016-05-16 11:49:07.826571+01
9	auth	0005_alter_user_last_login_null	2016-05-16 11:49:07.86549+01
10	auth	0006_require_contenttypes_0002	2016-05-16 11:49:07.878162+01
11	auth	0007_alter_validators_add_error_messages	2016-05-16 11:49:07.906109+01
12	wagtailcore	0001_initial	2016-05-16 11:49:08.398565+01
13	wagtailcore	0002_initial_data	2016-05-16 11:49:08.4101+01
14	wagtailcore	0003_add_uniqueness_constraint_on_group_page_permission	2016-05-16 11:49:08.421455+01
15	wagtailcore	0004_page_locked	2016-05-16 11:49:08.432691+01
16	wagtailcore	0005_add_page_lock_permission_to_moderators	2016-05-16 11:49:08.444266+01
17	wagtailcore	0006_add_lock_page_permission	2016-05-16 11:49:08.454231+01
18	wagtailcore	0007_page_latest_revision_created_at	2016-05-16 11:49:08.464186+01
19	wagtailcore	0008_populate_latest_revision_created_at	2016-05-16 11:49:08.47469+01
20	wagtailcore	0009_remove_auto_now_add_from_pagerevision_created_at	2016-05-16 11:49:08.48609+01
21	wagtailcore	0010_change_page_owner_to_null_on_delete	2016-05-16 11:49:08.499274+01
22	wagtailcore	0011_page_first_published_at	2016-05-16 11:49:08.509835+01
23	wagtailcore	0012_extend_page_slug_field	2016-05-16 11:49:08.521364+01
24	wagtailcore	0013_update_golive_expire_help_text	2016-05-16 11:49:08.531913+01
25	wagtailcore	0014_add_verbose_name	2016-05-16 11:49:08.542484+01
26	wagtailcore	0015_add_more_verbose_names	2016-05-16 11:49:08.556085+01
27	wagtailcore	0016_change_page_url_path_to_text_field	2016-05-16 11:49:08.566649+01
28	wagtailcore	0017_change_edit_page_permission_description	2016-05-16 11:49:08.598476+01
29	wagtailcore	0018_pagerevision_submitted_for_moderation_index	2016-05-16 11:49:08.644476+01
30	wagtailcore	0019_verbose_names_cleanup	2016-05-16 11:49:08.761377+01
31	wagtailcore	0020_add_index_on_page_first_published_at	2016-05-16 11:49:08.814833+01
32	wagtailcore	0021_capitalizeverbose	2016-05-16 11:49:09.712659+01
33	wagtailcore	0022_add_site_name	2016-05-16 11:49:09.779553+01
34	wagtailcore	0023_alter_page_revision_on_delete_behaviour	2016-05-16 11:49:09.855332+01
35	wagtailcore	0024_collection	2016-05-16 11:49:09.899207+01
36	wagtailcore	0025_collection_initial_data	2016-05-16 11:49:09.928813+01
37	wagtailcore	0026_group_collection_permission	2016-05-16 11:49:10.040503+01
38	wagtailcore	0027_fix_collection_path_collation	2016-05-16 11:49:10.072404+01
39	wagtailcore	0024_alter_page_content_type_on_delete_behaviour	2016-05-16 11:49:10.144354+01
40	wagtailcore	0028_merge	2016-05-16 11:49:10.156762+01
41	cms	0001_initial	2016-05-16 11:49:10.210888+01
42	cms	0002_create_homepage	2016-05-16 11:49:10.283042+01
43	cms	0003_richtextpage	2016-05-16 11:49:10.360596+01
44	cms	0004_auto_20160511_1440	2016-05-16 11:49:10.460061+01
45	cms	0005_blogindexpage_blogpost	2016-05-16 11:49:10.557283+01
46	sessions	0001_initial	2016-05-16 11:49:10.606395+01
47	taggit	0001_initial	2016-05-16 11:49:10.73348+01
48	taggit	0002_auto_20150616_2121	2016-05-16 11:49:10.804595+01
49	wagtailadmin	0001_create_admin_access_permissions	2016-05-16 11:49:10.913607+01
50	wagtaildocs	0001_initial	2016-05-16 11:49:10.978658+01
51	wagtaildocs	0002_initial_data	2016-05-16 11:49:11.073124+01
52	wagtaildocs	0003_add_verbose_names	2016-05-16 11:49:11.225688+01
53	wagtaildocs	0004_capitalizeverbose	2016-05-16 11:49:11.47745+01
54	wagtaildocs	0005_document_collection	2016-05-16 11:49:11.546931+01
55	wagtaildocs	0006_copy_document_permissions_to_collections	2016-05-16 11:49:11.598249+01
56	wagtaildocs	0005_alter_uploaded_by_user_on_delete_action	2016-05-16 11:49:11.705224+01
57	wagtaildocs	0007_merge	2016-05-16 11:49:11.717572+01
58	wagtailembeds	0001_initial	2016-05-16 11:49:11.767787+01
59	wagtailembeds	0002_add_verbose_names	2016-05-16 11:49:11.78849+01
60	wagtailembeds	0003_capitalizeverbose	2016-05-16 11:49:11.80665+01
61	wagtailforms	0001_initial	2016-05-16 11:49:11.896163+01
62	wagtailforms	0002_add_verbose_names	2016-05-16 11:49:11.98077+01
63	wagtailforms	0003_capitalizeverbose	2016-05-16 11:49:12.07585+01
64	wagtailimages	0001_initial	2016-05-16 11:49:12.353601+01
65	wagtailimages	0002_initial_data	2016-05-16 11:49:12.432907+01
66	wagtailimages	0003_fix_focal_point_fields	2016-05-16 11:49:12.596765+01
67	wagtailimages	0004_make_focal_point_key_not_nullable	2016-05-16 11:49:12.678278+01
68	wagtailimages	0005_make_filter_spec_unique	2016-05-16 11:49:12.787662+01
69	wagtailimages	0006_add_verbose_names	2016-05-16 11:49:13.096813+01
70	wagtailimages	0007_image_file_size	2016-05-16 11:49:13.154988+01
71	wagtailimages	0008_image_created_at_index	2016-05-16 11:49:13.232762+01
72	wagtailimages	0009_capitalizeverbose	2016-05-16 11:49:13.55597+01
73	wagtailimages	0010_change_on_delete_behaviour	2016-05-16 11:49:13.645712+01
74	wagtailimages	0011_image_collection	2016-05-16 11:49:13.735668+01
75	wagtailimages	0012_copy_image_permissions_to_collections	2016-05-16 11:49:13.790097+01
76	wagtailredirects	0001_initial	2016-05-16 11:49:13.889885+01
77	wagtailredirects	0002_add_verbose_names	2016-05-16 11:49:14.044346+01
78	wagtailredirects	0003_make_site_field_editable	2016-05-16 11:49:14.163919+01
79	wagtailredirects	0004_set_unique_on_path_and_site	2016-05-16 11:49:14.30425+01
80	wagtailredirects	0005_capitalizeverbose	2016-05-16 11:49:14.723174+01
81	wagtailsearch	0001_initial	2016-05-16 11:49:14.951922+01
82	wagtailsearch	0002_add_verbose_names	2016-05-16 11:49:15.191642+01
83	wagtailsearch	0003_remove_editors_pick	2016-05-16 11:49:15.254686+01
84	wagtailusers	0001_initial	2016-05-16 11:49:15.346151+01
85	wagtailusers	0002_add_verbose_name_on_userprofile	2016-05-16 11:49:15.492077+01
86	wagtailusers	0003_add_verbose_names	2016-05-16 11:49:15.549145+01
87	wagtailusers	0004_capitalizeverbose	2016-05-16 11:49:15.740761+01
88	wagtailcore	0001_squashed_0016_change_page_url_path_to_text_field	2016-05-16 11:49:15.758559+01
89	cms	0006_auto_20160518_1259	2016-05-18 12:59:09.1846+01
90	cms	0007_auto_20160526_1544	2016-05-26 15:44:59.829881+01
91	cms	0008_auto_20160526_1617	2016-05-26 16:17:13.425172+01
\.


--
-- TOC entry 2323 (class 0 OID 409998)
-- Dependencies: 198
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
o1g51zl4b3jzapb80arzzzqrsuzqp4dq	NzYxNjMzOTNlNTNlODUwNWI3MDBmZTViNmU0NGI5NWIxN2M2M2RmNjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk3NDMzZjAzMWYyZGE5NjU3Y2ExMWVlYWI5YzllMzYzOTg2NWZkMTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2016-05-30 11:55:16.525846+01
t3s34av3xyvh23123w7cw1aoj80jgruu	NzYxNjMzOTNlNTNlODUwNWI3MDBmZTViNmU0NGI5NWIxN2M2M2RmNjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk3NDMzZjAzMWYyZGE5NjU3Y2ExMWVlYWI5YzllMzYzOTg2NWZkMTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2016-05-31 13:16:35.70221+01
vp2js0m3dsucolxmhjikem4fm9ylukq9	NzYxNjMzOTNlNTNlODUwNWI3MDBmZTViNmU0NGI5NWIxN2M2M2RmNjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk3NDMzZjAzMWYyZGE5NjU3Y2ExMWVlYWI5YzllMzYzOTg2NWZkMTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2016-06-01 16:29:52.247682+01
ygcd5ze8j2fnfhzt793fae9nnuh8dzvn	NDA0ZDE2ZTdkOGE5MWFmMDhjMzZlMmZlNDFhMWQ3NDMzYWU5ZWI0NTp7Il9hdXRoX3VzZXJfaGFzaCI6ImJiZDIwM2NkN2U2YjI4Zjk1YWMwMmI1MjRkYjc4MDU0NjY4OTEzYTAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=	2016-06-07 17:38:39.473085+01
o5niq4ednwgdc7rz934zh26jug2mwkvg	NDA0ZDE2ZTdkOGE5MWFmMDhjMzZlMmZlNDFhMWQ3NDMzYWU5ZWI0NTp7Il9hdXRoX3VzZXJfaGFzaCI6ImJiZDIwM2NkN2U2YjI4Zjk1YWMwMmI1MjRkYjc4MDU0NjY4OTEzYTAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=	2016-06-09 15:24:05.747868+01
q2tcl18xtbvufzv80u0uguw3bufkss5m	NzYxNjMzOTNlNTNlODUwNWI3MDBmZTViNmU0NGI5NWIxN2M2M2RmNjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk3NDMzZjAzMWYyZGE5NjU3Y2ExMWVlYWI5YzllMzYzOTg2NWZkMTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2016-06-30 12:28:12.839346+01
\.


--
-- TOC entry 2324 (class 0 OID 410010)
-- Dependencies: 200
-- Data for Name: taggit_tag; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY taggit_tag (id, name, slug) FROM stdin;
\.


--
-- TOC entry 2325 (class 0 OID 410022)
-- Dependencies: 202
-- Data for Name: taggit_taggeditem; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY taggit_taggeditem (id, object_id, content_type_id, tag_id) FROM stdin;
\.


--
-- TOC entry 2316 (class 0 OID 409892)
-- Dependencies: 190
-- Data for Name: wagtailcore_collection; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailcore_collection (id, path, depth, numchild, name) FROM stdin;
1	0001	1	0	Root
\.


--
-- TOC entry 2317 (class 0 OID 409908)
-- Dependencies: 192
-- Data for Name: wagtailcore_groupcollectionpermission; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailcore_groupcollectionpermission (id, collection_id, group_id, permission_id) FROM stdin;
1	1	1	2
2	1	2	2
3	1	1	3
4	1	2	3
5	1	1	5
6	1	2	5
7	1	1	6
8	1	2	6
\.


--
-- TOC entry 2312 (class 0 OID 409750)
-- Dependencies: 182
-- Data for Name: wagtailcore_grouppagepermission; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailcore_grouppagepermission (id, permission_type, group_id, page_id) FROM stdin;
1	add	1	1
2	edit	1	1
3	publish	1	1
4	add	2	1
5	edit	2	1
6	lock	1	1
\.


--
-- TOC entry 2311 (class 0 OID 409733)
-- Dependencies: 180
-- Data for Name: wagtailcore_page; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailcore_page (id, path, depth, numchild, title, slug, live, has_unpublished_changes, url_path, seo_title, show_in_menus, search_description, go_live_at, expire_at, expired, content_type_id, owner_id, locked, latest_revision_created_at, first_published_at) FROM stdin;
1	0001	1	1	Root	root	t	f	/		f		\N	\N	f	1	\N	f	\N	\N
23	0001000100020003	4	0	History and literature in the Middle Ages	history-and-literature-middle-ages	t	f	/home/more-about-project/history-and-literature-middle-ages/		f		\N	\N	f	29	1	f	2016-05-24 14:54:08.208695+01	2016-05-24 14:54:08.24894+01
5	000100010001	3	3	The Values of French	values-french	t	f	/home/values-french/		t		\N	\N	f	28	1	f	2016-05-23 15:10:13.437236+01	2016-05-16 11:58:35.883388+01
9	000100010002	3	4	More about the project	more-about-project	t	f	/home/more-about-project/		t		\N	\N	f	28	1	f	2016-05-24 14:50:22.425163+01	2016-05-16 12:02:01.573575+01
21	0001000100020001	4	0	The nature of French in the Middle Ages	nature-french-middle-ages	t	f	/home/more-about-project/nature-french-middle-ages/		f		\N	\N	f	29	1	f	2016-05-26 15:37:57.465454+01	2016-05-24 14:50:57.744998+01
24	0001000100020004	4	0	Conferences	conferences	t	f	/home/more-about-project/conferences/		f		\N	\N	f	29	1	f	2016-05-24 14:56:24.348662+01	2016-05-24 14:56:24.367918+01
6	0001000100010001	4	0	The project team	project-team	t	f	/home/values-french/project-team/		f		\N	\N	f	29	1	f	2016-05-24 09:42:14.621617+01	2016-05-16 12:00:10.980576+01
25	0001000100030001	4	0	Seminar members	seminar-members	t	f	/home/project-seminar/seminar-members/		f		\N	\N	f	29	1	f	2016-05-24 14:57:42.108047+01	2016-05-24 14:57:42.127777+01
7	0001000100010002	4	0	Project partners and links	project-partners-and-links	t	f	/home/values-french/project-partners-and-links/		f		\N	\N	f	29	1	f	2016-05-24 14:46:19.504043+01	2016-05-16 12:00:32.373833+01
10	000100010003	3	1	The project seminar	project-seminar	t	f	/home/project-seminar/		t		\N	\N	f	28	1	f	2016-05-24 14:58:55.581526+01	2016-05-16 12:16:58.611552+01
8	0001000100010003	4	0	Contact	contact	t	f	/home/values-french/contact/		f		\N	\N	f	29	1	f	2016-05-24 14:47:40.11232+01	2016-05-16 12:00:44.007551+01
15	000100010005	3	3	Blog	blog	t	f	/home/blog/		f		\N	\N	f	30	1	f	2016-05-18 12:51:10.996258+01	2016-05-18 12:51:11.06143+01
19	000100010004	3	0	Events	events	t	f	/home/events/		t		\N	\N	f	28	1	f	2016-05-24 15:01:22.463409+01	2016-05-18 16:10:33.175341+01
30	0001000100050003	4	0	‘Uns rois estoit adonques en Thebes’ –– Once upon a time there was a king in Thebes, or the (morbid) pleasure of storytelling	uns-rois-estoit-adonques-en-thebes-once-upon-time-there-was-king-thebes-or-morbid-pleasure-storytelling	t	f	/home/blog/uns-rois-estoit-adonques-en-thebes-once-upon-time-there-was-king-thebes-or-morbid-pleasure-storytelling/		f		\N	\N	f	31	4	f	2016-05-24 15:16:18.602053+01	2016-05-24 15:16:18.628948+01
22	0001000100020002	4	0	Editions of the Histoire ancienne jusqu’à César	editions-histoire-ancienne-jusqu-cesar	t	f	/home/more-about-project/editions-histoire-ancienne-jusqu-cesar/		f		\N	\N	f	29	1	f	2016-05-24 14:52:55.003991+01	2016-05-24 14:52:55.025041+01
29	0001000100050002	4	0	Our Catalan friend	our-catalan-friend	t	f	/home/blog/our-catalan-friend/		f		\N	\N	f	31	3	f	2016-05-24 15:13:07.916148+01	2016-05-24 15:13:07.938553+01
26	0001000100060001	4	0	Meet our new team member	meet-our-new-team-member	t	f	/home/news/meet-our-new-team-member/		f		\N	\N	f	31	1	f	2016-05-24 15:03:16.274504+01	2016-05-24 15:03:16.295988+01
20	000100010006	3	2	News	news	t	f	/home/news/		f		\N	\N	f	30	1	f	2016-05-18 16:12:00.261031+01	2016-05-18 16:12:00.33936+01
28	0001000100050001	4	0	Jacob’s speckled flock, miscegenation and the dangers of female desire	jacobs-speckled-flock-miscegenation-and-dangers-female-desire	t	f	/home/blog/jacobs-speckled-flock-miscegenation-and-dangers-female-desire/		f		\N	\N	f	31	2	f	2016-05-24 15:09:04.087805+01	2016-05-24 15:09:04.108808+01
27	0001000100060002	4	0	PhD Studentship	phd-studentship	t	f	/home/news/phd-studentship/		f		\N	\N	f	31	1	f	2016-05-24 15:05:00.468002+01	2016-05-24 15:05:00.487264+01
3	00010001	2	6	Home	home	t	f	/home/		f		\N	\N	f	2	\N	f	2016-05-26 16:20:06.234769+01	2016-05-16 11:57:08.87772+01
\.


--
-- TOC entry 2313 (class 0 OID 409760)
-- Dependencies: 184
-- Data for Name: wagtailcore_pagerevision; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailcore_pagerevision (id, submitted_for_moderation, created_at, content_json, approved_go_live_at, page_id, user_id) FROM stdin;
5	f	2016-05-16 12:00:10.899671+01	{"locked": false, "title": "The project team", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 29, "path": "0001000100010001", "owner": 1, "pk": 6, "first_published_at": null, "url_path": "/home/values-french/project-team/", "expired": false, "slug": "project-team", "expire_at": null, "go_live_at": null}	\N	6	1
2	f	2016-05-16 11:57:08.823328+01	{"locked": false, "title": "Home", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "search_description": "", "depth": 2, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 2, "path": "00010001", "owner": null, "pk": 3, "first_published_at": null, "url_path": "/home/", "expired": false, "slug": "home", "expire_at": null, "go_live_at": null}	\N	3	1
3	f	2016-05-16 11:58:35.821153+01	{"locked": false, "title": "The Values of French", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[]", "search_description": "", "depth": 3, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 28, "path": "000100010001", "owner": 1, "pk": 5, "first_published_at": null, "url_path": "/home/values-french/", "expired": false, "slug": "values-french", "expire_at": null, "go_live_at": null}	\N	5	1
4	f	2016-05-16 11:59:17.313194+01	{"locked": false, "title": "The Values of French", "numchild": 0, "show_in_menus": true, "live": true, "seo_title": "", "content": "[]", "search_description": "", "depth": 3, "latest_revision_created_at": "2016-05-16T10:58:35.821Z", "has_unpublished_changes": false, "content_type": 28, "path": "000100010001", "owner": 1, "pk": 5, "first_published_at": "2016-05-16T10:58:35.883Z", "url_path": "/home/values-french/", "expired": false, "slug": "values-french", "expire_at": null, "go_live_at": null}	\N	5	1
10	f	2016-05-16 12:02:27.769316+01	{"locked": false, "title": "More about the project", "numchild": 0, "show_in_menus": true, "live": true, "seo_title": "", "content": "[]", "search_description": "", "depth": 3, "latest_revision_created_at": "2016-05-16T11:02:01.499Z", "has_unpublished_changes": false, "content_type": 28, "path": "000100010002", "owner": 1, "pk": 9, "first_published_at": "2016-05-16T11:02:01.573Z", "url_path": "/home/more-about-project/", "expired": false, "slug": "more-about-project", "expire_at": null, "go_live_at": null}	\N	9	1
6	f	2016-05-16 12:00:32.31185+01	{"locked": false, "title": "Project partners and links", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 29, "path": "0001000100010002", "owner": 1, "pk": 7, "first_published_at": null, "url_path": "/home/values-french/project-partners-and-links/", "expired": false, "slug": "project-partners-and-links", "expire_at": null, "go_live_at": null}	\N	7	1
9	f	2016-05-16 12:02:01.499888+01	{"locked": false, "title": "More about the project", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[]", "search_description": "", "depth": 3, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 28, "path": "000100010002", "owner": 1, "pk": 9, "first_published_at": null, "url_path": "/home/more-about-project/", "expired": false, "slug": "more-about-project", "expire_at": null, "go_live_at": null}	\N	9	1
11	f	2016-05-16 12:16:58.54242+01	{"locked": false, "title": "The project seminar", "numchild": 0, "show_in_menus": true, "live": true, "seo_title": "", "content": "[]", "search_description": "", "depth": 3, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 28, "path": "000100010003", "owner": 1, "pk": 10, "first_published_at": null, "url_path": "/home/project-seminar/", "expired": false, "slug": "project-seminar", "expire_at": null, "go_live_at": null}	\N	10	1
7	f	2016-05-16 12:00:43.927387+01	{"locked": false, "title": "Contant", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 29, "path": "0001000100010003", "owner": 1, "pk": 8, "first_published_at": null, "url_path": "/home/values-french/contant/", "expired": false, "slug": "contant", "expire_at": null, "go_live_at": null}	\N	8	1
8	f	2016-05-16 12:01:23.918902+01	{"locked": false, "title": "Contact", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[]", "search_description": "", "depth": 4, "latest_revision_created_at": "2016-05-16T11:00:43.927Z", "has_unpublished_changes": false, "content_type": 29, "path": "0001000100010003", "owner": 1, "pk": 8, "first_published_at": "2016-05-16T11:00:44.007Z", "url_path": "/home/values-french/contant/", "expired": false, "slug": "contact", "expire_at": null, "go_live_at": null}	\N	8	1
19	f	2016-05-18 12:51:10.996258+01	{"locked": false, "title": "Blog", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "search_description": "", "depth": 3, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 30, "path": "000100010004", "owner": 1, "pk": 15, "first_published_at": null, "url_path": "/home/blog/", "expired": false, "slug": "blog", "expire_at": null, "go_live_at": null}	\N	15	1
35	f	2016-05-24 14:49:45.364018+01	{"locked": false, "title": "More about the project", "numchild": 0, "show_in_menus": true, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>The main objectives of\\\\u00a0<em>The Values of French\\\\u00a0</em>are:</p><p></p><ol><li>To develop a better understanding of the values of the use of French as a transnational and supralocal language in the Middle Ages (1100-1450).</li><li>To investigate the role that French played in the emergence of a European, transnational and supralocal identity (as opposed to a specific French national identity) at a crucial point in history (i.e. 1100-1450).</li><li>To conduct empirical research on a sizeable body of under-researched material that is central to the writing of European history in the Middle Ages, the so-called\\\\u00a0<em>Histoire ancienne jusqu\\\\u2019\\\\u00e0 C\\\\u00e9sar</em>, in order to make this material available digitally.</li><li>To engage in more speculative, theoretical, and genuinely interdisciplinary enquiry about the contours of individual languages and linguistic definition, using medieval French as a case study.</li><li>To engage in more speculative, theoretical, and interdisciplinary enquiry about the nature of the \\\\u2018literary\\\\u2019 and its relation to the conception and practice of historical writing.</li></ol>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 53, \\"caption\\": \\"<p>Illustration of the voyage of the Cretans and battle between the Cretans and Athenians, from London, British Library, Royal 20 D I, f. 21v. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 3, "latest_revision_created_at": "2016-05-16T11:02:27.769Z", "has_unpublished_changes": false, "content_type": 28, "path": "000100010002", "owner": 1, "pk": 9, "first_published_at": "2016-05-16T11:02:01.573Z", "url_path": "/home/more-about-project/", "expired": false, "slug": "more-about-project", "expire_at": null, "go_live_at": null}	\N	9	1
25	f	2016-05-18 16:10:33.081641+01	{"locked": false, "title": "Events", "numchild": 0, "show_in_menus": true, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"heading\\", \\"value\\": \\"Placeholder\\"}]", "search_description": "", "depth": 3, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 28, "path": "000100010005", "owner": 1, "pk": 19, "first_published_at": null, "url_path": "/home/events/", "expired": false, "slug": "events", "expire_at": null, "go_live_at": null}	\N	19	1
26	f	2016-05-18 16:12:00.261031+01	{"locked": false, "title": "News", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "search_description": "", "depth": 3, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 30, "path": "000100010006", "owner": 1, "pk": 20, "first_published_at": null, "url_path": "/home/news/", "expired": false, "slug": "news", "expire_at": null, "go_live_at": null}	\N	20	1
27	f	2016-05-23 15:09:45.894359+01	{"locked": false, "title": "The Values of French", "numchild": 3, "show_in_menus": true, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><em>The Values of French Language and Literature in the European Middle Ages</em>\\\\u00a0is a five-year research project running from 2015 to 2020 in the Department of French at King\\\\u2019s College London, funded by the European Research Council within the framework of an Advanced Grant.\\\\u00a0</p><p><em>The Values of French</em>\\\\u00a0examines the nature and value of the use of French in Europe during a crucial period, 1100-1450, less in terms of its cultural prestige (the traditional focus of scholarship) than of its role as a supralocal, transnational language, particularly in Western Europe and the Eastern Mediterranean.</p><p>The project fosters collaboration between, and cuts across, different intellectual and national scholarly traditions, drawing on expertise in codicology, critical theory, linguistics, literature, and philology; it involves scholars from a range of European countries and North America, entailing empirical research around a complex and widely disseminated textual tradition vital to medieval understandings of European history and identity,\\\\u00a0<em>L'Histoire ancienne jusqu'\\\\u00e0 C\\\\u00e9sar</em>.</p>\\"}, {\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"This case study grounds and stimulates broader speculative reflection on two questions concerning linguistic identity. What is the relation historically between language and identity in Europe? How are cognate languages demarcated from each other? Indeed, its final aim, through and beyond its consideration of French as a\\\\u00a0<em>lingua franca</em>, is to interrogate that language's role in the emergence of a European identity in the Middle Ages.\\\\u00a0<p></p><p></p><p>To:\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/more-about-project/\\\\\\">More about the project</a></p>\\", \\"image\\": 28, \\"alignment\\": \\"left\\", \\"caption\\": \\"<p>Miniature of the construction of Rome, from London, British Library, Add. 15268, f. 156r. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 3, "latest_revision_created_at": "2016-05-16T10:59:17.313Z", "has_unpublished_changes": false, "content_type": 28, "path": "000100010001", "owner": 1, "pk": 5, "first_published_at": "2016-05-16T10:58:35.883Z", "url_path": "/home/values-french/", "expired": false, "slug": "values-french", "expire_at": null, "go_live_at": null}	\N	5	1
28	f	2016-05-23 15:10:13.437236+01	{"locked": false, "title": "The Values of French", "numchild": 3, "show_in_menus": true, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><em>The Values of French Language and Literature in the European Middle Ages</em>\\\\u00a0is a five-year research project running from 2015 to 2020 in the Department of French at King\\\\u2019s College London, funded by the European Research Council within the framework of an Advanced Grant.\\\\u00a0</p><p><em>The Values of French</em>\\\\u00a0examines the nature and value of the use of French in Europe during a crucial period, 1100-1450, less in terms of its cultural prestige (the traditional focus of scholarship) than of its role as a supralocal, transnational language, particularly in Western Europe and the Eastern Mediterranean.</p><p>The project fosters collaboration between, and cuts across, different intellectual and national scholarly traditions, drawing on expertise in codicology, critical theory, linguistics, literature, and philology; it involves scholars from a range of European countries and North America, entailing empirical research around a complex and widely disseminated textual tradition vital to medieval understandings of European history and identity,\\\\u00a0<em>L'Histoire ancienne jusqu'\\\\u00e0 C\\\\u00e9sar</em>.</p>\\"}, {\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"This case study grounds and stimulates broader speculative reflection on two questions concerning linguistic identity. What is the relation historically between language and identity in Europe? How are cognate languages demarcated from each other? Indeed, its final aim, through and beyond its consideration of French as a\\\\u00a0<em>lingua franca</em>, is to interrogate that language's role in the emergence of a European identity in the Middle Ages.\\\\u00a0<p></p><p></p><p>To:\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/more-about-project/\\\\\\">More about the project</a></p>\\", \\"image\\": 28, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Miniature of the construction of Rome, from London, British Library, Add. 15268, f. 156r. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 3, "latest_revision_created_at": "2016-05-23T14:09:45.894Z", "has_unpublished_changes": false, "content_type": 28, "path": "000100010001", "owner": 1, "pk": 5, "first_published_at": "2016-05-16T10:58:35.883Z", "url_path": "/home/values-french/", "expired": false, "slug": "values-french", "expire_at": null, "go_live_at": null}	\N	5	1
29	f	2016-05-23 15:18:22.440909+01	{"locked": false, "title": "The project team", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/gaunt/index.aspx\\\\\\">Simon Gaunt</a>\\\\u00a0(Principal Investigator) is Professor of French Language and Literature at King\\\\u2019s College London where he has previously been Head of the Department of French and Head of the School of Arts and Humanities. His most recent books are\\\\u00a0<em>Marco Polo\\\\u2019s</em>\\\\u00a0Le Devisement du Monde:\\\\u00a0<em>Narrative Voice, Language and Diversity</em>\\\\u00a0(2013),\\\\u00a0<em>The Cambridge Companion to Medieval French Literature</em>\\\\u00a0(2008), which he edited with Sarah Kay, and\\\\u00a0<em>Martyrs to Love: Love and Death in Medieval French and Occitan Courtly Literature</em>\\\\u00a0(2006). He was previously PI on the AHRC-funded project\\\\u00a0<a href=\\\\\\"http://mflc-stg.cch.kcl.ac.uk/\\\\\\"><em>Medieval Francophone Literary Culture outside France</em></a>.</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/morcosh.aspx\\\\\\">Hannah Morcos</a>\\\\u00a0completed her PhD thesis at King\\\\u2019s College London. Her research on the compilation and reception of medieval francophone story collections in multi-text codices formed part of the cross-European Hera-funded project\\\\u00a0<a href=\\\\\\"http://dynamicsofthemedievalmanuscript.eu/\\\\\\"><i>The Dynamics of the Medieval Manuscript: Text Collections from a European Perspective</i></a>. After completing her PhD, she worked in the British Library\\\\u2019s Section of Ancient, Medieval and Early Modern Manuscripts\\\\u00a0as post-graduate intern. Her research interests centre on medieval French literature and manuscript studies.</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/rachettamt.aspx\\\\\\">Maria Teresa Rachetta</a>\\\\u00a0obtained her PhD at the University of Rome \\\\u2018La Sapienza\\\\u2019 in 2015. She also studied at the University of Paris 4 \\\\u2018Sorbonne\\\\u2019 and at the University of Cambridge and was research fellow at the\\\\u00a0<em>Istituto Italiano per gli Studi Storici</em>\\\\u00a0in Naples. She specialises in Romance languages and literatures from 1100 to 1400. Her approach is interdisciplinary, centred on textual criticism, but also making use of linguistics and literary theory, with an interest too in cultural history. Her research has focussed particularly on Old French prose historiography and Biblical verse adaptations, as well as on sermons, verse romances, and lyric poetry in French and Occitan.</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/venturas.aspx\\\\\\">Simone Ventura</a>\\\\u00a0specialises in Romance languages and literatures (esp. Catalan, French, Italian, Occitan) from 1100 to 1500. His work ranges across linguistics, manuscript studies, digital humanities, and the broad field of comparative literary studies, including translation studies. His publications are mainly in the following areas: troubadour lyric; medieval Latin and vernacular grammaticography and rhetoric; medieval encyclopaedic texts in translation; Boccaccio and translations of Boccaccio\\\\u2019s works. Dr Ventura\\\\u2019s most recent publications include two books on the manuscript tradition of the lyric of the troubadours and on vernacular encyclopaedism, and various contributions on Boccaccio.</p>\\"}, {\\"type\\": \\"image\\", \\"value\\": 30}]", "search_description": "", "depth": 4, "latest_revision_created_at": "2016-05-16T11:00:10.899Z", "has_unpublished_changes": false, "content_type": 29, "path": "0001000100010001", "owner": 1, "pk": 6, "first_published_at": "2016-05-16T11:00:10.980Z", "url_path": "/home/values-french/project-team/", "expired": false, "slug": "project-team", "expire_at": null, "go_live_at": null}	\N	6	1
30	f	2016-05-23 15:19:53.198061+01	{"locked": false, "title": "The project team", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/gaunt/index.aspx\\\\\\">Simon Gaunt</a>\\\\u00a0(Principal Investigator) is Professor of French Language and Literature at King\\\\u2019s College London where he has previously been Head of the Department of French and Head of the School of Arts and Humanities. His most recent books are\\\\u00a0<em>Marco Polo\\\\u2019s</em>\\\\u00a0Le Devisement du Monde:\\\\u00a0<em>Narrative Voice, Language and Diversity</em>\\\\u00a0(2013),\\\\u00a0<em>The Cambridge Companion to Medieval French Literature</em>\\\\u00a0(2008), which he edited with Sarah Kay, and\\\\u00a0<em>Martyrs to Love: Love and Death in Medieval French and Occitan Courtly Literature</em>\\\\u00a0(2006). He was previously PI on the AHRC-funded project\\\\u00a0<a href=\\\\\\"http://mflc-stg.cch.kcl.ac.uk/\\\\\\"><em>Medieval Francophone Literary Culture outside France</em></a>.</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/morcosh.aspx\\\\\\">Hannah Morcos</a>\\\\u00a0completed her PhD thesis at King\\\\u2019s College London. Her research on the compilation and reception of medieval francophone story collections in multi-text codices formed part of the cross-European Hera-funded project\\\\u00a0<a href=\\\\\\"http://dynamicsofthemedievalmanuscript.eu/\\\\\\"><i>The Dynamics of the Medieval Manuscript: Text Collections from a European Perspective</i></a>. After completing her PhD, she worked in the British Library\\\\u2019s Section of Ancient, Medieval and Early Modern Manuscripts\\\\u00a0as post-graduate intern. Her research interests centre on medieval French literature and manuscript studies.</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/rachettamt.aspx\\\\\\">Maria Teresa Rachetta</a>\\\\u00a0obtained her PhD at the University of Rome \\\\u2018La Sapienza\\\\u2019 in 2015. She also studied at the University of Paris 4 \\\\u2018Sorbonne\\\\u2019 and at the University of Cambridge and was research fellow at the\\\\u00a0<em>Istituto Italiano per gli Studi Storici</em>\\\\u00a0in Naples. She specialises in Romance languages and literatures from 1100 to 1400. Her approach is interdisciplinary, centred on textual criticism, but also making use of linguistics and literary theory, with an interest too in cultural history. Her research has focussed particularly on Old French prose historiography and Biblical verse adaptations, as well as on sermons, verse romances, and lyric poetry in French and Occitan.</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/venturas.aspx\\\\\\">Simone Ventura</a>\\\\u00a0specialises in Romance languages and literatures (esp. Catalan, French, Italian, Occitan) from 1100 to 1500. His work ranges across linguistics, manuscript studies, digital humanities, and the broad field of comparative literary studies, including translation studies. His publications are mainly in the following areas: troubadour lyric; medieval Latin and vernacular grammaticography and rhetoric; medieval encyclopaedic texts in translation; Boccaccio and translations of Boccaccio\\\\u2019s works. Dr Ventura\\\\u2019s most recent publications include two books on the manuscript tradition of the lyric of the troubadours and on vernacular encyclopaedism, and various contributions on Boccaccio.</p>\\"}, {\\"type\\": \\"image\\", \\"value\\": 30}, {\\"type\\": \\"image_caption\\", \\"value\\": \\"Miniature of the construction of Rome, from London, British Library, Add. 15268, f. 156r. Reproduced with the permission of the British Library Board.\\"}]", "search_description": "", "depth": 4, "latest_revision_created_at": "2016-05-23T14:18:22.440Z", "has_unpublished_changes": false, "content_type": 29, "path": "0001000100010001", "owner": 1, "pk": 6, "first_published_at": "2016-05-16T11:00:10.980Z", "url_path": "/home/values-french/project-team/", "expired": false, "slug": "project-team", "expire_at": null, "go_live_at": null}	\N	6	1
31	f	2016-05-24 09:42:14.621617+01	{"locked": false, "title": "The project team", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/gaunt/index.aspx\\\\\\">Simon Gaunt</a>\\\\u00a0(Principal Investigator) is Professor of French Language and Literature at King\\\\u2019s College London where he has previously been Head of the Department of French and Head of the School of Arts and Humanities. His most recent books are\\\\u00a0<em>Marco Polo\\\\u2019s</em>\\\\u00a0Le Devisement du Monde:\\\\u00a0<em>Narrative Voice, Language and Diversity</em>\\\\u00a0(2013),\\\\u00a0<em>The Cambridge Companion to Medieval French Literature</em>\\\\u00a0(2008), which he edited with Sarah Kay, and\\\\u00a0<em>Martyrs to Love: Love and Death in Medieval French and Occitan Courtly Literature</em>\\\\u00a0(2006). He was previously PI on the AHRC-funded project\\\\u00a0<a href=\\\\\\"http://mflc-stg.cch.kcl.ac.uk/\\\\\\"><em>Medieval Francophone Literary Culture outside France</em></a>.</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/morcosh.aspx\\\\\\">Hannah Morcos</a>\\\\u00a0completed her PhD thesis at King\\\\u2019s College London. Her research on the compilation and reception of medieval francophone story collections in multi-text codices formed part of the cross-European Hera-funded project\\\\u00a0<a href=\\\\\\"http://dynamicsofthemedievalmanuscript.eu/\\\\\\"><i>The Dynamics of the Medieval Manuscript: Text Collections from a European Perspective</i></a>. After completing her PhD, she worked in the British Library\\\\u2019s Section of Ancient, Medieval and Early Modern Manuscripts\\\\u00a0as post-graduate intern. Her research interests centre on medieval French literature and manuscript studies.</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/rachettamt.aspx\\\\\\">Maria Teresa Rachetta</a>\\\\u00a0obtained her PhD at the University of Rome \\\\u2018La Sapienza\\\\u2019 in 2015. She also studied at the University of Paris 4 \\\\u2018Sorbonne\\\\u2019 and at the University of Cambridge and was research fellow at the\\\\u00a0<em>Istituto Italiano per gli Studi Storici</em>\\\\u00a0in Naples. She specialises in Romance languages and literatures from 1100 to 1400. Her approach is interdisciplinary, centred on textual criticism, but also making use of linguistics and literary theory, with an interest too in cultural history. Her research has focussed particularly on Old French prose historiography and Biblical verse adaptations, as well as on sermons, verse romances, and lyric poetry in French and Occitan.</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/venturas.aspx\\\\\\">Simone Ventura</a>\\\\u00a0specialises in Romance languages and literatures (esp. Catalan, French, Italian, Occitan) from 1100 to 1500. His work ranges across linguistics, manuscript studies, digital humanities, and the broad field of comparative literary studies, including translation studies. His publications are mainly in the following areas: troubadour lyric; medieval Latin and vernacular grammaticography and rhetoric; medieval encyclopaedic texts in translation; Boccaccio and translations of Boccaccio\\\\u2019s works. Dr Ventura\\\\u2019s most recent publications include two books on the manuscript tradition of the lyric of the troubadours and on vernacular encyclopaedism, and various contributions on Boccaccio.</p>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 30, \\"caption\\": \\"<p>Miniature of the construction of Rome, from London, British Library, Add. 15268, f. 156r. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": "2016-05-23T14:19:53.198Z", "has_unpublished_changes": false, "content_type": 29, "path": "0001000100010001", "owner": 1, "pk": 6, "first_published_at": "2016-05-16T11:00:10.980Z", "url_path": "/home/values-french/project-team/", "expired": false, "slug": "project-team", "expire_at": null, "go_live_at": null}	\N	6	1
32	f	2016-05-24 14:45:50.206715+01	{"locked": false, "title": "Project partners and links", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"<p><i><a href=\\\\\\"http://www.medievalfrancophone.ac.uk/\\\\\\">Medieval Francophone Literary Culture Outside France</a>\\\\u00a0</i></p><p><i><br/></i></p><p>Full colour digitisations of manuscripts containing the\\\\u00a0<i>Histoire ancienne jusqu'\\\\u00e0 C\\\\u00e9sar</i>:<i>\\\\u00a0\\\\u00a0</i></p><p><a href=\\\\\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Add_MS_15268\\\\\\">London, British Library, Additional 15268</a></p><p><a href=\\\\\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Add_MS_19669\\\\\\">London, British Library, Additional 19669</a></p><p><a href=\\\\\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Royal_MS_20_D_I\\\\\\">London, British Library, Royal 20 D I</a></p><p><a href=\\\\\\"http://gallica.bnf.fr/ark:/12148/btv1b52505677c.r=20125\\\\\\">Paris, Biblioth\\\\u00e8que nationale de France, f. fr. 20125</a>\\\\u00a0</p><p><a href=\\\\\\"http://data.onb.ac.at/rec/AL00167906#\\\\\\">Vienna, \\\\u00d6sterreichische Nationalbibliothek, Cod. 2576</a></p>\\", \\"image\\": 61, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Miniature of Theseus attacking Crete, from London, British Library, Add. 15268, f.136v. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": "2016-05-16T11:00:32.311Z", "has_unpublished_changes": false, "content_type": 29, "path": "0001000100010002", "owner": 1, "pk": 7, "first_published_at": "2016-05-16T11:00:32.373Z", "url_path": "/home/values-french/project-partners-and-links/", "expired": false, "slug": "project-partners-and-links", "expire_at": null, "go_live_at": null}	\N	7	1
33	f	2016-05-24 14:46:19.504043+01	{"locked": false, "title": "Project partners and links", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/digitallab/index.aspx\\\\\\">King's Digital Laboratory</a>\\\\u00a0</p>\\"}, {\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"<p><i><a href=\\\\\\"http://www.medievalfrancophone.ac.uk/\\\\\\">Medieval Francophone Literary Culture Outside France</a>\\\\u00a0</i></p><p><i><br/></i></p><p>Full colour digitisations of manuscripts containing the\\\\u00a0<i>Histoire ancienne jusqu'\\\\u00e0 C\\\\u00e9sar</i>:<i>\\\\u00a0\\\\u00a0</i></p><p><a href=\\\\\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Add_MS_15268\\\\\\">London, British Library, Additional 15268</a></p><p><a href=\\\\\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Add_MS_19669\\\\\\">London, British Library, Additional 19669</a></p><p><a href=\\\\\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Royal_MS_20_D_I\\\\\\">London, British Library, Royal 20 D I</a></p><p><a href=\\\\\\"http://gallica.bnf.fr/ark:/12148/btv1b52505677c.r=20125\\\\\\">Paris, Biblioth\\\\u00e8que nationale de France, f. fr. 20125</a>\\\\u00a0</p><p><a href=\\\\\\"http://data.onb.ac.at/rec/AL00167906#\\\\\\">Vienna, \\\\u00d6sterreichische Nationalbibliothek, Cod. 2576</a></p>\\", \\"image\\": 61, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Miniature of Theseus attacking Crete, from London, British Library, Add. 15268, f.136v. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": "2016-05-24T13:45:50.206Z", "has_unpublished_changes": false, "content_type": 29, "path": "0001000100010002", "owner": 1, "pk": 7, "first_published_at": "2016-05-16T11:00:32.373Z", "url_path": "/home/values-french/project-partners-and-links/", "expired": false, "slug": "project-partners-and-links", "expire_at": null, "go_live_at": null}	\N	7	1
34	f	2016-05-24 14:47:40.11232+01	{"locked": false, "title": "Contact", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"<p>Professor Simon Gaunt</p>Department of French<br/>King's College London<br/>Room 4.35 Virginia Woolf Building<br/>22 Kingsway<br/>London WC2B 6LE<p></p><p></p><p><a href=\\\\\\"mailto:simon.gaunt@kcl.ac.uk\\\\\\">simon.gaunt@kcl.ac.uk</a>\\\\u00a0</p><p>You can also find us on\\\\u00a0<a href=\\\\\\"https://www.facebook.com/thevaluesoffrench/?ref=hl\\\\\\">Facebook</a>\\\\u00a0and\\\\u00a0<a href=\\\\\\"https://twitter.com/ValuesOfFrench\\\\\\">Twitter</a>.</p>\\", \\"image\\": 46, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Miniature of Jason, the Greeks and Trojans, from London, British Library, Add. 19669, f. 77r. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": "2016-05-16T11:01:23.918Z", "has_unpublished_changes": false, "content_type": 29, "path": "0001000100010003", "owner": 1, "pk": 8, "first_published_at": "2016-05-16T11:00:44.007Z", "url_path": "/home/values-french/contact/", "expired": false, "slug": "contact", "expire_at": null, "go_live_at": null}	\N	8	1
36	f	2016-05-24 14:50:22.425163+01	{"locked": false, "title": "More about the project", "numchild": 0, "show_in_menus": true, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>The main objectives of\\\\u00a0<em>The Values of French\\\\u00a0</em>are:</p><p></p><ol><li>To develop a better understanding of the values of the use of French as a transnational and supralocal language in the Middle Ages (1100-1450).</li><li>To investigate the role that French played in the emergence of a European, transnational and supralocal identity (as opposed to a specific French national identity) at a crucial point in history (i.e. 1100-1450).</li><li>To conduct empirical research on a sizeable body of under-researched material that is central to the writing of European history in the Middle Ages, the so-called\\\\u00a0<em>Histoire ancienne jusqu\\\\u2019\\\\u00e0 C\\\\u00e9sar</em>, in order to make this material available digitally.</li><li>To engage in more speculative, theoretical, and genuinely interdisciplinary enquiry about the contours of individual languages and linguistic definition, using medieval French as a case study.</li><li>To engage in more speculative, theoretical, and interdisciplinary enquiry about the nature of the \\\\u2018literary\\\\u2019 and its relation to the conception and practice of historical writing.</li></ol>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 42, \\"caption\\": \\"<p>Illustration of the voyage of the Cretans and battle between the Cretans and Athenians, from London, British Library, Royal 20 D I, f. 21v. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 3, "latest_revision_created_at": "2016-05-24T13:49:45.364Z", "has_unpublished_changes": false, "content_type": 28, "path": "000100010002", "owner": 1, "pk": 9, "first_published_at": "2016-05-16T11:02:01.573Z", "url_path": "/home/more-about-project/", "expired": false, "slug": "more-about-project", "expire_at": null, "go_live_at": null}	\N	9	1
37	f	2016-05-24 14:50:57.72006+01	{"locked": false, "title": "The nature of French in the Middle Ages", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 29, "path": "0001000100020001", "owner": 1, "pk": 21, "first_published_at": null, "url_path": "/home/more-about-project/nature-french-middle-ages/", "expired": false, "slug": "nature-french-middle-ages", "expire_at": null, "go_live_at": null}	\N	21	1
38	f	2016-05-24 14:52:55.003991+01	{"locked": false, "title": "Editions of the Histoire ancienne jusqu\\u2019\\u00e0 C\\u00e9sar", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"<p>The extensive and complex manuscript transmission\\\\u00a0<em>L\\\\u2019Histoire ancienne jusqu\\\\u2019\\\\u00e0 C\\\\u00e9sar\\\\u00a0</em>will be the focus here, both because of its origin and wide dissemination outside France and because of its centrality to the diffusion of ideas about European history and identity. The aim here, on the one hand, is to produce digital editions of hitherto unedited but widely disseminated material that was highly influential for Western Europe\\\\u2019s construction of its own past from the mid-thirteenth century through to the mid-fifteenth; on the other hand, to reflect upon method. How does a consideration of language and geography impact upon our understanding of a text\\\\u2019s evolution through time and how in turn does this affect how we choose to edit a text? We will produce digital editions of two key manuscripts of the text:\\\\u00a0<a href=\\\\\\"http://gallica.bnf.fr/ark:/12148/btv1b52505677c.r=20125\\\\\\">Biblioth\\\\u00e8que nationale de France, f. fr. 20125</a>, possibly made in Acre in the second half of the thirteenth century and one of the earliest surviving witnesses, and\\\\u00a0<a href=\\\\\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Royal_MS_20_D_I\\\\\\">British Library,\\\\u00a0Royal 20 D I</a>, the earliest manuscript of the so-called second redaction made in Naples in the early fourteenth-century. Both manuscripts contain large amounts of hitherto unedited material written in non-standard forms of French. We will also edit a third manuscript we are still in the process of selecting. Lead:\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/values-french/project-team/\\\\\\">Hannah Morcos</a>.</p><p><br/></p><p>To:\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/more-about-project/history-and-literature-middle-ages/\\\\\\">History and literature in the Middle Ages</a><br/></p>\\", \\"image\\": 55, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Miniature of the sack of Troy, from London, British Library, Royal 20 D I, f. 169r. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 29, "path": "0001000100020002", "owner": 1, "pk": 22, "first_published_at": null, "url_path": "/home/more-about-project/editions-histoire-ancienne-jusqu-cesar/", "expired": false, "slug": "editions-histoire-ancienne-jusqu-cesar", "expire_at": null, "go_live_at": null}	\N	22	1
43	f	2016-05-24 15:00:32.987321+01	{"locked": false, "title": "Events", "numchild": 0, "show_in_menus": true, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"heading\\", \\"value\\": \\"Upcoming Events  11 May 2016  Simon Gaunt, 'Manuscripts as Agents: The Histoire ancienne jusqu'\\\\u00e0 C\\\\u00e9sar' Institut f\\\\u00fcr deutsche Literatur Humboldt-Universit\\\\u00e4t, Berlin\\"}, {\\"type\\": \\"image\\", \\"value\\": 34}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 56, \\"caption\\": \\"<p><i>Miniature of the Wheel of Fortune, from London, British Library, Royal 20 D I, f. 168v. Reproduced with the permission of the British Library Board.</i></p>\\"}}]", "search_description": "", "depth": 3, "latest_revision_created_at": "2016-05-18T15:10:33.081Z", "has_unpublished_changes": false, "content_type": 28, "path": "000100010004", "owner": 1, "pk": 19, "first_published_at": "2016-05-18T15:10:33.175Z", "url_path": "/home/events/", "expired": false, "slug": "events", "expire_at": null, "go_live_at": null}	\N	19	1
45	f	2016-05-24 15:01:22.463409+01	{"locked": false, "title": "Events", "numchild": 0, "show_in_menus": true, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><b>Upcoming Events</b></p><p><b>11 May 2016</b></p><p><b><a href=\\\\\\"https://www.literatur.hu-berlin.de/de/events/einladung-zum-gastvortrag-simon-gaunt-110516prof-joerg-kreienbrock-020516\\\\\\">Simon Gaunt, 'Manuscripts as Agents: The\\\\u00a0<i>Histoire ancienne jusqu'\\\\u00e0 C\\\\u00e9sar</i>'</a></b><br/>Institut f\\\\u00fcr deutsche Literatur<br/>Humboldt-Universit\\\\u00e4t, Berlin</p>\\"}, {\\"type\\": \\"image\\", \\"value\\": 34}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 56, \\"caption\\": \\"<p><i>Miniature of the Wheel of Fortune, from London, British Library, Royal 20 D I, f. 168v. Reproduced with the permission of the British Library Board.</i></p>\\"}}]", "search_description": "", "depth": 3, "latest_revision_created_at": "2016-05-24T14:01:06.123Z", "has_unpublished_changes": true, "content_type": 28, "path": "000100010004", "owner": 1, "pk": 19, "first_published_at": "2016-05-18T15:10:33.175Z", "url_path": "/home/events/", "expired": false, "slug": "events", "expire_at": null, "go_live_at": null}	\N	19	1
39	f	2016-05-24 14:54:08.208695+01	{"locked": false, "title": "History and literature in the Middle Ages", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>Our third seam will be a theoretical reflection on literary history, in particular on the question of genre and of our understanding of the literary. Much of the textual material transmitted in French outside France (such as the\\\\u00a0<em>Histoire ancienne jusqu\\\\u2019\\\\u00e0 C\\\\u00e9sar</em>) can only loosely be considered \\\\u2018literary\\\\u2019 according to modern understandings of the term, yet this material resembles more \\\\u2018literary\\\\u2019 material closely\\\\u2014both stylistically and linguistically\\\\u2014and has much to tell us about European cultural identity, concerned as it is with the foundation and history of Europe as both a cultural and a political entity. While modern understandings of the \\\\u2018literary\\\\u2019 and \\\\u2018genre\\\\u2019 are often anachronistic, how is literary history affected once we consider the vast body of material in French that has not been deemed \\\\u2018great literature\\\\u2019 in the modern period? More particularly: how useful are the generic categories of modern scholarship for understanding this material, and, if they turn out not to be useful, what other categories can we deploy in their place?</p>\\"}, {\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"Lead:\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/values-french/project-team/\\\\\\">Maria Teresa Rachetta</a>.<p></p><p>To:\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/more-about-project/\\\\\\">More about the project</a></p>\\", \\"image\\": 60, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Miniature of Theseus and the Giant, from London, British Library, Royal 20 D I, f. 26r. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 29, "path": "0001000100020003", "owner": 1, "pk": 23, "first_published_at": null, "url_path": "/home/more-about-project/history-and-literature-middle-ages/", "expired": false, "slug": "history-and-literature-middle-ages", "expire_at": null, "go_live_at": null}	\N	23	1
44	f	2016-05-24 15:01:06.123903+01	{"locked": false, "title": "Events", "numchild": 0, "show_in_menus": true, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"heading\\", \\"value\\": \\"Upcoming Events  11 May 2016  Simon Gaunt, 'Manuscripts as Agents: The Histoire ancienne jusqu'\\\\u00e0 C\\\\u00e9sar' Institut f\\\\u00fcr deutsche Literatur Humboldt-Universit\\\\u00e4t, Berlin\\"}, {\\"type\\": \\"image\\", \\"value\\": 34}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 56, \\"caption\\": \\"<p><i>Miniature of the Wheel of Fortune, from London, British Library, Royal 20 D I, f. 168v. Reproduced with the permission of the British Library Board.</i></p>\\"}}]", "search_description": "", "depth": 3, "latest_revision_created_at": "2016-05-24T14:00:32.987Z", "has_unpublished_changes": false, "content_type": 28, "path": "000100010004", "owner": 1, "pk": 19, "first_published_at": "2016-05-18T15:10:33.175Z", "url_path": "/home/events/", "expired": false, "slug": "events", "expire_at": null, "go_live_at": null}	\N	19	1
40	f	2016-05-24 14:56:24.348662+01	{"locked": false, "title": "Conferences", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><em>The Values of French</em>\\\\u00a0will organise two international conferences to be held in London in 2018 and 2019.</p>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 29, \\"caption\\": \\"<p>Historiated initial with 7 medallions depicting Creation, from London, British Library, Add. 19669, f. 4r. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 29, "path": "0001000100020004", "owner": 1, "pk": 24, "first_published_at": null, "url_path": "/home/more-about-project/conferences/", "expired": false, "slug": "conferences", "expire_at": null, "go_live_at": null}	\N	24	1
51	f	2016-05-26 15:37:57.465454+01	{"locked": false, "title": "The nature of French in the Middle Ages", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"<p>How useful is it to think of French as \\\\u2018a language\\\\u2019 in the Middle Ages? Or are we dealing rather with a set of mutually intelligible\\\\u00a0<em>koines</em>, of which \\\\u2018standard\\\\u2019 French from France was but one?\\\\u00a0 Who used this language or these idioms now known as French? Were there norms and if so how did they arise? If not, how might this be accounted for in our understanding of medieval texts written in French? Lead:\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/values-french/project-team/\\\\\\">Simone Ventura</a></p><p></p><p><br/></p><p>To:\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/more-about-project/editions-histoire-ancienne-jusqu-cesar/\\\\\\">Editions of the\\\\u00a0<i>Histoire ancienne jusqu\\\\u2019\\\\u00e0 C\\\\u00e9sar</i></a></p>\\", \\"image\\": 44, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Miniature of Jason and the Argonauts, from London, British Library, Add. 15268, f. 105v. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": "2016-05-24T13:50:57.720Z", "has_unpublished_changes": false, "content_type": 29, "path": "0001000100020001", "owner": 1, "pk": 21, "first_published_at": "2016-05-24T13:50:57.744Z", "url_path": "/home/more-about-project/nature-french-middle-ages/", "expired": false, "slug": "nature-french-middle-ages", "expire_at": null, "go_live_at": null}	\N	21	2
41	f	2016-05-24 14:57:42.108047+01	{"locked": false, "title": "Seminar members", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>Apart from the project team, the members of this seminar are as follows:</p>\\"}, {\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"<p><a href=\\\\\\"http://www.unige.ch/lettres/mela/enseignant/philologie/barbieri/\\\\\\">Luca Barbieri</a>\\\\u00a0(Geneva)</p><p><a href=\\\\\\"http://unimap.unipi.it/cercapersone/dettaglio.php?ri=4049\\\\\\">Fabrizio Cigni</a>\\\\u00a0(Pisa)</p><p><a href=\\\\\\"http://www.deaf-page.de/fr/sd.php\\\\\\">Stephen D\\\\u00f6rr</a>\\\\u00a0(Heidelberg)</p><p><a href=\\\\\\"http://french.as.nyu.edu/object/sarahkay.html\\\\\\">Sarah Kay</a>\\\\u00a0(NYU)</p><p><a href=\\\\\\"https://kclpure.kcl.ac.uk/portal/en/persons/matt-lampitt(6408c45a-e418-4820-9d44-3d7a2518b5b8).html\\\\\\">Matthew Lampitt</a>\\\\u00a0(King's College London)</p><p><a href=\\\\\\"http://www.mml.cam.ac.uk/anl21\\\\\\">Adam Ledgeway</a>\\\\u00a0(Cambridge)</p><p><a href=\\\\\\"http://www.columbia.edu/cu/french/department/fac_bios/lefevre.htm\\\\\\">Sylvie Lef\\\\u00e8vre</a>\\\\u00a0(Paris 4/Sorbonne)</p><p><a href=\\\\\\"http://www.dfclam.unisi.it/it/dipartimento/persone/docenti/leonardi-lino\\\\\\">Lino Leonardi</a>\\\\u00a0(Florence/Sienna)</p><p><a href=\\\\\\"http://www.bbk.ac.uk/linguistics/our-staff/academic-staff/marjorie-lorch\\\\\\">Marjorie Lorch</a>\\\\u00a0(Birkbeck)</p><p><a href=\\\\\\"http://users.ox.ac.uk/~fmml0059/Site/About_Me.html\\\\\\">Sophie Marnette</a>\\\\u00a0(Oxford)</p><p><a href=\\\\\\"https://www.docenti.unina.it/laura.minervini\\\\\\">Laura Minervini</a>\\\\u00a0(Naples)</p><p><a href=\\\\\\"http://web.philo.ulg.ac.be/transitions/nicola-morato/\\\\\\">Nicola Morato</a>\\\\u00a0(Li\\\\u00e8ge)</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/mortonj.aspx\\\\\\">Jonathan Morton</a>\\\\u00a0(King\\\\u2019s College London)</p><p><a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/samuelsonc.aspx\\\\\\">Charles Samuelson</a>\\\\u00a0(King\\\\u2019s College London)</p><p><a href=\\\\\\"https://lettres.unifr.ch/fr/langues-litteratures/francais/collaborateurs/marion-vuagnoux-uhlig.html\\\\\\">Marion Uhlig</a>\\\\u00a0(Fribourg)</p><p><a href=\\\\\\"http://saprat.ephe.sorbonne.fr/enseignants-chercheurs/fabio-zinelli-68.htm\\\\\\">Fabio Zinelli</a>\\\\u00a0(Paris)</p>\\", \\"image\\": 50, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Miniature of Noah and the ark, from London, British Library, Add. 15268, f. 7v. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 29, "path": "0001000100030001", "owner": 1, "pk": 25, "first_published_at": null, "url_path": "/home/project-seminar/seminar-members/", "expired": false, "slug": "seminar-members", "expire_at": null, "go_live_at": null}	\N	25	1
42	f	2016-05-24 14:58:55.581526+01	{"locked": false, "title": "The project seminar", "numchild": 1, "show_in_menus": true, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>An integral part of the project is an international seminar that meets in London three times a year to discuss the project findings and engage with\\\\u00a0<em>The Value of French</em>\\\\u2019s\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/more-about-project/\\\\\\">main objectives</a>.</p>\\"}, {\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"<p><b>Seminar 1</b></p><p>18th and 19th March 2016</p><p><b>Seminar 2</b></p><p>24th and 25th June 2016</p><p><b>Seminar 3</b></p><p>16th and 17th December 2016</p>\\", \\"image\\": 59, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Miniature of the Temple of Janus with senators dining, from London, British Library, Add. 15268, f. 242v. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 3, "latest_revision_created_at": "2016-05-16T11:16:58.542Z", "has_unpublished_changes": false, "content_type": 28, "path": "000100010003", "owner": 1, "pk": 10, "first_published_at": "2016-05-16T11:16:58.611Z", "url_path": "/home/project-seminar/", "expired": false, "slug": "project-seminar", "expire_at": null, "go_live_at": null}	\N	10	1
46	f	2016-05-24 15:03:16.274504+01	{"locked": false, "title": "Meet our new team member", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>We are delighted to announce that we have appointed Henry Ravenhall as the project\\\\u2019s PhD student. Henry was selected from a strong field of applicants, and we thank all those who took the time to apply.</p><p>Henry discusses his research interests and PhD proposal below.</p><p>\\\\u2018I completed a BA in French and History at KCL in 2015, focussing on late antique and medieval history. My undergraduate dissertation concerned a piece of medieval Latin historiography entitled\\\\u00a0<i>Historia Comitum Ghisnensium</i>\\\\u00a0(\\\\u2018History of the Counts of Guines\\\\u2019) in which by applying a quantitative approach I sought to ascertain how descriptions of character (\\\\u2018being\\\\u2019) and conduct (\\\\u2018doing\\\\u2019) changed according to the historical chronology presented within the text. I have therefore been very much interested in applying linguistic methods to answer historical questions.\\\\u00a0I am currently studying for an MA in French Literature and Culture also at KCL, which I will complete in September 2016. I am also taking bi-weekly classes in Latin and have been attending palaeography sessions. I have become increasingly interested in how medieval languages interact and develop over time, particularly in relation to processes of vernacularisation.\\\\u00a0</p>\\"}, {\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"<p>My research proposal essentially seeks to question the divide between \\\\u2018Fiction\\\\u2019 and \\\\u2018History\\\\u2019 that as modern readers we impose upon medieval texts. Our simplistic attribution of these categories appears to belie contemporary consideration of the texts. It is my belief that we should attempt to identify firstly whether these categories can be kept at all, and secondly, if they are indeed problematic, what we may use to take their place. I\\\\u2019d like to ask: What can manuscript dissemination and compilation tell us about how medieval authors and audiences conceived of their texts? How does the choice of language (in regard to the local context) affect the textual discourse? What can notions of orality and spoken-ness communicate about how texts were initially formed and then received? And then, perhaps most crucially: how static or fluid are any such generic distinctions and how may they have changed over time and space in Europe between 1100\\\\u20131450?\\\\u2019</p>\\", \\"image\\": 41, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Henry Ravenhall</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 31, "path": "0001000100060001", "owner": 1, "pk": 26, "first_published_at": null, "url_path": "/home/news/meet-our-new-team-member/", "expired": false, "slug": "meet-our-new-team-member", "expire_at": null, "go_live_at": null}	\N	26	1
47	f	2016-05-24 15:05:00.468002+01	{"locked": false, "title": "PhD Studentship", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><em>The Values of French Language and Literature in the European Middle Ages</em>\\\\u00a0is pleased to announce one three-year fully-funded PhD studentship, to begin on 1 September 2016 and to be held in the Department of French at King\\\\u2019s College London. The student\\\\u2019s primary supervisor will be Professor\\\\u00a0<a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/gaunt/index.aspx\\\\\\">Simon Gaunt</a>, with Dr\\\\u00a0<a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/venturas.aspx\\\\\\">Simone Ventura</a>\\\\u00a0as secondary supervisor.</p><p>The studentship will pay home/EU fees (currently \\\\u00a34,600) and a maintenance allowance equivalent to an AHRC studentship (currently \\\\u00a316,057). Applicants are expected to have a first degree demonstrating competence in medieval and modern French at the level of at least a 2.1 and would normally be expected to have an MA (or to be in the process of completing an MA) in a relevant subject, or equivalent, to the level of at least a Merit. Applicants also need to meet the standard English-language entry requirements for\\\\u00a0<a href=\\\\\\"http://www.kcl.ac.uk/study/postgraduate/apply/entry-requirements/english-language.aspx\\\\\\">King\\\\u2019s College London</a>, and should note that theses must normally be written in English (only under exceptional circumstances are PhD students in the Department of French permitted to write theses in French).</p><p>The student will undertake a programme of doctoral research on a topic that falls broadly within one of the projects three strands: for further details see\\\\u00a0<a href=\\\\\\"http://blogs.kcl.ac.uk/tvof/about-tvof/more-about-the-project/\\\\\\">more about the project</a>. Candidates wishing to discuss an application informally may contact either\\\\u00a0<a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/gaunt/index.aspx\\\\\\">Simon Gaunt</a>\\\\u00a0or\\\\u00a0<a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/venturas.aspx\\\\\\">Simone Ventura</a>\\\\u00a0and should submit an application to simon.gaunt@kcl.ac.uk by midnight on 29 January 2016 consisting of the following:</p><ul><li>A research proposal consisting of no more than 2 sides of A4</li><li>A Curriculum Vitae that includes details of all academic qualifications</li><li>Two references: you should ask your referees to send these independently to\\\\u00a0<a href=\\\\\\"http://www.kcl.ac.uk/artshums/depts/french/people/academic/gaunt/index.aspx\\\\\\">Simon Gaunt</a>\\\\u00a0by the deadline</li></ul>\\"}, {\\"type\\": \\"image_and_text\\", \\"value\\": {\\"text\\": \\"<p>The successful candidate will subsequently be asked to submit a formal application for a place on the PhD programme at King\\\\u2019s College London if s/he has not already done so.</p><p>The project student will be a full member of the project team and be expected to take part in team meetings, seminars, and conferences. S/he will receive training in working with manuscripts, will be provided with his/her own laptop, and will be eligible for the project\\\\u2019s travel funds.</p>\\", \\"image\\": 31, \\"alignment\\": \\"right\\", \\"caption\\": \\"<p>Detail of a miniature of Troy, from London, British Library, Royal 20 D I, f. 67r. Reproduced with the permission of the British Library Board.</p>\\"}}]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 31, "path": "0001000100060002", "owner": 1, "pk": 27, "first_published_at": null, "url_path": "/home/news/phd-studentship/", "expired": false, "slug": "phd-studentship", "expire_at": null, "go_live_at": null}	\N	27	1
48	f	2016-05-24 15:09:04.087805+01	{"locked": false, "title": "Jacob\\u2019s speckled flock, miscegenation and the dangers of female desire", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>The\\\\u00a0<i>Histoire ancienne\\\\u00a0</i>is a text obsessed with origins, whether tracing back the evolution of cultural and intellectual customs (as explored in this\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/blog/medieval-present-and-biblical-past-continuity-change-and-doubt/\\\\\\">post</a>), or, perhaps more significantly, attempting to establish the genealogical roots of contemporary medieval society. Questions concerning how origins affect behaviour and (il)legitimate heirs abound throughout. One rogue example, however, complicates this message. It is the longest secular \\\\u2018anecdote\\\\u2019 inserted into the Genesis section, introduced by the perplexing rubric: \\\\u2018C\\\\u2019on ne doit faire en chambre de haut home nulle laide figure\\\\u2019\\\\u00a0 (Why a nobleman shouldn\\\\u2019t have [images of] ugly figures in his bedroom) (Paris, BNF, f. fr. 20125, f. 48vb). Whilst much of the other supplementary material can be traced back to Peter Comestor\\\\u2019s\\\\u00a0<i>Historia scholastica</i>\\\\u00a0amongst other sources, this intervention represents the author\\\\u2019s development of an unusual theological commentary.\\\\u00a0</p>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 38, \\"caption\\": \\"<p>Miniature of Jacob kneeling\\\\u00a0before Isaac,\\\\u00a0pretending to be his brother Esau, from Paris, BnF, f. fr. 20125, f. 43v.\\\\u00a0Source:\\\\u00a0<a href=\\\\\\"http://gallica.bnf.fr/\\\\\\">Gallica.BnF.fr</a>.</p>\\"}}, {\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>The episode that precedes this anecdote concerns Jacob\\\\u2019s request to leave Laban, his father-in-law and uncle, after many years of service, the acquisition of two wives and multiple children. Laban refuses to let him go and instead offers to pay him for tending his flock. Jacob then proposes the speckled animals as payment. Laban agrees to this, and the flock is thus divided. We then hear how Jacob miraculously causes the speckled flock to increase. Jacob\\\\u2019s \\\\u2018engin\\\\u2019 (ruse) is described as \\\\u2018une merveillouse chose\\\\u2019 which works\\\\u00a0\\\\u2018contre nature\\\\u2019 (f. 48ra). It involves peeling back some of the bark from branches of poplar, almond, and plane trees, and then placing them in front of the animals\\\\u2019 drinking place, with the intention that the plain females look at the multi-coloured branches whilst copulating. This plan works out successfully for Jacob, and soon the speckled flock increases significantly. When Laban's sons perceive what has happened, they let their father know, who then asks Jacob to swap the speckled flock for the animals of a single colour. Jacob agrees, and uses the same ruse to increase the plain animals, making the branches by \\\\u00a0the water a single colour (black or white with all the bark peeled off). \\\\u00a0His\\\\u00a0bewildered\\\\u00a0uncle gives up, realising that Jacob's flock will somehow always increase.\\\\u00a0</p>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 57, \\"caption\\": \\"<p>Miniature from the 'Rochester Bestiary', London, British Library, Royal 12 F XIII, f. 35r. Source:\\\\u00a0<a href=\\\\\\"http://www.bl.uk/catalogues/illuminatedmanuscripts/ILLUMIN.ASP?Size=mid&amp;IllID=33635\\\\\\">British Library, Catalogue of Illuminated Manuscripts</a>.</p>\\"}}, {\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>At first, the inserted secular tale that follows seems incongruous after the outcome of the episode. However, the narrator explains \\\\u2018de la semblance de ces verges deffendent li plusor sage home encore qu\\\\u2019en chambre a haut home ne a haute dame ne doit on paindre ne portraire diverse forme d\\\\u2019ome ne laide samblance\\\\u2019 (in the same manner as the branches, many wise men advise against painting portraits of different types of men of ugly appearance in the bedrooms of noblemen and noblewomen) (f. 48vb). So, just as the different coloured branches affected the progeny of the flock, the same could happen when \\\\u2018la dame concoive en l\\\\u2019esgardance [et] en la pensee de la semblance de la figure\\\\u2019 (the woman conceives whilst looking at and thinking about the appearance of the [painted] figure) (f. 48vb). After setting out its moral, the narrator tells the tale of an incredibly beautiful noblewoman and her equally attractive husband, who were very much in love. They lived in a richly adorned mansion, and their bedroom was \\\\u2018mout vaillans de grant maniere,\\\\u00a0painte [et] portraite a or [et] a asur de chief en chief tote de riches estories ancieines\\\\u2019 (extremely opulent, painted and decorated in gold and azure, [and] from top to bottom depicted magnificent stories of ancient times\\\\u2019 (ff. 48vb-49ra). In the lady\\\\u2019s eyeline, whilst lying in her bed, was a portrait of a figure \\\\u2018samblant a un noir home d\\\\u2019Ethiope\\\\u2019 (resembling a black man from Ethiopia) (f. 49ra), whose appearance is described in abhorrently racist terms. This figure greatly appealed to the lady, who looked at it constantly (\\\\u2018au main [et] au soir\\\\u2019). After being impregnated by her husband (\\\\u2018co[n]ciut un fiz de son baron\\\\u2019 (f. 49ra)), she then gives birth to a child \\\\u2018sambla[n]s a l\\\\u2019image\\\\u2019 ([which] resembled the image).\\\\u00a0</p>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 39, \\"caption\\": \\"<p>Paris, BnF, f. fr. 20125, f. 48v.\\\\u00a0Source:\\\\u00a0<a href=\\\\\\"http://gallica.bnf.fr/\\\\\\">Gallica.BnF.fr</a>.</p>\\"}}, {\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>It is not uncommon to find the basic principle of this tale in commentaries on how Jacob increased the speckled flock in the writings of the Church Fathers and contemporary medieval authors. In St Jerome\\\\u2019s\\\\u00a0<i>Liber quaestionum hebraicarum in Genesim</i>, immediately after describing Jacob\\\\u2019s ruse, he explains how it demonstrates \\\\u2018the nature of females in the act of conception\\\\u2019 (\\\\u2018in conceptu feminarum esse naturam\\\\u2019) and cites how Quintilian used it in defence of a white woman who gave birth to an Ethiopian baby. Similar comments in relation to the offspring of animals and women reflecting what they saw (or imagined) are found in Isidore of Seville\\\\u2019s\\\\u00a0<i>Etymologies</i>\\\\u00a0(12.58-60), amongst many others.</p><p>In the\\\\u00a0<i>HA</i>, the precept is developed into a short narrative insertion, an act justified by the author in his final words on the topic: \\\\u2018en plusors aventures que su[n]t avenues puet on prendre aucun bon essample qui veut oir retenir [et] aprendre\\\\u2019 (one can take good examples from many past events/adventures, [as long as you are open to] remembering and learning [from them]) (f. 49ra).\\\\u00a0</p><p>Yet, this narrative elaboration simultaneously reveals not only abhorrent views on racial difference, but also anxiety about the effects of female desire, which risks destabilising genealogical legitimacy. Moreover, it illustrates how the reception of penetrating depictions of \\\\u2018riches estories ancieines\\\\u2019 cannot necessarily be controlled.</p><p><br/></p><p>Bibliography</p><p>For an overview of material related to Jacob\\\\u2019s use of the different coloured branches, see\\\\u00a0<br/>Irven Resnick,\\\\u00a0<i>Marks of Distinctions: Christian Perceptions of Jews in the High Middle Ages</i>\\\\u00a0(Washington, DC: The Catholic University of America Press, 2012), pp. 291-300.</p>\\"}]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 31, "path": "0001000100050001", "owner": 1, "pk": 28, "first_published_at": null, "url_path": "/home/blog/jacobs-speckled-flock-miscegenation-and-dangers-female-desire/", "expired": false, "slug": "jacobs-speckled-flock-miscegenation-and-dangers-female-desire", "expire_at": null, "go_live_at": null}	\N	28	1
49	f	2016-05-24 15:13:07.916148+01	{"locked": false, "title": "Our Catalan friend", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>Last week for the first time I was able to work on the manuscript BnF f.fr. 20125 itself. With its 375 neatly written folios, it\\\\u2019s a substantial and impressive book. Everything about it indicates a lot of money, care and labour were invested in making it: some of the corrections made by the scribe, the rubricator and a contemporary editor bespeak attention to detail, the quality and gold decoration of the images are astonishing, and even the regularity of the quire structure suggests a meticulously executed project (see the\\\\u00a0description by the\\\\u00a0<a href=\\\\\\"http://www.medievalfrancophone.ac.uk/browse/mss/47/manuscript.html\\\\\\">MFLCOF</a>\\\\u00a0project). One can also tell that the book has been both read and treasured. On the one hand, the writing on some pages is badly effaced through use; on the other it is by and large in excellent condition.</p><p>As the physical structure of the manuscript is already well-documented, I spent most of my time deciphering passages from the 100 or so folios we have already transcribed that we have been unable to read from the digitisation. Another key task was the transcription of the 45 marginal annotations in a later medieval hand (late 14th\\\\u00a0or early 15th-c.): we had been able to make sense of only a few of these using the digitisation, partly because of the unfamiliar cursive hand, partly because a good number disappear into the gutter of the manuscript in its current 18th-c. binding and are not fully visible on the digitisation (which suggests that the original binding must have been much looser).</p><p>I guess we medievalists don\\\\u2019t get out much as I found the process of learning how to read this handwriting strangely exhilarating. My breakthrough came when staring for the fifth or sixth time at folio 7r and more particularly at the first annotation:</p>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 17, \\"caption\\": \\"<p>BnF f.fr. 20125, f. 7r. Source: Gallica.BnF.fr.</p>\\"}}, {\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>When one looks at all the annotations, one quickly realises they all begin with an abbreviated \\\\u2018nota\\\\u2019 (indeed some consist simply of \\\\u2018nota\\\\u2019), though some, as here, are hastily written. Of course context helped me here, as it did with reading the other annotations. The passage that is glossed is about the foundation of the city of Ephraim, and a few lines later we are told by the text \\\\u2018Ceste cite fu la premiere qui onques fu estoree\\\\u2019. This annotation reads \\\\u2018no[ta] p[ri]ma cjutat\\\\u2019:</p>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 37, \\"caption\\": \\"<p>BnF f.fr. 20125, f. 7r detail. The beginning of 'p[ri]ma' is not visible on the digitisation. Source: Gallica.BnF.fr.</p>\\"}}, {\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>Deciphering the word \\\\u2018cjutat\\\\u2019 allowed me to identify some common letters, which in turn gave me the key to reading the other annotations. A better paleographer would have got there more quickly, but small victories in research are always a pleasure!</p><p>The annotations or glosses have not attracted much attention. However, they give us an idea of what at least one later medieval reader thought worthy of remark in the\\\\u00a0<i>Histoire ancienne</i>,\\\\u00a0which in itself is of great interest to our project, as is the language in which they are written.\\\\u00a0Earlier scholarship deemed them to be written in Occitan, or to be the work of \\\\u2018someone of Spanish origin\\\\u2019. However, Fabio Zinelli has recently argued they are written in Catalan, and we agree. As Zinelli also suggests, this does not necessarily mean they were written in Catalonia, since our Catalan friend (as I have come to think of him) could easily have been somewhere else with a Catalan presence in the Middle Ages: Rhodes, Cyprus, or the Greek mainland.</p><p>So what was our Catalan friend interested in? The short answer is (and in this order) origins, places and people. It\\\\u2019s not possible to know why he stopped annotating the book after one hundred folios (perhaps a librarian caught him writing in the margins and told him off!), but one of the dominant themes of the earlier sections of the\\\\u00a0<i>Histoire ancienne</i>\\\\u00a0is the foundation of cities, the origin of customs, technologies, languages and so on: 19 of the annotations concern the foundation of cities, the first kings of significant kingdoms, the origin of different languages, of the cultivation of olives, or of music, necromancy, astronomy, of iron and copper work. While origins are a dominant theme of the text, the rubrics tend to focus on events and the names of people. Perhaps our reader stopped annotating the book when the theme he was most interested in and wanted to be able to locate quickly ceased to be so important? In any event, his annotations suggest an interest in history focussed on beginnings.</p><p>He also frequently marks places, either with \\\\u2018nota\\\\u2019 signs, or with glosses like \\\\u2018d[e]la yla d[e] xpre\\\\u2019 (f. 16v) or \\\\u2018no[ta]: d[e]la ploblacjio d[e]la jla d[e] rod[e]s\\\\u2019 (f. 85v) (which incidentally contain several characteristically Catalan forms). Some of the places he picks out are biblical, but the majority are Eastern Mediterranean and are not mentioned in rubrics. Thus our Catalan friend also approached the\\\\u00a0<i>Histoire ancienne\\\\u00a0</i>with a cultural geography of the Mediterranean in mind. It is probably coincidental that two of his annotations concern Rhodes (see also f. 18r), but the prevalence of places in the Eastern Mediterranean that are picked out by glosses may support Zinelli\\\\u2019s suggestion that the annotations were made there.\\\\u00a0</p>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 19, \\"caption\\": \\"<p>BnF f.fr. 20125, f. 18r. The reference to Rhodes is the second in the left margin. Source: Gallica.BnF.fr.</p>\\"}}, {\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>That this Catalan speaker (aka our man in Rhodes?) was reading and reacting to a book written in French to satisfy his interest in history is of course vital to our project. If he was (quite rightly) told off for defacing the book, we at least are grateful to him for doing so!</p><p>Simon Gaunt</p>\\"}]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 31, "path": "0001000100050002", "owner": 1, "pk": 29, "first_published_at": null, "url_path": "/home/blog/our-catalan-friend/", "expired": false, "slug": "our-catalan-friend", "expire_at": null, "go_live_at": null}	\N	29	1
50	f	2016-05-24 15:16:18.602053+01	{"locked": false, "title": "\\u2018Uns rois estoit adonques en Thebes\\u2019 \\u2013\\u2013 Once upon a time there was a king in Thebes, or the (morbid) pleasure of storytelling", "numchild": 0, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>For Horace poets had either to be useful (<i>prodesse</i>) or to delight (<i>delectare</i>). The\\\\u00a0<i>Histoire ancienne jusqu\\\\u2019\\\\u00e0 C\\\\u00e9sar</i>, our object of study, fulfils both objectives. On the one hand, the\\\\u00a0<i>HA</i>\\\\u00a0conveys serious, edifying accounts of how crucial events for humanity took place (the creation, the flood, the foundation of Troy, Rome, Paris): in this respect, the\\\\u00a0<i>HA</i>\\\\u00a0is \\\\u2018history\\\\u2019 providing the audience with useful knowledge. On the other hand, the\\\\u00a0<i>HA</i>\\\\u00a0presents a showcase of the most delectable stories on the market: the tales that everybody had heard of or wanted to know about. How did the angel stop the arm of Abraham on the verge of killing Isaac, his beloved son? How was Rome founded? How about the story of the twins, Romulus and Remus? And, of course, what happened between Eneas and Dido? Did he really leave her on the shores of Carthage? Did she kill herself without his knowing so that he might not feel regret or shame? (Needless to say the anonymous redactor of the\\\\u00a0<i>HA</i>fuelled Eneas\\\\u2019 bad press, well-deserved according to many).</p><p>We all know how attractive gruesome stories can be. There are tales we always return to\\\\u2013\\\\u2013no matter how many times we hear them and no matter how violent they are. The legend of Oedipus is one of these stories. Not\\\\u00a0<i>a</i>\\\\u00a0tragedy, of course, but rather\\\\u00a0<i>the</i>\\\\u00a0tragedy. This story, part of the Theban saga, works so well that it is invariably successful in fascinating us with its bloodthirsty and vicious little charm: even when narrated in medieval French, in the thirteenth century, on the basis of some obscure as yet unidentified source, which in turn reworked the first- and second-century Latin versions of the Theban myth (Seneca and Statius), which in turn had rewritten the drama that crystallised in its most famous version (for us), the one that penned by Sophocles in Pericles\\\\u2019 Athens (fifth century BC).</p>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 35, \\"caption\\": \\"<p>The brief retelling of the Oedipus story in the\\\\u00a0<i>HA</i>\\\\u00a0is often richly illustrated, with particular attention paid to two key episodes in Oedipus\\\\u2019s tragic trajectory: his childhood exposure and his encounter with the sphinx. Two-compartment miniature of Laius and Jocasta (above) and Oedipus hanging from a tree (below), from Paris, BnF, f. fr. 20125, f. 88v. Source:\\\\u00a0<a href=\\\\\\"http://gallica.bnf.fr/\\\\\\">Gallica.BnF.fr</a>.</p>\\"}}, {\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>The redactor of the\\\\u00a0<i>HA</i>\\\\u00a0was aware of Oedipus\\\\u2019s fate, yet provided his own version of the story, peculiar both in terms of plot development and in tone. One crucial moment in the tragedy illustrates this: Oedipus\\\\u2019s murder of Laius, his father. The red title or \\\\u2018rubric\\\\u2019 of the passage in Paris, BnF, f. fr. 20125 summarises the episode as follows: \\\\u2018Que Edippus quist respons a Apollin qui estoit ses peres et coment il l\\\\u2019ocist\\\\u2019 (f. 90va) (How Oedipus consulted (the oracle of) Apollo about whom his father was, and how he killed him).</p><p>As we all remember, Oedipus, having discovered he is not the son of the king Polybus, leaves to look for his parents. The oracle tells him he will find out if he goes to Thebes. On his way to Thebes, however, Oedipus arrives at the city of Daulis, in the Greek region of Phocis\\\\u2013\\\\u2013the castle of \\\\u2018Phoce\\\\u2019 in the French text. According to the\\\\u00a0<i>HA</i>, Oedipus stops at the outskirts of the city to attend some jousts. Unfortunately, a terrible fight breaks out. Misfortune after misfortune, Oedipus finds himself crushed by the mob against the city gates. Precisely at this point, Laius, the king of Thebes, who was also there to watch, comes out of the gates and is killed by Oedipus in rather opaque circumstances. No account of the murderous fight over who had right of way at the crossroad near Daulis. Famously, Oedipus kills Laius, and then encounters the sphinx, before finally getting to Thebes.</p>\\"}, {\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 25, \\"caption\\": \\"<p>Oedipus encounters the sphinx, from\\\\u00a0<a href=\\\\\\"http://www.bl.uk/manuscripts/FullDisplay.aspx?index=0&amp;ref=Add_MS_15268\\\\\\">London, British Library,\\\\u00a0Add. 15268</a>, f. 77v.\\\\u00a0Reproduced with the permission of the British Library Board.</p>\\"}}, {\\"type\\": \\"paragraph\\", \\"value\\": \\"<p>According to the French narrator, Oedipus kills his father in a chaotic general mel\\\\u00e9e not in an individual encounter. This means that the trigger for the tragic fate of Oedipus and that of his lineage is quite different. This final gloss on how Oedipus actually killed his father is not without irony:</p><p><i>Teus ia qui dient qu\\\\u2019il l\\\\u2019ocist au clore dou flael de la porte, [et] teus i a que dient de s\\\\u2019espee. Or vos en tenes au quel que uos voudres, mes ensi fu mors li rois de Thebes, mes ne sot nus de ses gens qui cil estoit qui l\\\\u2019avoit mort, quar tost se refu Edippus mis entre les autres.\\\\u00a0(Paris, BnF, fr. 20125, f. 91ra)</i></p><p>(Some people say that he (Oedipus) killed his father while the doors (of the city) were closing down [literally: while the bar was locking down the doors of the city], and some others say he did it with his sword. Now, you choose whichever you like, thus the king of Thebes was killed, and no one among the king\\\\u2019s people knew who killed him, as Oedipus quickly returned to the crowd.)</p><p>The narrator here seems humorously to give up: unable to provide a consistent report of the facts, he leaves the decision to his audience. It is then up to us to decide whether Oedipus killed his father brandishing a sword, as a coldblooded but noble murderer, or as a vulgar hooligan who allowed his father to die ridiculously, crushed by the heavy gates of\\\\u00a0<i>Phoce</i>.</p><p>Simone Ventura</p>\\"}]", "search_description": "", "depth": 4, "latest_revision_created_at": null, "has_unpublished_changes": false, "content_type": 31, "path": "0001000100050003", "owner": 1, "pk": 30, "first_published_at": null, "url_path": "/home/blog/uns-rois-estoit-adonques-en-thebes-once-upon-time-there-was-king-thebes-or-morbid-pleasure-storytelling/", "expired": false, "slug": "uns-rois-estoit-adonques-en-thebes-once-upon-time-there-was-king-thebes-or-morbid-pleasure-storytelling", "expire_at": null, "go_live_at": null}	\N	30	1
52	f	2016-05-26 16:15:29.0294+01	{"locked": false, "title": "Home", "numchild": 6, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><em>The Values of French Language and Literature in the European Middle Ages</em>\\\\u00a0is a five-year research project running from 2015 to 2020 in the Department of French at King\\\\u2019s College London, funded by the European Research Council within the framework of an Advanced Grant.<em>The Values of French</em>\\\\u00a0examines the nature and value of the use of French in Europe during a crucial period, 1100-1450, less in terms of its cultural prestige (the traditional focus of scholarship) than of its role as a supralocal, transnational language, particularly in Western Europe and the Eastern Mediterranean. The project fosters collaboration between, and cuts across, different intellectual and national scholarly traditions, drawing on expertise in codicology, critical theory, linguistics, literature, and philology; it involves scholars from a range of European countries and North America, entailing empirical research around a complex and widely disseminated textual tradition vital to medieval understandings of European history and identity,\\\\u00a0<em>L\\\\u2019Histoire ancienne jusqu\\\\u2019\\\\u00e0 C\\\\u00e9sar</em>. This case study grounds and stimulates broader speculative reflection on two questions concerning linguistic identity. What is the relation historically between language and identity in Europe? How are cognate languages demarcated from each other? Indeed, its final aim, through and beyond its consideration of French as a\\\\u00a0<em>lingua franca</em>, is to interrogate that language\\\\u2019s role in the emergence of a European identity in the Middle Ages. To:\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/values-french/\\\\\\">More about the project</a></p>\\"}]", "search_description": "", "depth": 2, "latest_revision_created_at": "2016-05-16T10:57:08.823Z", "has_unpublished_changes": false, "content_type": 2, "path": "00010001", "owner": null, "pk": 3, "first_published_at": "2016-05-16T10:57:08.877Z", "url_path": "/home/", "expired": false, "slug": "home", "expire_at": null, "go_live_at": null}	\N	3	1
53	f	2016-05-26 16:20:06.234769+01	{"locked": false, "title": "Home", "numchild": 6, "show_in_menus": false, "live": true, "seo_title": "", "content": "[{\\"type\\": \\"image_and_caption\\", \\"value\\": {\\"images\\": 63, \\"caption\\": \\"<p>Miniature of Noah and the ark, from London, British Library, Add. 15268, f. 7v. Reproduced with the permission of the British Library Board.</p>\\"}}, {\\"type\\": \\"paragraph\\", \\"value\\": \\"<p><em>The Values of French Language and Literature in the European Middle Ages</em>\\\\u00a0is a five-year research project running from 2015 to 2020 in the Department of French at King\\\\u2019s College London, funded by the European Research Council within the framework of an Advanced Grant.<em>The Values of French</em>\\\\u00a0examines the nature and value of the use of French in Europe during a crucial period, 1100-1450, less in terms of its cultural prestige (the traditional focus of scholarship) than of its role as a supralocal, transnational language, particularly in Western Europe and the Eastern Mediterranean. The project fosters collaboration between, and cuts across, different intellectual and national scholarly traditions, drawing on expertise in codicology, critical theory, linguistics, literature, and philology; it involves scholars from a range of European countries and North America, entailing empirical research around a complex and widely disseminated textual tradition vital to medieval understandings of European history and identity,\\\\u00a0<em>L\\\\u2019Histoire ancienne jusqu\\\\u2019\\\\u00e0 C\\\\u00e9sar</em>. This case study grounds and stimulates broader speculative reflection on two questions concerning linguistic identity. What is the relation historically between language and identity in Europe? How are cognate languages demarcated from each other? Indeed, its final aim, through and beyond its consideration of French as a\\\\u00a0<em>lingua franca</em>, is to interrogate that language\\\\u2019s role in the emergence of a European identity in the Middle Ages. To:\\\\u00a0<a href=\\\\\\"http://www.tvof.ac.uk/values-french/\\\\\\">More about the project</a></p>\\"}]", "search_description": "", "depth": 2, "latest_revision_created_at": "2016-05-26T15:15:29.029Z", "has_unpublished_changes": false, "content_type": 2, "path": "00010001", "owner": null, "pk": 3, "first_published_at": "2016-05-16T10:57:08.877Z", "url_path": "/home/", "expired": false, "slug": "home", "expire_at": null, "go_live_at": null}	\N	3	1
\.


--
-- TOC entry 2314 (class 0 OID 409771)
-- Dependencies: 186
-- Data for Name: wagtailcore_pageviewrestriction; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailcore_pageviewrestriction (id, password, page_id) FROM stdin;
\.


--
-- TOC entry 2315 (class 0 OID 409779)
-- Dependencies: 188
-- Data for Name: wagtailcore_site; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailcore_site (id, hostname, port, is_default_site, root_page_id, site_name) FROM stdin;
2	localhost	80	t	3	\N
\.


--
-- TOC entry 2326 (class 0 OID 410046)
-- Dependencies: 204
-- Data for Name: wagtaildocs_document; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtaildocs_document (id, title, file, created_at, uploaded_by_user_id, collection_id) FROM stdin;
\.


--
-- TOC entry 2327 (class 0 OID 410087)
-- Dependencies: 206
-- Data for Name: wagtailembeds_embed; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailembeds_embed (id, url, max_width, type, html, title, author_name, provider_name, thumbnail_url, width, height, last_updated) FROM stdin;
\.


--
-- TOC entry 2328 (class 0 OID 410100)
-- Dependencies: 208
-- Data for Name: wagtailforms_formsubmission; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailforms_formsubmission (id, form_data, submit_time, page_id) FROM stdin;
\.


--
-- TOC entry 2329 (class 0 OID 410117)
-- Dependencies: 210
-- Data for Name: wagtailimages_filter; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailimages_filter (id, spec) FROM stdin;
1	max-165x165
2	
3	original
4	max-800x600
5	width-400
6	width-500
7	1000
8	width-1000
9	width-2000
\.


--
-- TOC entry 2330 (class 0 OID 410125)
-- Dependencies: 212
-- Data for Name: wagtailimages_image; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailimages_image (id, title, file, width, height, created_at, focal_point_x, focal_point_y, focal_point_width, focal_point_height, uploaded_by_user_id, file_size, collection_id) FROM stdin;
44	Jason and the Argonauts add ms 15268 f105v 2 compartment	original_images/Jason_and_the_Argonauts_add_ms_15268_f105v_2_compartment.jpeg	622	678	2016-05-23 14:56:37.859146+01	\N	\N	\N	\N	1	421927	1
45	Jason and the Argonauts add ms 15268 f105v 	original_images/Jason_and_the_Argonauts_add_ms_15268_f105v_copy.jpg	628	1020	2016-05-23 14:56:37.980684+01	\N	\N	\N	\N	1	618685	1
46	Jason and the golden fleece add ms 19669 f077r  2	original_images/Jason_and_the_golden_fleece_add_ms_19669_f077r_copy_2.jpg	342	295	2016-05-23 14:56:38.087106+01	\N	\N	\N	\N	1	120767	1
47	Jason and the golden fleece add ms 19669 f077r  2 Qrdgy1I	original_images/Jason_and_the_golden_fleece_add_ms_19669_f077r_copy_2_Qrdgy1I.jpg	342	295	2016-05-23 14:56:38.193143+01	\N	\N	\N	\N	1	120767	1
48	Marriage of Paris and Helen royal ms 20 d i f053r 	original_images/Marriage_of_Paris_and_Helen_royal_ms_20_d_i_f053r_copy.jpg	891	632	2016-05-23 14:56:38.308251+01	\N	\N	\N	\N	1	577413	1
50	Noah and the ark add ms 15268 f007v 	original_images/Noah_and_the_ark_add_ms_15268_f007v_copy.jpg	641	1039	2016-05-23 14:56:38.537065+01	\N	\N	\N	\N	1	735442	1
51	Priam joining the battle royal ms 20 d i f117v  2	original_images/Priam_joining_the_battle_royal_ms_20_d_i_f117v_copy_2.jpg	909	676	2016-05-23 14:56:38.653231+01	\N	\N	\N	\N	1	755861	1
53	Royal 20 D I f. 21v	original_images/Royal_20_D_I_f._21v.png	682	728	2016-05-23 14:56:38.891565+01	\N	\N	\N	\N	1	1078599	1
56	Royal MS 20 D I Wheel of Fortune-f.163v	original_images/Royal_MS_20_D_I_Wheel_of_Fortune-f.163v.png	1063	853	2016-05-23 14:56:39.317763+01	\N	\N	\N	\N	1	2064821	1
57	Sheep Royal 12 F XIII f. 35r	original_images/Sheep_Royal_12_F_XIII_f._35r.png	770	642	2016-05-23 14:56:39.452401+01	\N	\N	\N	\N	1	1187991	1
58	Start of Troy add ms 19669 f077r 	original_images/Start_of_Troy_add_ms_19669_f077r_copy.jpg	438	800	2016-05-23 14:56:39.568439+01	\N	\N	\N	\N	1	343627	1
59	Temple of Janus with senators dining add ms 15268 f242v 	original_images/Temple_of_Janus_with_senators_dining_add_ms_15268_f242v_copy.jpg	619	456	2016-05-23 14:56:39.679606+01	\N	\N	\N	\N	1	277328	1
60	Theseus and the Giant royal ms 20 d i f026r 	original_images/Theseus_and_the_Giant_royal_ms_20_d_i_f026r_copy.jpg	815	557	2016-05-23 14:56:39.803912+01	\N	\N	\N	\N	1	516085	1
61	Theseus attacking Crete add ms 15268 f136v 	original_images/Theseus_attacking_Crete_add_ms_15268_f136v_copy.jpg	595	598	2016-05-23 14:56:39.935425+01	\N	\N	\N	\N	1	349766	1
62	Tiger of Thebes royal ms 20 d i f017v 	original_images/Tiger_of_Thebes_royal_ms_20_d_i_f017v_copy.jpg	889	567	2016-05-23 14:56:40.046866+01	\N	\N	\N	\N	1	551948	1
63	BritishLibraryAdd15268	original_images/header.jpg	1000	288	2016-05-26 16:19:46.099076+01	\N	\N	\N	\N	1	\N	1
2	13138901 10154176902044187 9179986453672733933 n	original_images/13138901_10154176902044187_9179986453672733933_n.jpg	420	294	2016-05-18 16:30:53.524523+01	\N	\N	\N	\N	1	23779	1
1	test image	original_images/beta_flag.png	124	125	2016-05-17 13:17:31.879211+01	\N	\N	\N	\N	1	3402	1
3	Tombs of Troilus and Memnon Hecuba and Paris royal ms 20 d i f146r 	original_images/Tombs_of_Troilus_and_Memnon_Hecuba_and_Paris_royal_ms_20_d_i_f146r_copy.jpg	872	1370	2016-05-23 14:56:32.986139+01	\N	\N	\N	\N	1	1352855	1
4	Transcription fr. 20125 f. 24ra	original_images/Transcription_fr._20125_f._24ra.jpg	1500	1125	2016-05-23 14:56:33.205956+01	\N	\N	\N	\N	1	2081417	1
5	Transcription fr. 20125 f. 24ra WtYzkKI	original_images/Transcription_fr._20125_f._24ra_WtYzkKI.jpg	1500	1125	2016-05-23 14:56:33.33095+01	\N	\N	\N	\N	1	2081417	1
6	Transcription fr. 20125 f. 24ra Z2XPl3Y	original_images/Transcription_fr._20125_f._24ra_Z2XPl3Y.jpg	1500	1125	2016-05-23 14:56:33.45803+01	\N	\N	\N	\N	1	2081417	1
7	Troybest royal ms 20 d i f154r 	original_images/Troybest_royal_ms_20_d_i_f154r_copy.jpg	889	1364	2016-05-23 14:56:33.598763+01	\N	\N	\N	\N	1	1520453	1
8	Troybest royal ms 20 d i f154r  1OEb6tm	original_images/Troybest_royal_ms_20_d_i_f154r_copy_1OEb6tm.jpg	889	1364	2016-05-23 14:56:33.748727+01	\N	\N	\N	\N	1	1520453	1
9	Troybest royal ms 20 d i f154r  3ZBQ6SF	original_images/Troybest_royal_ms_20_d_i_f154r_copy_3ZBQ6SF.jpg	889	1364	2016-05-23 14:56:33.873165+01	\N	\N	\N	\N	1	1520453	1
10	Troybest royal ms 20 d i f154r  5PQ0u0Q	original_images/Troybest_royal_ms_20_d_i_f154r_copy_5PQ0u0Q.jpg	889	1364	2016-05-23 14:56:34.014624+01	\N	\N	\N	\N	1	1520453	1
11	Troybest royal ms 20 d i f154r  CLM5B0h	original_images/Troybest_royal_ms_20_d_i_f154r_copy_CLM5B0h.jpg	889	1364	2016-05-23 14:56:34.131305+01	\N	\N	\N	\N	1	1520453	1
12	Troybest royal ms 20 d i f154r  j3T9vST	original_images/Troybest_royal_ms_20_d_i_f154r_copy_j3T9vST.jpg	889	1364	2016-05-23 14:56:34.255317+01	\N	\N	\N	\N	1	1520453	1
13	Troybest royal ms 20 d i f154r  Kz2s9qC	original_images/Troybest_royal_ms_20_d_i_f154r_copy_Kz2s9qC.jpg	889	1364	2016-05-23 14:56:34.364987+01	\N	\N	\N	\N	1	1520453	1
17	7r	original_images/7r.jpeg	1024	1482	2016-05-23 14:56:34.841575+01	\N	\N	\N	\N	1	422697	1
14	Troybest royal ms 20 d i f154r  LiKIwTi	original_images/Troybest_royal_ms_20_d_i_f154r_copy_LiKIwTi.jpg	889	1364	2016-05-23 14:56:34.478658+01	\N	\N	\N	\N	1	1520453	1
15	Troybest royal ms 20 d i f154r  nE7mrMB	original_images/Troybest_royal_ms_20_d_i_f154r_copy_nE7mrMB.jpg	889	1364	2016-05-23 14:56:34.60547+01	\N	\N	\N	\N	1	1520453	1
16	Troybest royal ms 20 d i f154r  W23RQlT	original_images/Troybest_royal_ms_20_d_i_f154r_copy_W23RQlT.jpg	889	1364	2016-05-23 14:56:34.736042+01	\N	\N	\N	\N	1	1520453	1
18	7r detail	original_images/7r_detail.jpg	1646	1214	2016-05-23 14:56:34.962093+01	\N	\N	\N	\N	1	457647	1
19	18r	original_images/18r.jpeg	1024	1482	2016-05-23 14:56:35.081507+01	\N	\N	\N	\N	1	461103	1
20	Abraham and Isaac add ms 15268 f030v 	original_images/Abraham_and_Isaac_add_ms_15268_f030v_copy.jpg	611	576	2016-05-23 14:56:35.178221+01	\N	\N	\N	\N	1	353255	1
21	Add. 19669 f. 58r	original_images/Add._19669_f._58r.png	813	879	2016-05-23 14:56:35.294979+01	\N	\N	\N	\N	1	1490816	1
22	add 15268 1v	original_images/add_15268_1v.jpg	995	1500	2016-05-23 14:56:35.4143+01	\N	\N	\N	\N	1	1325067	1
23	add 15268 1v WsGOS9K	original_images/add_15268_1v_WsGOS9K.jpg	995	1500	2016-05-23 14:56:35.536774+01	\N	\N	\N	\N	1	1325067	1
24	add 15268 16r vj5dlwy	original_images/add_15268_16r_vj5dlwy.jpg	1001	1500	2016-05-23 14:56:35.659898+01	\N	\N	\N	\N	1	1055166	1
25	Add MS 15268 f. 77v	original_images/Add_MS_15268_f._77v.png	795	593	2016-05-23 14:56:35.771382+01	\N	\N	\N	\N	1	1147753	1
34	Einladung-Gastvortrag-Simon-Gaunt z7NFj65	original_images/Einladung-Gastvortrag-Simon-Gaunt_z7NFj65.jpg	1240	1754	2016-05-23 14:56:36.755158+01	\N	\N	\N	\N	1	485072	1
35	f. 20125 88v	original_images/f._20125_88v.jpg	1283	1740	2016-05-23 14:56:36.863992+01	\N	\N	\N	\N	1	590127	1
36	fr. 20125 f. 3r	original_images/fr._20125_f._3r.jpg	417	657	2016-05-23 14:56:36.960537+01	\N	\N	\N	\N	1	69756	1
37	fr. 20125 f. 7r digitisation	original_images/fr._20125_f._7r_digitisation.jpg	1640	919	2016-05-23 14:56:37.068258+01	\N	\N	\N	\N	1	244914	1
38	fr. 20125 f. 43v	original_images/fr._20125_f._43v.jpg	1626	1549	2016-05-23 14:56:37.179111+01	\N	\N	\N	\N	1	581123	1
39	fr. 20125 f. 48v	original_images/fr._20125_f._48v.jpg	1424	2387	2016-05-23 14:56:37.310019+01	\N	\N	\N	\N	1	672392	1
40	Greek ships being wrecked in a storm royal ms 20 d i f176v 	original_images/Greek_ships_being_wrecked_in_a_storm_royal_ms_20_d_i_f176v_copy.jpg	947	518	2016-05-23 14:56:37.417846+01	\N	\N	\N	\N	1	571373	1
41	Henry 2	original_images/Henry_2.jpeg	1080	720	2016-05-23 14:56:37.531868+01	\N	\N	\N	\N	1	131512	1
42	Hercules and Theseus royal ms 20 d i f021v 	original_images/Hercules_and_Theseus_royal_ms_20_d_i_f021v_copy.jpg	935	455	2016-05-23 14:56:37.630971+01	\N	\N	\N	\N	1	479815	1
43	Image and transcription f. 24ra	original_images/Image_and_transcription_f._24ra.jpg	1754	1239	2016-05-23 14:56:37.756487+01	\N	\N	\N	\N	1	2328638	1
52	Royal 20 D I f. 1r	original_images/Royal_20_D_I_f._1r.png	758	1100	2016-05-23 14:56:38.772106+01	\N	\N	\N	\N	1	1699287	1
30	Detail Jason and the Argonauts add ms 15268 f105v  2	original_images/Detail_Jason_and_the_Argonauts_add_ms_15268_f105v_copy_2.jpg	590	331	2016-05-23 14:56:36.329306+01	\N	\N	\N	\N	1	199134	1
26	Another battle royal ms 20 d i f117v 	original_images/Another_battle_royal_ms_20_d_i_f117v_copy.jpg	933	1345	2016-05-23 14:56:35.888928+01	\N	\N	\N	\N	1	1443647	1
27	BnF fr. 20125 f. 90r	original_images/BnF_fr._20125_f._90r.jpg	577	899	2016-05-23 14:56:35.996916+01	\N	\N	\N	\N	1	152081	1
28	Construction of Rome add ms 15268 f156r 	original_images/Construction_of_Rome_add_ms_15268_f156r_copy.jpg	608	517	2016-05-23 14:56:36.096318+01	\N	\N	\N	\N	1	330686	1
29	Creation add ms 19669 f004r 	original_images/Creation_add_ms_19669_f004r_copy.jpg	1010	1404	2016-05-23 14:56:36.217018+01	\N	\N	\N	\N	1	1595271	1
31	Detail of Troy royal ms 20 d i f067r 	original_images/Detail_of_Troy_royal_ms_20_d_i_f067r_copy.jpg	491	558	2016-05-23 14:56:36.427117+01	\N	\N	\N	\N	1	379230	1
32	Einladung-Gastvortrag-Simon-Gaunt	original_images/Einladung-Gastvortrag-Simon-Gaunt.jpg	1240	1754	2016-05-23 14:56:36.545268+01	\N	\N	\N	\N	1	485072	1
33	Einladung-Gastvortrag-Simon-Gaunt PO9TVmS	original_images/Einladung-Gastvortrag-Simon-Gaunt_PO9TVmS.jpg	1240	1754	2016-05-23 14:56:36.649594+01	\N	\N	\N	\N	1	485072	1
49	miniature add 15268 54r HzXNFRN	original_images/miniature_add_15268_54r_HzXNFRN.png	624	470	2016-05-23 14:56:38.422955+01	\N	\N	\N	\N	1	653145	1
55	royal ms 20 d i f169r  qddwnv3	original_images/royal_ms_20_d_i_f169r_copy_qddwnv3.jpg	1069	1500	2016-05-23 14:56:39.181782+01	\N	\N	\N	\N	1	1776377	1
54	Royal 20 D I,f. 109	original_images/Royal_20_D_I_f._109v.png	1082	1018	2016-05-23 14:56:39.026803+01	\N	\N	\N	\N	1	2433320	1
\.


--
-- TOC entry 2331 (class 0 OID 410137)
-- Dependencies: 214
-- Data for Name: wagtailimages_rendition; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailimages_rendition (id, file, width, height, focal_point_key, filter_id, image_id) FROM stdin;
1	images/beta_flag.max-165x165.png	124	125		1	1
2	images/13138901_10154176902044187_91799864536727339.max-165x165.jpg	165	115		1	2
3	images/13138901_10154176902044187_9179986453672733933_.original.jpg	420	294		3	2
4	images/13138901_10154176902044187_91799864536727339.max-800x600.jpg	420	294		4	2
5	images/beta_flag.original.png	124	125		3	1
6	images/beta_flag.max-800x600.png	124	125		4	1
7	images/Tiger_of_Thebes_royal_ms_20_d_i_f017v_copy.max-165x165.jpg	165	105		1	62
8	images/Theseus_attacking_Crete_add_ms_15268_f136v_c.max-165x165.jpg	164	165		1	61
9	images/Theseus_and_the_Giant_royal_ms_20_d_i_f026r_.max-165x165.jpg	165	112		1	60
10	images/Temple_of_Janus_with_senators_dining_add_ms_.max-165x165.jpg	165	121		1	59
11	images/Start_of_Troy_add_ms_19669_f077r_copy.max-165x165.jpg	90	165		1	58
12	images/Sheep_Royal_12_F_XIII_f._35r.max-165x165.png	165	137		1	57
13	images/Royal_MS_20_D_I_Wheel_of_Fortune-f.163v.max-165x165.png	165	132		1	56
14	images/royal_ms_20_d_i_f169r_copy_qddwnv3.max-165x165.jpg	117	165		1	55
15	images/Royal_20_D_I_f._109v.max-165x165.png	165	155		1	54
16	images/Royal_20_D_I_f._21v.max-165x165.png	154	165		1	53
17	images/Royal_20_D_I_f._1r.max-165x165.png	113	165		1	52
18	images/Priam_joining_the_battle_royal_ms_20_d_i_f11.max-165x165.jpg	165	122		1	51
19	images/Noah_and_the_ark_add_ms_15268_f007v_copy.max-165x165.jpg	101	165		1	50
20	images/miniature_add_15268_54r_HzXNFRN.max-165x165.png	165	124		1	49
21	images/Marriage_of_Paris_and_Helen_royal_ms_20_d_i_.max-165x165.jpg	165	117		1	48
22	images/Jason_and_the_golden_fleece_add_ms_19669_f07.max-165x165.jpg	165	142		1	47
23	images/Jason_and_the_golden_fleece_add_ms_19669_f07.max-165x165_3v7SLGY.jpg	165	142		1	46
24	images/Jason_and_the_Argonauts_add_ms_15268_f105v_c.max-165x165.jpg	101	165		1	45
25	images/Jason_and_the_Argonauts_add_ms_15268_f105v_2.max-165x165.jpg	151	165		1	44
26	images/Image_and_transcription_f._24ra.max-165x165.jpg	165	116		1	43
27	images/Royal_20_D_I_f._109v.original.png	1082	1018		3	54
28	images/Royal_20_D_I_f._109v.max-800x600.png	637	600		4	54
29	images/Temple_of_Janus_with_senators_dining_add_ms_152.original.jpg	619	456		3	59
30	images/Temple_of_Janus_with_senators_dining_add_ms_.max-800x600.jpg	619	456		4	59
31	images/Hercules_and_Theseus_royal_ms_20_d_i_f021v_c.max-165x165.jpg	165	80		1	42
32	images/Henry_2.max-165x165.jpg	165	110		1	41
33	images/Greek_ships_being_wrecked_in_a_storm_royal_m.max-165x165.jpg	165	90		1	40
34	images/fr._20125_f._48v.max-165x165.jpg	98	165		1	39
35	images/fr._20125_f._43v.max-165x165.jpg	165	157		1	38
36	images/fr._20125_f._7r_digitisation.max-165x165.jpg	165	92		1	37
37	images/fr._20125_f._3r.max-165x165.jpg	104	165		1	36
38	images/f._20125_88v.max-165x165.jpg	121	165		1	35
39	images/Einladung-Gastvortrag-Simon-Gaunt_z7NFj65.max-165x165.jpg	116	165		1	34
40	images/Einladung-Gastvortrag-Simon-Gaunt_PO9TVmS.max-165x165.jpg	116	165		1	33
41	images/Einladung-Gastvortrag-Simon-Gaunt.max-165x165.jpg	116	165		1	32
42	images/Detail_of_Troy_royal_ms_20_d_i_f067r_copy.max-165x165.jpg	145	165		1	31
43	images/Detail_Jason_and_the_Argonauts_add_ms_15268_.max-165x165.jpg	165	92		1	30
44	images/Creation_add_ms_19669_f004r_copy.max-165x165.jpg	118	165		1	29
45	images/Construction_of_Rome_add_ms_15268_f156r_copy.max-165x165.jpg	165	140		1	28
46	images/BnF_fr._20125_f._90r.max-165x165.jpg	105	165		1	27
47	images/Another_battle_royal_ms_20_d_i_f117v_copy.max-165x165.jpg	114	165		1	26
48	images/Add_MS_15268_f._77v.max-165x165.png	165	123		1	25
49	images/add_15268_16r_vj5dlwy.max-165x165.jpg	110	165		1	24
50	images/add_15268_1v_WsGOS9K.max-165x165.jpg	109	165		1	23
51	images/Hercules_and_Theseus_royal_ms_20_d_i_f021v_copy.original.jpg	935	455		3	42
52	images/Hercules_and_Theseus_royal_ms_20_d_i_f021v_c.max-800x600.jpg	800	389		4	42
53	images/Detail_Jason_and_the_Argonauts_add_ms_15268_f10.original.jpg	590	331		3	30
54	images/Detail_Jason_and_the_Argonauts_add_ms_15268_.max-800x600.jpg	590	331		4	30
55	images/Tombs_of_Troilus_and_Memnon_Hecuba_and_Paris.max-165x165.jpg	105	165		1	3
56	images/Construction_of_Rome_add_ms_15268_f156r_copy.width-400.jpg	400	340		5	28
57	images/Construction_of_Rome_add_ms_15268_f156r_copy.width-500.jpg	500	425		6	28
58	images/beta_flag.width-500.png	124	125		6	1
59	images/Detail_Jason_and_the_Argonauts_add_ms_15268_f1.width-500.jpg	500	280		6	30
60	images/Theseus_attacking_Crete_add_ms_15268_f136v_cop.width-500.jpg	500	502		6	61
61	images/Jason_and_the_golden_fleece_add_ms_19669_f077r.width-500.jpg	342	295		6	46
62	images/Abraham_and_Isaac_add_ms_15268_f030v_copy.max-165x165.jpg	165	155		1	20
63	images/Troybest_royal_ms_20_d_i_f154r_copy_Kz2s9qC.max-165x165.jpg	107	165		1	13
64	images/Troybest_royal_ms_20_d_i_f154r_copy_CLM5B0h.max-165x165.jpg	107	165		1	11
65	images/Transcription_fr._20125_f._24ra_Z2XPl3Y.max-165x165.jpg	165	123		1	6
66	images/Transcription_fr._20125_f._24ra_WtYzkKI.max-165x165.jpg	165	123		1	5
67	images/Transcription_fr._20125_f._24ra.max-165x165.jpg	165	123		1	4
68	images/Troybest_royal_ms_20_d_i_f154r_copy_W23RQlT.max-165x165.jpg	107	165		1	16
69	images/Troybest_royal_ms_20_d_i_f154r_copy_nE7mrMB.max-165x165.jpg	107	165		1	15
70	images/Troybest_royal_ms_20_d_i_f154r_copy_LiKIwTi.max-165x165.jpg	107	165		1	14
71	images/Troybest_royal_ms_20_d_i_f154r_copy_j3T9vST.max-165x165.jpg	107	165		1	12
72	images/Royal_20_D_I_f._21v.original.png	682	728		3	53
73	images/Troybest_royal_ms_20_d_i_f154r_copy_5PQ0u0Q.max-165x165.jpg	107	165		1	10
75	images/Troybest_royal_ms_20_d_i_f154r_copy_3ZBQ6SF.max-165x165.jpg	107	165		1	9
77	images/Troybest_royal_ms_20_d_i_f154r_copy_1OEb6tm.max-165x165.jpg	107	165		1	8
78	images/Troybest_royal_ms_20_d_i_f154r_copy.max-165x165.jpg	107	165		1	7
80	images/royal_ms_20_d_i_f169r_copy_qddwnv3.width-500.jpg	500	701		6	55
81	images/Theseus_and_the_Giant_royal_ms_20_d_i_f026r_co.width-500.jpg	500	341		6	60
82	images/Creation_add_ms_19669_f004r_copy.original.jpg	1010	1404		3	29
83	images/Temple_of_Janus_with_senators_dining_add_ms_15.width-500.jpg	500	368		6	59
84	images/Einladung-Gastvortrag-Simon-Gaunt_z7NFj65.original.jpg	1240	1754		3	34
85	images/Royal_MS_20_D_I_Wheel_of_Fortune-f.163v.original.png	1063	853		3	56
86	images/Henry_2.width-500.jpg	500	333		6	41
87	images/Detail_of_Troy_royal_ms_20_d_i_f067r_copy.width-500.jpg	491	558		6	31
88	images/fr._20125_f._43v.original.jpg	1626	1549		3	38
89	images/Sheep_Royal_12_F_XIII_f._35r.original.png	770	642		3	57
90	images/fr._20125_f._48v.original.jpg	1424	2387		3	39
91	images/7r_detail.max-165x165.jpg	165	121		1	18
92	images/7r.max-165x165.jpg	114	165		1	17
93	images/18r.max-165x165.jpg	114	165		1	19
94	images/add_15268_1v.max-165x165.jpg	109	165		1	22
95	images/f._20125_88v.original.jpg	1283	1740		3	35
96	images/Add_MS_15268_f._77v.original.png	795	593		3	25
97	images/Noah_and_the_ark_add_ms_15268_f007v_copy.width-500.jpg	500	810		6	50
98	images/7r.original.jpg	1024	1482		3	17
99	images/fr._20125_f._7r_digitisation.original.jpg	1640	919		3	37
100	images/18r.original.jpg	1024	1482		3	19
101	images/Jason_and_the_Argonauts_add_ms_15268_f105v_2_c.width-500.jpg	500	545		6	44
102	images/header.max-165x165.jpg	165	47		1	63
103	images/header.original.jpg	1000	288		3	63
104	images/header.width-1000.jpg	1000	288		8	63
105	images/header.width-2000.jpg	1000	288		9	63
106	images/Construction_of_Rome_add_ms_15268_f156r_copy.original.jpg	608	517		3	28
107	images/Construction_of_Rome_add_ms_15268_f156r_copy.max-800x600.jpg	608	517		4	28
\.


--
-- TOC entry 2332 (class 0 OID 410200)
-- Dependencies: 216
-- Data for Name: wagtailredirects_redirect; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailredirects_redirect (id, old_path, is_permanent, redirect_link, redirect_page_id, site_id) FROM stdin;
\.


--
-- TOC entry 2333 (class 0 OID 410245)
-- Dependencies: 218
-- Data for Name: wagtailsearch_editorspick; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailsearch_editorspick (id, sort_order, description, page_id, query_id) FROM stdin;
\.


--
-- TOC entry 2334 (class 0 OID 410256)
-- Dependencies: 220
-- Data for Name: wagtailsearch_query; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailsearch_query (id, query_string) FROM stdin;
\.


--
-- TOC entry 2335 (class 0 OID 410266)
-- Dependencies: 222
-- Data for Name: wagtailsearch_querydailyhits; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailsearch_querydailyhits (id, date, hits, query_id) FROM stdin;
\.


--
-- TOC entry 2336 (class 0 OID 410300)
-- Dependencies: 224
-- Data for Name: wagtailusers_userprofile; Type: TABLE DATA; Schema: public; Owner: app_tvof
--

COPY wagtailusers_userprofile (id, submitted_notifications, approved_notifications, rejected_notifications, user_id) FROM stdin;
\.


--
-- TOC entry 2110 (class 2606 OID 409607)
-- Dependencies: 168 168
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 2116 (class 2606 OID 409662)
-- Dependencies: 170 170 170
-- Name: auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 2118 (class 2606 OID 409615)
-- Dependencies: 170 170
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2112 (class 2606 OID 409605)
-- Dependencies: 168 168
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 2105 (class 2606 OID 409648)
-- Dependencies: 166 166 166
-- Name: auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 2107 (class 2606 OID 409597)
-- Dependencies: 166 166
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 2127 (class 2606 OID 409633)
-- Dependencies: 174 174
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 2129 (class 2606 OID 409677)
-- Dependencies: 174 174 174
-- Name: auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- TOC entry 2120 (class 2606 OID 409623)
-- Dependencies: 172 172
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2133 (class 2606 OID 409641)
-- Dependencies: 176 176
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2135 (class 2606 OID 409691)
-- Dependencies: 176 176 176
-- Name: auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- TOC entry 2123 (class 2606 OID 409625)
-- Dependencies: 172 172
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 2190 (class 2606 OID 409982)
-- Dependencies: 196 196
-- Name: cms_blogindexpage_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY cms_blogindexpage
    ADD CONSTRAINT cms_blogindexpage_pkey PRIMARY KEY (page_ptr_id);


--
-- TOC entry 2192 (class 2606 OID 409987)
-- Dependencies: 197 197
-- Name: cms_blogpost_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY cms_blogpost
    ADD CONSTRAINT cms_blogpost_pkey PRIMARY KEY (page_ptr_id);


--
-- TOC entry 2184 (class 2606 OID 409946)
-- Dependencies: 193 193
-- Name: cms_homepage_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY cms_homepage
    ADD CONSTRAINT cms_homepage_pkey PRIMARY KEY (page_ptr_id);


--
-- TOC entry 2188 (class 2606 OID 409972)
-- Dependencies: 195 195
-- Name: cms_indexpage_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY cms_indexpage
    ADD CONSTRAINT cms_indexpage_pkey PRIMARY KEY (page_ptr_id);


--
-- TOC entry 2186 (class 2606 OID 409959)
-- Dependencies: 194 194
-- Name: cms_richtextpage_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY cms_richtextpage
    ADD CONSTRAINT cms_richtextpage_pkey PRIMARY KEY (page_ptr_id);


--
-- TOC entry 2139 (class 2606 OID 409705)
-- Dependencies: 178 178
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 2100 (class 2606 OID 409589)
-- Dependencies: 164 164 164
-- Name: django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 2102 (class 2606 OID 409587)
-- Dependencies: 164 164
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 2098 (class 2606 OID 409579)
-- Dependencies: 162 162
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 2195 (class 2606 OID 410005)
-- Dependencies: 198 198
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 2199 (class 2606 OID 410017)
-- Dependencies: 200 200
-- Name: taggit_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_name_key UNIQUE (name);


--
-- TOC entry 2201 (class 2606 OID 410015)
-- Dependencies: 200 200
-- Name: taggit_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_pkey PRIMARY KEY (id);


--
-- TOC entry 2204 (class 2606 OID 410019)
-- Dependencies: 200 200
-- Name: taggit_tag_slug_key; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_slug_key UNIQUE (slug);


--
-- TOC entry 2210 (class 2606 OID 410027)
-- Dependencies: 202 202
-- Name: taggit_taggeditem_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_pkey PRIMARY KEY (id);


--
-- TOC entry 2173 (class 2606 OID 409935)
-- Dependencies: 190 190
-- Name: wagtailcore_collection_path_key; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_collection
    ADD CONSTRAINT wagtailcore_collection_path_key UNIQUE (path);


--
-- TOC entry 2175 (class 2606 OID 409902)
-- Dependencies: 190 190
-- Name: wagtailcore_collection_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_collection
    ADD CONSTRAINT wagtailcore_collection_pkey PRIMARY KEY (id);


--
-- TOC entry 2180 (class 2606 OID 409915)
-- Dependencies: 192 192 192 192
-- Name: wagtailcore_groupcollectionpermission_group_id_a21cefe9_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_groupcollectionpermission
    ADD CONSTRAINT wagtailcore_groupcollectionpermission_group_id_a21cefe9_uniq UNIQUE (group_id, collection_id, permission_id);


--
-- TOC entry 2182 (class 2606 OID 409913)
-- Dependencies: 192 192
-- Name: wagtailcore_groupcollectionpermission_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_groupcollectionpermission
    ADD CONSTRAINT wagtailcore_groupcollectionpermission_pkey PRIMARY KEY (id);


--
-- TOC entry 2153 (class 2606 OID 409757)
-- Dependencies: 182 182 182 182
-- Name: wagtailcore_grouppagepermission_group_id_0898bdf8_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_grouppagepermission
    ADD CONSTRAINT wagtailcore_grouppagepermission_group_id_0898bdf8_uniq UNIQUE (group_id, page_id, permission_type);


--
-- TOC entry 2155 (class 2606 OID 409755)
-- Dependencies: 182 182
-- Name: wagtailcore_grouppagepermission_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_grouppagepermission
    ADD CONSTRAINT wagtailcore_grouppagepermission_pkey PRIMARY KEY (id);


--
-- TOC entry 2146 (class 2606 OID 409747)
-- Dependencies: 180 180
-- Name: wagtailcore_page_path_key; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_page
    ADD CONSTRAINT wagtailcore_page_path_key UNIQUE (path);


--
-- TOC entry 2148 (class 2606 OID 409743)
-- Dependencies: 180 180
-- Name: wagtailcore_page_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_page
    ADD CONSTRAINT wagtailcore_page_pkey PRIMARY KEY (id);


--
-- TOC entry 2159 (class 2606 OID 409768)
-- Dependencies: 184 184
-- Name: wagtailcore_pagerevision_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_pagerevision
    ADD CONSTRAINT wagtailcore_pagerevision_pkey PRIMARY KEY (id);


--
-- TOC entry 2163 (class 2606 OID 409776)
-- Dependencies: 186 186
-- Name: wagtailcore_pageviewrestriction_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_pageviewrestriction
    ADD CONSTRAINT wagtailcore_pageviewrestriction_pkey PRIMARY KEY (id);


--
-- TOC entry 2167 (class 2606 OID 409786)
-- Dependencies: 188 188 188
-- Name: wagtailcore_site_hostname_2c626d70_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_site
    ADD CONSTRAINT wagtailcore_site_hostname_2c626d70_uniq UNIQUE (hostname, port);


--
-- TOC entry 2170 (class 2606 OID 409784)
-- Dependencies: 188 188
-- Name: wagtailcore_site_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailcore_site
    ADD CONSTRAINT wagtailcore_site_pkey PRIMARY KEY (id);


--
-- TOC entry 2214 (class 2606 OID 410051)
-- Dependencies: 204 204
-- Name: wagtaildocs_document_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtaildocs_document
    ADD CONSTRAINT wagtaildocs_document_pkey PRIMARY KEY (id);


--
-- TOC entry 2216 (class 2606 OID 410095)
-- Dependencies: 206 206
-- Name: wagtailembeds_embed_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailembeds_embed
    ADD CONSTRAINT wagtailembeds_embed_pkey PRIMARY KEY (id);


--
-- TOC entry 2218 (class 2606 OID 410097)
-- Dependencies: 206 206 206
-- Name: wagtailembeds_embed_url_8a2922d8_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailembeds_embed
    ADD CONSTRAINT wagtailembeds_embed_url_8a2922d8_uniq UNIQUE (url, max_width);


--
-- TOC entry 2221 (class 2606 OID 410108)
-- Dependencies: 208 208
-- Name: wagtailforms_formsubmission_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailforms_formsubmission
    ADD CONSTRAINT wagtailforms_formsubmission_pkey PRIMARY KEY (id);


--
-- TOC entry 2223 (class 2606 OID 410122)
-- Dependencies: 210 210
-- Name: wagtailimages_filter_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailimages_filter
    ADD CONSTRAINT wagtailimages_filter_pkey PRIMARY KEY (id);


--
-- TOC entry 2225 (class 2606 OID 410167)
-- Dependencies: 210 210
-- Name: wagtailimages_filter_spec_42ad6e02_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailimages_filter
    ADD CONSTRAINT wagtailimages_filter_spec_42ad6e02_uniq UNIQUE (spec);


--
-- TOC entry 2230 (class 2606 OID 410134)
-- Dependencies: 212 212
-- Name: wagtailimages_image_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailimages_image
    ADD CONSTRAINT wagtailimages_image_pkey PRIMARY KEY (id);


--
-- TOC entry 2234 (class 2606 OID 410144)
-- Dependencies: 214 214 214 214
-- Name: wagtailimages_rendition_image_id_03110280_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailimages_rendition
    ADD CONSTRAINT wagtailimages_rendition_image_id_03110280_uniq UNIQUE (image_id, filter_id, focal_point_key);


--
-- TOC entry 2236 (class 2606 OID 410142)
-- Dependencies: 214 214
-- Name: wagtailimages_rendition_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailimages_rendition
    ADD CONSTRAINT wagtailimages_rendition_pkey PRIMARY KEY (id);


--
-- TOC entry 2240 (class 2606 OID 410232)
-- Dependencies: 216 216 216
-- Name: wagtailredirects_redirect_old_path_783622d7_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailredirects_redirect
    ADD CONSTRAINT wagtailredirects_redirect_old_path_783622d7_uniq UNIQUE (old_path, site_id);


--
-- TOC entry 2243 (class 2606 OID 410205)
-- Dependencies: 216 216
-- Name: wagtailredirects_redirect_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailredirects_redirect
    ADD CONSTRAINT wagtailredirects_redirect_pkey PRIMARY KEY (id);


--
-- TOC entry 2247 (class 2606 OID 410253)
-- Dependencies: 218 218
-- Name: wagtailsearch_editorspick_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailsearch_editorspick
    ADD CONSTRAINT wagtailsearch_editorspick_pkey PRIMARY KEY (id);


--
-- TOC entry 2249 (class 2606 OID 410261)
-- Dependencies: 220 220
-- Name: wagtailsearch_query_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailsearch_query
    ADD CONSTRAINT wagtailsearch_query_pkey PRIMARY KEY (id);


--
-- TOC entry 2252 (class 2606 OID 410263)
-- Dependencies: 220 220
-- Name: wagtailsearch_query_query_string_key; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailsearch_query
    ADD CONSTRAINT wagtailsearch_query_query_string_key UNIQUE (query_string);


--
-- TOC entry 2255 (class 2606 OID 410271)
-- Dependencies: 222 222
-- Name: wagtailsearch_querydailyhits_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailsearch_querydailyhits
    ADD CONSTRAINT wagtailsearch_querydailyhits_pkey PRIMARY KEY (id);


--
-- TOC entry 2257 (class 2606 OID 410273)
-- Dependencies: 222 222 222
-- Name: wagtailsearch_querydailyhits_query_id_1dd232e6_uniq; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailsearch_querydailyhits
    ADD CONSTRAINT wagtailsearch_querydailyhits_query_id_1dd232e6_uniq UNIQUE (query_id, date);


--
-- TOC entry 2259 (class 2606 OID 410305)
-- Dependencies: 224 224
-- Name: wagtailusers_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailusers_userprofile
    ADD CONSTRAINT wagtailusers_userprofile_pkey PRIMARY KEY (id);


--
-- TOC entry 2261 (class 2606 OID 410307)
-- Dependencies: 224 224
-- Name: wagtailusers_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: app_tvof; Tablespace: 
--

ALTER TABLE ONLY wagtailusers_userprofile
    ADD CONSTRAINT wagtailusers_userprofile_user_id_key UNIQUE (user_id);


--
-- TOC entry 2108 (class 1259 OID 409650)
-- Dependencies: 168
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 2113 (class 1259 OID 409663)
-- Dependencies: 170
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- TOC entry 2114 (class 1259 OID 409664)
-- Dependencies: 170
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- TOC entry 2103 (class 1259 OID 409649)
-- Dependencies: 166
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- TOC entry 2124 (class 1259 OID 409679)
-- Dependencies: 174
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- TOC entry 2125 (class 1259 OID 409678)
-- Dependencies: 174
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- TOC entry 2130 (class 1259 OID 409693)
-- Dependencies: 176
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 2131 (class 1259 OID 409692)
-- Dependencies: 176
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 2121 (class 1259 OID 409665)
-- Dependencies: 172
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 2136 (class 1259 OID 409716)
-- Dependencies: 178
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- TOC entry 2137 (class 1259 OID 409717)
-- Dependencies: 178
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- TOC entry 2193 (class 1259 OID 410006)
-- Dependencies: 198
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- TOC entry 2196 (class 1259 OID 410007)
-- Dependencies: 198
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 2197 (class 1259 OID 410028)
-- Dependencies: 200
-- Name: taggit_tag_name_58eb2ed9_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX taggit_tag_name_58eb2ed9_like ON taggit_tag USING btree (name varchar_pattern_ops);


--
-- TOC entry 2202 (class 1259 OID 410029)
-- Dependencies: 200
-- Name: taggit_tag_slug_6be58b2c_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX taggit_tag_slug_6be58b2c_like ON taggit_tag USING btree (slug varchar_pattern_ops);


--
-- TOC entry 2205 (class 1259 OID 410041)
-- Dependencies: 202
-- Name: taggit_taggeditem_417f1b1c; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX taggit_taggeditem_417f1b1c ON taggit_taggeditem USING btree (content_type_id);


--
-- TOC entry 2206 (class 1259 OID 410042)
-- Dependencies: 202
-- Name: taggit_taggeditem_76f094bc; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX taggit_taggeditem_76f094bc ON taggit_taggeditem USING btree (tag_id);


--
-- TOC entry 2207 (class 1259 OID 410040)
-- Dependencies: 202
-- Name: taggit_taggeditem_af31437c; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX taggit_taggeditem_af31437c ON taggit_taggeditem USING btree (object_id);


--
-- TOC entry 2208 (class 1259 OID 410043)
-- Dependencies: 202 202
-- Name: taggit_taggeditem_content_type_id_196cc965_idx; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX taggit_taggeditem_content_type_id_196cc965_idx ON taggit_taggeditem USING btree (content_type_id, object_id);


--
-- TOC entry 2171 (class 1259 OID 409936)
-- Dependencies: 190
-- Name: wagtailcore_collection_path_d848dc19_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_collection_path_d848dc19_like ON wagtailcore_collection USING btree (path varchar_pattern_ops);


--
-- TOC entry 2176 (class 1259 OID 409931)
-- Dependencies: 192
-- Name: wagtailcore_groupcollectionpermission_0a1a4dd8; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_groupcollectionpermission_0a1a4dd8 ON wagtailcore_groupcollectionpermission USING btree (collection_id);


--
-- TOC entry 2177 (class 1259 OID 409932)
-- Dependencies: 192
-- Name: wagtailcore_groupcollectionpermission_0e939a4f; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_groupcollectionpermission_0e939a4f ON wagtailcore_groupcollectionpermission USING btree (group_id);


--
-- TOC entry 2178 (class 1259 OID 409933)
-- Dependencies: 192
-- Name: wagtailcore_groupcollectionpermission_8373b171; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_groupcollectionpermission_8373b171 ON wagtailcore_groupcollectionpermission USING btree (permission_id);


--
-- TOC entry 2150 (class 1259 OID 409812)
-- Dependencies: 182
-- Name: wagtailcore_grouppagepermission_0e939a4f; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_grouppagepermission_0e939a4f ON wagtailcore_grouppagepermission USING btree (group_id);


--
-- TOC entry 2151 (class 1259 OID 409813)
-- Dependencies: 182
-- Name: wagtailcore_grouppagepermission_1a63c800; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_grouppagepermission_1a63c800 ON wagtailcore_grouppagepermission USING btree (page_id);


--
-- TOC entry 2140 (class 1259 OID 409797)
-- Dependencies: 180
-- Name: wagtailcore_page_2dbcba41; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_page_2dbcba41 ON wagtailcore_page USING btree (slug);


--
-- TOC entry 2141 (class 1259 OID 409798)
-- Dependencies: 180
-- Name: wagtailcore_page_417f1b1c; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_page_417f1b1c ON wagtailcore_page USING btree (content_type_id);


--
-- TOC entry 2142 (class 1259 OID 409799)
-- Dependencies: 180
-- Name: wagtailcore_page_5e7b1936; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_page_5e7b1936 ON wagtailcore_page USING btree (owner_id);


--
-- TOC entry 2143 (class 1259 OID 409841)
-- Dependencies: 180
-- Name: wagtailcore_page_first_published_at_2b5dd637_uniq; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_page_first_published_at_2b5dd637_uniq ON wagtailcore_page USING btree (first_published_at);


--
-- TOC entry 2144 (class 1259 OID 409800)
-- Dependencies: 180
-- Name: wagtailcore_page_path_98eba2c8_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_page_path_98eba2c8_like ON wagtailcore_page USING btree (path varchar_pattern_ops);


--
-- TOC entry 2149 (class 1259 OID 409801)
-- Dependencies: 180
-- Name: wagtailcore_page_slug_e7c11b8f_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_page_slug_e7c11b8f_like ON wagtailcore_page USING btree (slug varchar_pattern_ops);


--
-- TOC entry 2156 (class 1259 OID 409824)
-- Dependencies: 184
-- Name: wagtailcore_pagerevision_1a63c800; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_pagerevision_1a63c800 ON wagtailcore_pagerevision USING btree (page_id);


--
-- TOC entry 2157 (class 1259 OID 409825)
-- Dependencies: 184
-- Name: wagtailcore_pagerevision_e8701ad4; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_pagerevision_e8701ad4 ON wagtailcore_pagerevision USING btree (user_id);


--
-- TOC entry 2160 (class 1259 OID 409840)
-- Dependencies: 184
-- Name: wagtailcore_pagerevision_submitted_for_moderation_c682e44c_uniq; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_pagerevision_submitted_for_moderation_c682e44c_uniq ON wagtailcore_pagerevision USING btree (submitted_for_moderation);


--
-- TOC entry 2161 (class 1259 OID 409831)
-- Dependencies: 186
-- Name: wagtailcore_pageviewrestriction_1a63c800; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_pageviewrestriction_1a63c800 ON wagtailcore_pageviewrestriction USING btree (page_id);


--
-- TOC entry 2164 (class 1259 OID 409837)
-- Dependencies: 188
-- Name: wagtailcore_site_0897acf4; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_site_0897acf4 ON wagtailcore_site USING btree (hostname);


--
-- TOC entry 2165 (class 1259 OID 409838)
-- Dependencies: 188
-- Name: wagtailcore_site_8372b497; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_site_8372b497 ON wagtailcore_site USING btree (root_page_id);


--
-- TOC entry 2168 (class 1259 OID 409839)
-- Dependencies: 188
-- Name: wagtailcore_site_hostname_96b20b46_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailcore_site_hostname_96b20b46_like ON wagtailcore_site USING btree (hostname varchar_pattern_ops);


--
-- TOC entry 2211 (class 1259 OID 410074)
-- Dependencies: 204
-- Name: wagtaildocs_document_0a1a4dd8; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtaildocs_document_0a1a4dd8 ON wagtaildocs_document USING btree (collection_id);


--
-- TOC entry 2212 (class 1259 OID 410057)
-- Dependencies: 204
-- Name: wagtaildocs_document_ef01e2b6; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtaildocs_document_ef01e2b6 ON wagtaildocs_document USING btree (uploaded_by_user_id);


--
-- TOC entry 2219 (class 1259 OID 410114)
-- Dependencies: 208
-- Name: wagtailforms_formsubmission_1a63c800; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailforms_formsubmission_1a63c800 ON wagtailforms_formsubmission USING btree (page_id);


--
-- TOC entry 2226 (class 1259 OID 410192)
-- Dependencies: 212
-- Name: wagtailimages_image_0a1a4dd8; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailimages_image_0a1a4dd8 ON wagtailimages_image USING btree (collection_id);


--
-- TOC entry 2227 (class 1259 OID 410174)
-- Dependencies: 212
-- Name: wagtailimages_image_created_at_86fa6cd4_uniq; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailimages_image_created_at_86fa6cd4_uniq ON wagtailimages_image USING btree (created_at);


--
-- TOC entry 2228 (class 1259 OID 410152)
-- Dependencies: 212
-- Name: wagtailimages_image_ef01e2b6; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailimages_image_ef01e2b6 ON wagtailimages_image USING btree (uploaded_by_user_id);


--
-- TOC entry 2231 (class 1259 OID 410163)
-- Dependencies: 214
-- Name: wagtailimages_rendition_0a317463; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailimages_rendition_0a317463 ON wagtailimages_rendition USING btree (filter_id);


--
-- TOC entry 2232 (class 1259 OID 410164)
-- Dependencies: 214
-- Name: wagtailimages_rendition_f33175e6; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailimages_rendition_f33175e6 ON wagtailimages_rendition USING btree (image_id);


--
-- TOC entry 2237 (class 1259 OID 410218)
-- Dependencies: 216
-- Name: wagtailredirects_redirect_2fd79f37; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailredirects_redirect_2fd79f37 ON wagtailredirects_redirect USING btree (redirect_page_id);


--
-- TOC entry 2238 (class 1259 OID 410219)
-- Dependencies: 216
-- Name: wagtailredirects_redirect_9365d6e7; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailredirects_redirect_9365d6e7 ON wagtailredirects_redirect USING btree (site_id);


--
-- TOC entry 2241 (class 1259 OID 410220)
-- Dependencies: 216
-- Name: wagtailredirects_redirect_old_path_bb35247b_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailredirects_redirect_old_path_bb35247b_like ON wagtailredirects_redirect USING btree (old_path varchar_pattern_ops);


--
-- TOC entry 2244 (class 1259 OID 410287)
-- Dependencies: 218
-- Name: wagtailsearch_editorspick_0bbeda9c; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailsearch_editorspick_0bbeda9c ON wagtailsearch_editorspick USING btree (query_id);


--
-- TOC entry 2245 (class 1259 OID 410279)
-- Dependencies: 218
-- Name: wagtailsearch_editorspick_1a63c800; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailsearch_editorspick_1a63c800 ON wagtailsearch_editorspick USING btree (page_id);


--
-- TOC entry 2250 (class 1259 OID 410280)
-- Dependencies: 220
-- Name: wagtailsearch_query_query_string_e785ea07_like; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailsearch_query_query_string_e785ea07_like ON wagtailsearch_query USING btree (query_string varchar_pattern_ops);


--
-- TOC entry 2253 (class 1259 OID 410286)
-- Dependencies: 222
-- Name: wagtailsearch_querydailyhits_0bbeda9c; Type: INDEX; Schema: public; Owner: app_tvof; Tablespace: 
--

CREATE INDEX wagtailsearch_querydailyhits_0bbeda9c ON wagtailsearch_querydailyhits USING btree (query_id);


--
-- TOC entry 2264 (class 2606 OID 409656)
-- Dependencies: 2106 166 170
-- Name: auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2263 (class 2606 OID 409651)
-- Dependencies: 170 168 2111
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2262 (class 2606 OID 409642)
-- Dependencies: 2101 164 166
-- Name: auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2266 (class 2606 OID 409671)
-- Dependencies: 174 168 2111
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2265 (class 2606 OID 409666)
-- Dependencies: 172 174 2119
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2268 (class 2606 OID 409685)
-- Dependencies: 176 166 2106
-- Name: auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2267 (class 2606 OID 409680)
-- Dependencies: 2119 176 172
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2285 (class 2606 OID 409988)
-- Dependencies: 180 2147 196
-- Name: cms_blogindexpage_page_ptr_id_1391b50a_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY cms_blogindexpage
    ADD CONSTRAINT cms_blogindexpage_page_ptr_id_1391b50a_fk_wagtailcore_page_id FOREIGN KEY (page_ptr_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2286 (class 2606 OID 409993)
-- Dependencies: 197 180 2147
-- Name: cms_blogpost_page_ptr_id_119a50c7_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY cms_blogpost
    ADD CONSTRAINT cms_blogpost_page_ptr_id_119a50c7_fk_wagtailcore_page_id FOREIGN KEY (page_ptr_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2282 (class 2606 OID 409947)
-- Dependencies: 180 193 2147
-- Name: cms_homepage_page_ptr_id_3967ea6a_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY cms_homepage
    ADD CONSTRAINT cms_homepage_page_ptr_id_3967ea6a_fk_wagtailcore_page_id FOREIGN KEY (page_ptr_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2284 (class 2606 OID 409973)
-- Dependencies: 2147 195 180
-- Name: cms_indexpage_page_ptr_id_66d6c698_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY cms_indexpage
    ADD CONSTRAINT cms_indexpage_page_ptr_id_66d6c698_fk_wagtailcore_page_id FOREIGN KEY (page_ptr_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2283 (class 2606 OID 409960)
-- Dependencies: 194 180 2147
-- Name: cms_richtextpage_page_ptr_id_eb2bfc13_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY cms_richtextpage
    ADD CONSTRAINT cms_richtextpage_page_ptr_id_eb2bfc13_fk_wagtailcore_page_id FOREIGN KEY (page_ptr_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2269 (class 2606 OID 409706)
-- Dependencies: 164 2101 178
-- Name: django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2270 (class 2606 OID 409711)
-- Dependencies: 178 172 2119
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2287 (class 2606 OID 410030)
-- Dependencies: 2101 202 164
-- Name: taggit_tagge_content_type_id_9957a03c_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_tagge_content_type_id_9957a03c_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2288 (class 2606 OID 410035)
-- Dependencies: 200 202 2200
-- Name: taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id FOREIGN KEY (tag_id) REFERENCES taggit_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2272 (class 2606 OID 409937)
-- Dependencies: 2101 180 164
-- Name: wagtailcore__content_type_id_c28424df_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_page
    ADD CONSTRAINT wagtailcore__content_type_id_c28424df_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2279 (class 2606 OID 409916)
-- Dependencies: 192 190 2174
-- Name: wagtailcore_collection_id_5423575a_fk_wagtailcore_collection_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_groupcollectionpermission
    ADD CONSTRAINT wagtailcore_collection_id_5423575a_fk_wagtailcore_collection_id FOREIGN KEY (collection_id) REFERENCES wagtailcore_collection(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2281 (class 2606 OID 409926)
-- Dependencies: 192 2106 166
-- Name: wagtailcore_groupc_permission_id_1b626275_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_groupcollectionpermission
    ADD CONSTRAINT wagtailcore_groupc_permission_id_1b626275_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2280 (class 2606 OID 409921)
-- Dependencies: 2111 168 192
-- Name: wagtailcore_groupcollectionp_group_id_05d61460_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_groupcollectionpermission
    ADD CONSTRAINT wagtailcore_groupcollectionp_group_id_05d61460_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2274 (class 2606 OID 409847)
-- Dependencies: 2147 180 182
-- Name: wagtailcore_grouppagepe_page_id_710b114a_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_grouppagepermission
    ADD CONSTRAINT wagtailcore_grouppagepe_page_id_710b114a_fk_wagtailcore_page_id FOREIGN KEY (page_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2273 (class 2606 OID 409842)
-- Dependencies: 182 168 2111
-- Name: wagtailcore_grouppagepermiss_group_id_fc07e671_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_grouppagepermission
    ADD CONSTRAINT wagtailcore_grouppagepermiss_group_id_fc07e671_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2271 (class 2606 OID 409857)
-- Dependencies: 180 2119 172
-- Name: wagtailcore_page_owner_id_fbf7c332_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_page
    ADD CONSTRAINT wagtailcore_page_owner_id_fbf7c332_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2275 (class 2606 OID 409862)
-- Dependencies: 184 180 2147
-- Name: wagtailcore_pagerevisio_page_id_d421cc1d_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_pagerevision
    ADD CONSTRAINT wagtailcore_pagerevisio_page_id_d421cc1d_fk_wagtailcore_page_id FOREIGN KEY (page_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2276 (class 2606 OID 409885)
-- Dependencies: 2119 172 184
-- Name: wagtailcore_pagerevision_user_id_2409d2f4_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_pagerevision
    ADD CONSTRAINT wagtailcore_pagerevision_user_id_2409d2f4_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2277 (class 2606 OID 409872)
-- Dependencies: 2147 186 180
-- Name: wagtailcore_pageviewres_page_id_15a8bea6_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_pageviewrestriction
    ADD CONSTRAINT wagtailcore_pageviewres_page_id_15a8bea6_fk_wagtailcore_page_id FOREIGN KEY (page_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2278 (class 2606 OID 409877)
-- Dependencies: 2147 188 180
-- Name: wagtailcore_site_root_page_id_e02fb95c_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailcore_site
    ADD CONSTRAINT wagtailcore_site_root_page_id_e02fb95c_fk_wagtailcore_page_id FOREIGN KEY (root_page_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2289 (class 2606 OID 410075)
-- Dependencies: 204 2174 190
-- Name: wagtaildocs_collection_id_23881625_fk_wagtailcore_collection_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtaildocs_document
    ADD CONSTRAINT wagtaildocs_collection_id_23881625_fk_wagtailcore_collection_id FOREIGN KEY (collection_id) REFERENCES wagtailcore_collection(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2290 (class 2606 OID 410080)
-- Dependencies: 204 2119 172
-- Name: wagtaildocs_docume_uploaded_by_user_id_17258b41_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtaildocs_document
    ADD CONSTRAINT wagtaildocs_docume_uploaded_by_user_id_17258b41_fk_auth_user_id FOREIGN KEY (uploaded_by_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2291 (class 2606 OID 410109)
-- Dependencies: 208 180 2147
-- Name: wagtailforms_formsubmis_page_id_e48e93e7_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailforms_formsubmission
    ADD CONSTRAINT wagtailforms_formsubmis_page_id_e48e93e7_fk_wagtailcore_page_id FOREIGN KEY (page_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2293 (class 2606 OID 410193)
-- Dependencies: 212 2174 190
-- Name: wagtailimag_collection_id_c2f8af7e_fk_wagtailcore_collection_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailimages_image
    ADD CONSTRAINT wagtailimag_collection_id_c2f8af7e_fk_wagtailcore_collection_id FOREIGN KEY (collection_id) REFERENCES wagtailcore_collection(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2292 (class 2606 OID 410180)
-- Dependencies: 212 172 2119
-- Name: wagtailimages_imag_uploaded_by_user_id_5d73dc75_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailimages_image
    ADD CONSTRAINT wagtailimages_imag_uploaded_by_user_id_5d73dc75_fk_auth_user_id FOREIGN KEY (uploaded_by_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2294 (class 2606 OID 410153)
-- Dependencies: 210 2222 214
-- Name: wagtailimages_ren_filter_id_7fc52567_fk_wagtailimages_filter_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailimages_rendition
    ADD CONSTRAINT wagtailimages_ren_filter_id_7fc52567_fk_wagtailimages_filter_id FOREIGN KEY (filter_id) REFERENCES wagtailimages_filter(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2295 (class 2606 OID 410158)
-- Dependencies: 212 2229 214
-- Name: wagtailimages_rendi_image_id_3e1fd774_fk_wagtailimages_image_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailimages_rendition
    ADD CONSTRAINT wagtailimages_rendi_image_id_3e1fd774_fk_wagtailimages_image_id FOREIGN KEY (image_id) REFERENCES wagtailimages_image(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2296 (class 2606 OID 410233)
-- Dependencies: 2147 180 216
-- Name: wagtailredirec_redirect_page_id_b5728a8f_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailredirects_redirect
    ADD CONSTRAINT wagtailredirec_redirect_page_id_b5728a8f_fk_wagtailcore_page_id FOREIGN KEY (redirect_page_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2297 (class 2606 OID 410238)
-- Dependencies: 2169 216 188
-- Name: wagtailredirects_redire_site_id_780a0e1e_fk_wagtailcore_site_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailredirects_redirect
    ADD CONSTRAINT wagtailredirects_redire_site_id_780a0e1e_fk_wagtailcore_site_id FOREIGN KEY (site_id) REFERENCES wagtailcore_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2298 (class 2606 OID 410288)
-- Dependencies: 2248 220 218
-- Name: wagtailsearch_edito_query_id_c6eee4a0_fk_wagtailsearch_query_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailsearch_editorspick
    ADD CONSTRAINT wagtailsearch_edito_query_id_c6eee4a0_fk_wagtailsearch_query_id FOREIGN KEY (query_id) REFERENCES wagtailsearch_query(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2299 (class 2606 OID 410293)
-- Dependencies: 2147 218 180
-- Name: wagtailsearch_editorspi_page_id_28cbc274_fk_wagtailcore_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailsearch_editorspick
    ADD CONSTRAINT wagtailsearch_editorspi_page_id_28cbc274_fk_wagtailcore_page_id FOREIGN KEY (page_id) REFERENCES wagtailcore_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2300 (class 2606 OID 410281)
-- Dependencies: 220 2248 222
-- Name: wagtailsearch_query_query_id_2185994b_fk_wagtailsearch_query_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailsearch_querydailyhits
    ADD CONSTRAINT wagtailsearch_query_query_id_2185994b_fk_wagtailsearch_query_id FOREIGN KEY (query_id) REFERENCES wagtailsearch_query(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2301 (class 2606 OID 410308)
-- Dependencies: 172 224 2119
-- Name: wagtailusers_userprofile_user_id_59c92331_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app_tvof
--

ALTER TABLE ONLY wagtailusers_userprofile
    ADD CONSTRAINT wagtailusers_userprofile_user_id_59c92331_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2341 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: app_tvof
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM app_tvof;
GRANT ALL ON SCHEMA public TO app_tvof;


-- Completed on 2016-06-29 15:13:09

--
-- PostgreSQL database dump complete
--


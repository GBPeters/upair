-- Table: public.rtflightpaths

-- DROP TABLE public.rtflightpaths;

CREATE TABLE public.rtflightpaths
(
  id bigserial NOT NULL,
  icao24 character(6),
  callsign character varying(15),
  geom geometry,
  CONSTRAINT rtflightpaths_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.rtflightpaths
  OWNER TO postgres;

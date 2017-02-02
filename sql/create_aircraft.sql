-- Table: public.aircraft

-- DROP TABLE public.aircraft;

CREATE TABLE public.aircraft
(
  id bigserial NOT NULL,
  icao24 character(6),
  registration character varying(10),
  icaotype character varying(15),
  type character varying(40),
  serial character varying(40),
  operator character varying(40),
  icaooperator character varying(40),
  suboperator character varying(40),
  CONSTRAINT aircraft_pkey PRIMARY KEY (id),
  CONSTRAINT aircraft_icao24_key UNIQUE (icao24)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.aircraft
  OWNER TO teammaja;

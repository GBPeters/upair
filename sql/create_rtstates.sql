-- Table: public.rtstates

-- DROP TABLE public.rtstates;

CREATE TABLE public.rtstates
(
  id bigserial NOT NULL,
  response_id bigint,
  icao24 character(6) NOT NULL,
  callsign character varying(15),
  origin_country character varying(50),
  time_position bigint,
  time_velocity bigint,
  longitude double precision,
  latitude double precision,
  altitude double precision,
  on_ground boolean,
  velocity double precision,
  heading double precision,
  vertical_rate double precision,
  atrisk boolean,
  CONSTRAINT rtstates_pkey PRIMARY KEY (id),
  CONSTRAINT rtstates_response_id_icao24_key UNIQUE (response_id, icao24)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.rtstates
  OWNER TO teammaja;

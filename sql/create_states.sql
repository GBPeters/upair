-- Table: public.states

-- DROP TABLE public.states;

CREATE TABLE public.states
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
  CONSTRAINT states_pkey PRIMARY KEY (id),
  CONSTRAINT states_response_id_icao24_key UNIQUE (response_id, icao24)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.states
  OWNER TO postgres;

-- Index: public.states_response_id_idx

-- DROP INDEX public.states_response_id_idx;

CREATE INDEX states_response_id_idx
  ON public.states
  USING btree
  (response_id);


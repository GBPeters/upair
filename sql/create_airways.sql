-- Table: public.airways

-- DROP TABLE public.airways;

CREATE TABLE public.airways
(
  id bigserial NOT NULL,
  geom geometry,
  CONSTRAINT airways_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.airways
  OWNER TO teammaja;

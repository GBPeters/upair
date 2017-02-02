-- Table: public.responses

-- DROP TABLE public.responses;

CREATE TABLE public.responses
(
  id bigserial NOT NULL,
  "time" bigint NOT NULL,
  CONSTRAINT responses_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.responses
  OWNER TO postgres;

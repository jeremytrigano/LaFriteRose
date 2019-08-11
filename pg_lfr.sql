CREATE TABLE lafriterose.centre(
	id_c serial PRIMARY KEY,
	nom character varying(50) NOT NULL,
	adresse character varying(250) NOT NULL,
	code_postal integer,
	ville character varying(200) NOT NULL,
	region character varying(100) NOT NULL,
	pays character varying(150) NOT NULL,
	nom_image character varying(20);
);

CREATE TABLE lafriterose.animateur(
	id_a serial PRIMARY KEY,
	nom character varying(50) NOT NULL,
	prenom character varying(50) NOT NULL,
	grade character varying(20)
);

CREATE TABLE lafriterose.vacancier(
	id_v serial PRIMARY KEY,
	nom character varying(50) NOT NULL,
	prenom character varying(50) NOT NULL,
	date_de_naissance date NOT NULL,
	statut character varying(10) NOT NULL
);

CREATE TABLE lafriterose.animation(
	id_an serial PRIMARY KEY,
	intitule character varying(100) NOT NULL,
	saison character varying(30) NOT NULL
);

CREATE TABLE lafriterose.planning(
	id_p serial PRIMARY KEY,
	date_debut timestamp NOT NULL,
	date_fin timestamp NOT NULL,
	id_an serial NOT NULL CONSTRAINT fk_id_an REFERENCES lafriterose.animation (id_an),
	id_c serial NOT NULL CONSTRAINT fk_id_c REFERENCES lafriterose.centre (id_c)
);

CREATE TABLE lafriterose.employer(
	id_c serial, CONSTRAINT fk_id_c FOREIGN KEY (id_c) REFERENCES lafriterose.centre(id_c),
	id_ar serial, CONSTRAINT fk_id_ar FOREIGN KEY (id_ar) REFERENCES lafriterose.animateur(id_ar),
	CONSTRAINT id_e PRIMARY KEY (id_c,id_ar)
);

CREATE TABLE lafriterose.reserver(
	id_v serial, CONSTRAINT fk_id_v FOREIGN KEY (id_v) REFERENCES lafriterose.vacancier(id_v),
	id_c serial, CONSTRAINT fk_id_c FOREIGN KEY (id_c) REFERENCES lafriterose.centre(id_c),
	date_debut timestamp NOT NULL,
	date_fin timestamp NOT NULL,
	CONSTRAINT id_r PRIMARY KEY (id_v,id_c)
);

CREATE TABLE lafriterose.animer(
	id_ar serial, CONSTRAINT fk_id_ar FOREIGN KEY (id_ar) REFERENCES lafriterose.animateur(id_ar),
	id_p serial, CONSTRAINT fk_id_p FOREIGN KEY (id_p) REFERENCES lafriterose.planning(id_p),
	CONSTRAINT id_am PRIMARY KEY (id_ar,id_p)
);

CREATE TABLE lafriterose.inscrire(
	id_v serial, CONSTRAINT fk_id_v FOREIGN KEY (id_v) REFERENCES lafriterose.vacancier(id_v),
	id_p serial, CONSTRAINT fk_id_p FOREIGN KEY (id_p) REFERENCES lafriterose.planning(id_p),
	CONSTRAINT id_i PRIMARY KEY (id_v,id_p)
);

CREATE TABLE lafriterose.proposer(
	id_c serial, CONSTRAINT fk_id_c FOREIGN KEY (id_c) REFERENCES lafriterose.centre(id_c),
	id_an serial, CONSTRAINT fk_id_an FOREIGN KEY (id_an) REFERENCES lafriterose.animation(id_an),
	CONSTRAINT id_pr PRIMARY KEY (id_c,id_an)
);
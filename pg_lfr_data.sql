SET CLIENT_ENCODING TO 'UTF-8';
SET DATESTYLE = SQL, DMY;

INSERT INTO centre (nom, adresse, code_postal, ville, region, pays, nom_image) VALUES
('Opio en Provence', 'Chemin Cambarnier-Nord', '06650', 'Opio','Alpes Maritimes', 'France', 'opio.jpg'),
('La Palmyre Atlantique', 'Allée du grand large La Palmyre', '17570', 'La Palmyre-Les Mathes','Poitou-Charentes', 'France', null),
('Rêv''hôtel', 'Plage d''Acharavi', '49100', 'Acharavi', 'Corfu', 'Grèce', null),
('L''idylle Arena', 'Viale Spartivento', '09010', 'Domus De Maria', 'Sardaigne', 'Italie', 'domus.jpg'),
('Lice Paradise', 'Route de la Côté 2000', '74120', 'Megève', 'Auvergne-Rhône-Alpes', 'France', 'megeve.jpg'),
('Vishnu Home', 'Jl. Raya Nusa Dua Selatan', '80363', 'Kabupaten Badung','Bali', 'Indonésie', 'bali.jpg');

INSERT INTO vacancier (nom, prenom, date_de_naissance, statut) VALUES
('Annaesky', 'Mario', '06/07/1985', 'VIP'),
('Guldich', 'Octave', '04/11/1978', 'VIP');

INSERT INTO animateur (nom,prenom) VALUES
('Noah','MacLittis'),
('Pyer','Emann');

INSERT INTO animation (intitule, saison) VALUES
('Plongée','printemps,été,automne,hiver'),
('Escalade','printemps,été'),
('Ski','hiver');

INSERT INTO employer (id_c,id_ar) VALUES
(1,1),
(1,2),
(2,2);

INSERT INTO planning (date_debut, date_fin, id_an, id_c) VALUES
('2019-02-15 09:00:00-00', '2019-02-15 12:00:00-00', 3, 5);

INSERT INTO proposer (id_c, id_an) VALUES
(5, 3),
(4, 1),
(4, 2);
SET CLIENT_ENCODING TO 'UTF-8';
SET DATESTYLE = SQL, DMY;

INSERT INTO centre (nom, adresse, code_postal, ville, region, pays) 
VALUES ('Opio en Provence', 'Chemin Cambarnier-Nord', '06650', 'Opio','Alpes Maritimes', 'France');
INSERT INTO centre (nom, adresse, code_postal, ville, region, pays) 
VALUES ('La Palmyre Atlantique', 'Allée du grand large La Palmyre', '17570', 'La Palmyre-Les Mathes','Poitou-Charentes', 'France');
INSERT INTO centre (nom, adresse, code_postal, ville, region, pays)
VALUES ('Rêv''hôtel', 'Plage d''Acharavi', '49100', 'Acharavi', 'Corfu', 'Grèce');
INSERT INTO centre (nom, adresse, code_postal, ville, region, pays)
VALUES ('L''idylle Arena', 'Viale Spartivento', '09010', 'Domus De Maria', 'Sardaigne', 'Italie');

INSERT INTO vacancier (nom, prenom, date_de_naissance, statut)
VALUES ('Annaesky', 'Mario', '06/07/1985', 'VIP');

INSERT INTO animateur (nom,prenom) VALUES ('Noah','MacLittis');
INSERT INTO animateur (nom,prenom) VALUES ('Pyer','Emann');

INSERT INTO employer (id_c,id_ar) VALUES (1,1);
INSERT INTO employer (id_c,id_ar) VALUES (1,2);
INSERT INTO employer (id_c,id_ar) VALUES (2,2);
INSERT INTO CORE_ROLE (name) VALUES ('client');
INSERT INTO CORE_ROLE (name) VALUES ('administrator');

INSERT INTO CORE_CATEGORY (name) VALUES ('Collares');
INSERT INTO CORE_CATEGORY (name) VALUES ('Juguetes');
INSERT INTO CORE_CATEGORY (name) VALUES ('Alimento');

INSERT INTO CORE_DISTRICT (name) VALUES ('Cerrillos');
INSERT INTO CORE_DISTRICT (name) VALUES ('Cerro Navia');
INSERT INTO CORE_DISTRICT (name) VALUES ('Conchalí');
INSERT INTO CORE_DISTRICT (name) VALUES ('El Bosque');
INSERT INTO CORE_DISTRICT (name) VALUES ('Estación Central');
INSERT INTO CORE_DISTRICT (name) VALUES ('Huechuraba');
INSERT INTO CORE_DISTRICT (name) VALUES ('Independencia');
INSERT INTO CORE_DISTRICT (name) VALUES ('La Cisterna');
INSERT INTO CORE_DISTRICT (name) VALUES ('La Florida');
INSERT INTO CORE_DISTRICT (name) VALUES ('La Granja');
INSERT INTO CORE_DISTRICT (name) VALUES ('La Pintana');
INSERT INTO CORE_DISTRICT (name) VALUES ('La Reina');
INSERT INTO CORE_DISTRICT (name) VALUES ('Las Condes');
INSERT INTO CORE_DISTRICT (name) VALUES ('Lo Barnechea');
INSERT INTO CORE_DISTRICT (name) VALUES ('Lo Espejo');
INSERT INTO CORE_DISTRICT (name) VALUES ('Lo Prado');
INSERT INTO CORE_DISTRICT (name) VALUES ('Macul');
INSERT INTO CORE_DISTRICT (name) VALUES ('Maipú');
INSERT INTO CORE_DISTRICT (name) VALUES ('Ñuñoa');
INSERT INTO CORE_DISTRICT (name) VALUES ('Pedro Aguirre Cerda');
INSERT INTO CORE_DISTRICT (name) VALUES ('Peñalolén');
INSERT INTO CORE_DISTRICT (name) VALUES ('Providencia');
INSERT INTO CORE_DISTRICT (name) VALUES ('Pudahuel');
INSERT INTO CORE_DISTRICT (name) VALUES ('Quilicura');
INSERT INTO CORE_DISTRICT (name) VALUES ('Quinta Normal');
INSERT INTO CORE_DISTRICT (name) VALUES ('Recoleta');
INSERT INTO CORE_DISTRICT (name) VALUES ('Renca');
INSERT INTO CORE_DISTRICT (name) VALUES ('San Joaquín');
INSERT INTO CORE_DISTRICT (name) VALUES ('San Miguel');
INSERT INTO CORE_DISTRICT (name) VALUES ('San Ramón');
INSERT INTO CORE_DISTRICT (name) VALUES ('Santiago');
INSERT INTO CORE_DISTRICT (name) VALUES ('Vitacura');

INSERT INTO CORE_SECQUESTION (question) VALUES ('¿Ciudad de nacimiento?');
INSERT INTO CORE_SECQUESTION (question) VALUES ('¿Nombre de su primera mascota?');
INSERT INTO CORE_SECQUESTION (question) VALUES ('¿Segundo apellido de su madre?');
INSERT INTO CORE_SECQUESTION (question) VALUES ('¿Número de hermanos/as mayores?');

INSERT INTO CORE_USER (rut, name, surname, mail, phone, password, role, secQuestion, secAnswer) VALUES ('10.000.000-0', 'William', 'Hartnell', 'whart@mail.com', '+123456789', 'pass', 1, 4, '13');
INSERT INTO CORE_USER (rut, name, surname, mail, phone, password, role, secQuestion, secAnswer) VALUES ('11.000.000-0', 'Patrick', 'Troughton', 'ptrou@mail.com', '+234567891', 'pass', 1, 4, '12');
INSERT INTO CORE_USER (rut, name, surname, mail, phone, password, role, secQuestion, secAnswer) VALUES ('12.000.000-0', 'Jon', 'Pertwee', 'jpert@mail.com', '+345678912', 'pass', 1, 4, '11');
INSERT INTO CORE_USER (rut, name, surname, mail, phone, password, role, secQuestion, secAnswer) VALUES ('13.000.000-0', 'Tom', 'Baker', 'tbake@mail.com', '+456789123', 'pass', 1, 4, '10');

INSERT INTO CORE_USER (rut, name, surname, mail, phone, password, role, secQuestion, secAnswer) VALUES ('20.000.000-0', 'Alvis', 'Claus', 'aclau@mail.com', '+987654321', 'pass', 2, 2, 'Kermit');
INSERT INTO CORE_USER (rut, name, surname, mail, phone, password, role, secQuestion, secAnswer) VALUES ('21.000.000-0', 'Ruby', 'Rose', 'rrose@mail.com', '+876543219', 'pass', 2, 1, 'NJ');

INSERT INTO CORE_ADDRESS (street, number, postalCode, user, district) VALUES ('Av. Enida', '123', '600345', 1, 1);
INSERT INTO CORE_ADDRESS (street, number, postalCode, user, district) VALUES ('Av. Siempreviva', '644', '530345', 1, 2);
INSERT INTO CORE_ADDRESS (street, number, postalCode, user, district) VALUES ('Los Aromos', '413-B', '332345', 2, 3);
INSERT INTO CORE_ADDRESS (street, number, postalCode, user, district) VALUES ('Los Naranjos', '166', '600123', 2, 4);
INSERT INTO CORE_ADDRESS (street, number, postalCode, user, district) VALUES ('Los Manzanos', '35-B', '987252', 3, 5);
INSERT INTO CORE_ADDRESS (street, number, postalCode, user, district) VALUES ('Los Plátanos', '13', '512312', 4, 6);
INSERT INTO CORE_ADDRESS (street, number, postalCode, user, district) VALUES ('Av. Italia', '61', '848455', 5, 7);
INSERT INTO CORE_ADDRESS (street, number, postalCode, user, district) VALUES ('Los Perales', '77-A', '111455', 6, 8);

INSERT INTO CORE_SALE (saleDate, deliveryDate, status, total, user, address, subscribed) VALUES (TO_DATE('2023/01/01 21:02:44', 'yyyy/mm/dd hh24:mi:ss'),TO_DATE('2023/01/10 11:31:24', 'yyyy/mm/dd hh24:mi:ss'), 'Completada', 7200, 1, 1, FALSE);
INSERT INTO CORE_SALE (saleDate, deliveryDate, status, total, user, address, subscribed) VALUES (TO_DATE('2023/02/02 19:32:24', 'yyyy/mm/dd hh24:mi:ss'), 'Carrito', 5800, 1, 1, FALSE);
INSERT INTO CORE_SALE (saleDate, deliveryDate, status, total, user, address, subscribed) VALUES (TO_DATE('2023/03/03 17:42:54', 'yyyy/mm/dd hh24:mi:ss'), 'Despachada', 4200, 1, 2, FALSE);
INSERT INTO CORE_SALE (saleDate, deliveryDate, status, total, user, address, subscribed) VALUES (TO_DATE('2023/04/04 16:22:43', 'yyyy/mm/dd hh24:mi:ss'), 'Pagada', 4200, 2, 3, FALSE);
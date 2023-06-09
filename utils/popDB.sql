DELETE FROM CORE_ROLE;
DELETE FROM CORE_CATEGORY;
DELETE FROM CORE_DISTRICT;
DELETE FROM CORE_SECQUESTION;
DELETE FROM CORE_USER;
DELETE FROM CORE_ADDRESS;
DELETE FROM CORE_SALE;

INSERT INTO CORE_ROLE (id,name) VALUES (1,'client');
INSERT INTO CORE_ROLE (id,name) VALUES (2,'administrator');

INSERT INTO CORE_CATEGORY (name,is_active) VALUES ('Collares',1);
INSERT INTO CORE_CATEGORY (name,is_active) VALUES ('Alimento',1);
INSERT INTO CORE_CATEGORY (name,is_active) VALUES ('Juguetes',1);

INSERT INTO CORE_DISTRICT (id,name) VALUES (1,'Cerrillos');
INSERT INTO CORE_DISTRICT (id,name) VALUES (2,'Cerro Navia');
INSERT INTO CORE_DISTRICT (id,name) VALUES (3,'Conchalí');
INSERT INTO CORE_DISTRICT (id,name) VALUES (4,'El Bosque');
INSERT INTO CORE_DISTRICT (id,name) VALUES (5,'Estación Central');
INSERT INTO CORE_DISTRICT (id,name) VALUES (6,'Huechuraba');
INSERT INTO CORE_DISTRICT (id,name) VALUES (7,'Independencia');
INSERT INTO CORE_DISTRICT (id,name) VALUES (8,'La Cisterna');
INSERT INTO CORE_DISTRICT (id,name) VALUES (9,'La Florida');
INSERT INTO CORE_DISTRICT (id,name) VALUES (10,'La Granja');
INSERT INTO CORE_DISTRICT (id,name) VALUES (11,'La Pintana');
INSERT INTO CORE_DISTRICT (id,name) VALUES (12,'La Reina');
INSERT INTO CORE_DISTRICT (id,name) VALUES (13,'Las Condes');
INSERT INTO CORE_DISTRICT (id,name) VALUES (14,'Lo Barnechea');
INSERT INTO CORE_DISTRICT (id,name) VALUES (15,'Lo Espejo');
INSERT INTO CORE_DISTRICT (id,name) VALUES (16,'Lo Prado');
INSERT INTO CORE_DISTRICT (id,name) VALUES (17,'Macul');
INSERT INTO CORE_DISTRICT (id,name) VALUES (18,'Maipú');
INSERT INTO CORE_DISTRICT (id,name) VALUES (19,'Ñuñoa');
INSERT INTO CORE_DISTRICT (id,name) VALUES (20,'Pedro Aguirre Cerda');
INSERT INTO CORE_DISTRICT (id,name) VALUES (21,'Peñalolén');
INSERT INTO CORE_DISTRICT (id,name) VALUES (22,'Providencia');
INSERT INTO CORE_DISTRICT (id,name) VALUES (23,'Pudahuel');
INSERT INTO CORE_DISTRICT (id,name) VALUES (24,'Quilicura');
INSERT INTO CORE_DISTRICT (id,name) VALUES (25,'Quinta Normal');
INSERT INTO CORE_DISTRICT (id,name) VALUES (26,'Recoleta');
INSERT INTO CORE_DISTRICT (id,name) VALUES (27,'Renca');
INSERT INTO CORE_DISTRICT (id,name) VALUES (28,'San Joaquín');
INSERT INTO CORE_DISTRICT (id,name) VALUES (29,'San Miguel');
INSERT INTO CORE_DISTRICT (id,name) VALUES (30,'San Ramón');
INSERT INTO CORE_DISTRICT (id,name) VALUES (31,'Santiago');
INSERT INTO CORE_DISTRICT (id,name) VALUES (32,'Vitacura');

INSERT INTO CORE_SECQUESTION (id,question) VALUES (1,'¿Ciudad de nacimiento?');
INSERT INTO CORE_SECQUESTION (id,question) VALUES (2,'¿Nombre de su primera mascota?');
INSERT INTO CORE_SECQUESTION (id,question) VALUES (3,'¿Segundo apellido de su madre?');
INSERT INTO CORE_SECQUESTION (id,question) VALUES (4,'¿Número de hermanos/as mayores?');

INSERT INTO CORE_USER (rut,name,surname,mail,phone,password,secanswer,role_id,secquestion_id,is_active) VALUES ('10.000.000-0','William','Hartnell','whart@mail.com','+123456789','pbkdf2_sha256$390000$flstV0aXVQzFKiGVUoBbNr$qmIvgvAvkfFdIVOmpuJj5nqZHbfHNrPV8qPrqmDFRcI=','13',1,4,1);
INSERT INTO CORE_USER (rut,name,surname,mail,phone,password,secanswer,role_id,secquestion_id,is_active) VALUES ('11.000.000-0','Patrick','Troughton','ptrou@mail.com','+234567891','pbkdf2_sha256$390000$B5CWSBuOvd7I690hwLQUnV$aEbPkISBeXC2EnGa6DEW8bVQCUcF9o0YCGWYlQ9ana4=','12',1,4,1);
INSERT INTO CORE_USER (rut,name,surname,mail,phone,password,secanswer,role_id,secquestion_id,is_active) VALUES ('12.000.000-0','Jon','Pertwee','jpert@mail.com','+345678912','pbkdf2_sha256$390000$tQNEqWqE76iovwzvEprCmD$r48M6BCfGulW7rTS7FEWekxcqgGlm/kCVmTnSb6IhJA=','11',1,4,1);
INSERT INTO CORE_USER (rut,name,surname,mail,phone,password,secanswer,role_id,secquestion_id,is_active) VALUES ('13.000.000-0','Tom','Baker','tbake@mail.com','+456789123','pbkdf2_sha256$390000$NrkZu3NdQFLP3CZAdDKPAs$r+dPC8PABxlU0j/uf/D/KTh/1882u0TFmIhcR3uxa/A=','10',1,4,1);
INSERT INTO CORE_USER (rut,name,surname,mail,phone,password,secanswer,role_id,secquestion_id,is_active) VALUES ('20.000.000-0','Alvis','Claus','aclau@mail.com','+987654321','pbkdf2_sha256$390000$4RA3XJJB4qk6jjW8xLLJ3F$WR3EF8pxT+6ETT0fjX2UUHJsO50AebjCF4YDkYsEps0=','Kermit',2,2,1);

INSERT INTO AUTH_USER (password,is_superuser,username,email,is_staff,is_active,date_joined) values ('pbkdf2_sha256$390000$flstV0aXVQzFKiGVUoBbNr$qmIvgvAvkfFdIVOmpuJj5nqZHbfHNrPV8qPrqmDFRcI=',0,'whart@mail.com','whart@mail.com',0,1,sysdate);
INSERT INTO AUTH_USER (password,is_superuser,username,email,is_staff,is_active,date_joined) values ('pbkdf2_sha256$390000$B5CWSBuOvd7I690hwLQUnV$aEbPkISBeXC2EnGa6DEW8bVQCUcF9o0YCGWYlQ9ana4=',0,'ptrou@mail.com','ptrou@mail.com',0,1,sysdate);
INSERT INTO AUTH_USER (password,is_superuser,username,email,is_staff,is_active,date_joined) values ('pbkdf2_sha256$390000$tQNEqWqE76iovwzvEprCmD$r48M6BCfGulW7rTS7FEWekxcqgGlm/kCVmTnSb6IhJA=',0,'jpert@mail.com','jpert@mail.com',0,1,sysdate);
INSERT INTO AUTH_USER (password,is_superuser,username,email,is_staff,is_active,date_joined) values ('pbkdf2_sha256$390000$NrkZu3NdQFLP3CZAdDKPAs$r+dPC8PABxlU0j/uf/D/KTh/1882u0TFmIhcR3uxa/A=',0,'tbake@mail.com','tbake@mail.com',0,1,sysdate);
INSERT INTO AUTH_USER (password,is_superuser,username,email,is_staff,is_active,date_joined) values ('pbkdf2_sha256$390000$4RA3XJJB4qk6jjW8xLLJ3F$WR3EF8pxT+6ETT0fjX2UUHJsO50AebjCF4YDkYsEps0=',0,'aclau@mail.com','aclau@mail.com',1,1,sysdate);

INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id, is_active) VALUES ('Av. Enida', '123', '600345', 1, 1, 1);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id, is_active) VALUES ('Av. Siempreviva', '644', '530345', 1, 2, 1);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id, is_active) VALUES ('Los Aromos', '413-B', '332345', 2, 3, 1);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id, is_active) VALUES ('Los Naranjos', '166', '600123', 2, 4, 1);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id, is_active) VALUES ('Los Manzanos', '35-B', '987252', 3, 5, 1);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id, is_active) VALUES ('Los Plátanos', '13', '512312', 4, 6, 1);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id, is_active) VALUES ('Av. Italia', '61', '848455', 5, 7, 1);

INSERT INTO CORE_SALE (saleDate, status, total, user_id, address_id, subscribed) VALUES (SYSDATE, 'Carrito', 0, 1, 1, 0);
INSERT INTO CORE_SALE (saleDate, status, total, user_id, address_id, subscribed) VALUES (SYSDATE, 'Carrito', 0, 2, 3, 0);
INSERT INTO CORE_SALE (saleDate, status, total, user_id, address_id, subscribed) VALUES (SYSDATE, 'Carrito', 0, 3, 5, 0);
INSERT INTO CORE_SALE (saleDate, status, total, user_id, address_id, subscribed) VALUES (SYSDATE, 'Carrito', 0, 4, 6, 0);

INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Collar Azul', 'Esta es la descripción del producto Collar Azul', 'products/collarBlue.png', 2500, 30, 1, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Collar Negro', 'Esta es la descripción del producto Collar Negro', 'products/collarBlack.png', 2600, 30, 1, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Collar Verde', 'Esta es la descripción del producto Collar Verde', 'products/collarGreen.png', 2700, 30, 1, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Collar Rosa', 'Esta es la descripción del producto Collar Rosa', 'products/collarPink.png', 2800, 30, 1, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Collar Rojo', 'Esta es la descripción del producto Collar Rojo', 'products/collarRed.png', 2900, 30, 1, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Comida Gato Adulto', 'Esta es la descripción del producto Comida Gato Adulto', 'products/foodCatAdult.png', 3500, 30, 2, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Comida Gato Cachorro', 'Esta es la descripción del producto Comida Gato Cachorro', 'products/foodCatYoung.png', 3600, 30, 2, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Comida Perro Adulto', 'Esta es la descripción del producto Comida Perro Adulto', 'products/foodDogAdult.png', 3700, 30, 2, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Comida Perro Cachorro', 'Esta es la descripción del producto Comida Pero Cachorro', 'products/foodDogYoung.png', 3800, 30, 2, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Comida Mapache', 'Esta es la descripción del producto Comida Mapache', 'products/foodRaccoon.png', 3900, 30, 2, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Disco Volador', 'Esta es la descripción del producto Disco Volador', 'products/toyFlyingDisk.png', 4500, 30, 3, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Cuerda Anudada', 'Esta es la descripción del producto Cuerda Anudada', 'products/toyKnotRope.png', 4600, 30, 3, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id, is_active) VALUES ('Pelota de Tenis', 'Esta es la descripción del producto Pelota de Tenis', 'products/toyTennisBall.png', 4700, 30, 3, 1);
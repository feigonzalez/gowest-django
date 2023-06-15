INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id) VALUES ('Av. Enida', '123', '600345', 1, 1);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id) VALUES ('Av. Siempreviva', '644', '530345', 1, 2);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id) VALUES ('Los Aromos', '413-B', '332345', 2, 3);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id) VALUES ('Los Naranjos', '166', '600123', 2, 4);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id) VALUES ('Los Manzanos', '35-B', '987252', 3, 5);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id) VALUES ('Los Plátanos', '13', '512312', 4, 6);
INSERT INTO CORE_ADDRESS (streetName, streetNumber, postalCode, user_id, district_id) VALUES ('Av. Italia', '61', '848455', 5, 7);

INSERT INTO CORE_SALE (saleDate, deliveryDate, status, total, user_id, address_id, subscribed) VALUES (TO_DATE('2023/01/01 21:02:44', 'yyyy/mm/dd hh24:mi:ss'),TO_DATE('2023/01/10 11:31:24', 'yyyy/mm/dd hh24:mi:ss'), 'Completada', 7200, 1, 1, 0);
INSERT INTO CORE_SALE (saleDate, status, total, user_id, address_id, subscribed) VALUES (TO_DATE('2023/02/02 19:32:24', 'yyyy/mm/dd hh24:mi:ss'), 'Carrito', 5800, 1, 1, 0);
INSERT INTO CORE_SALE (saleDate, status, total, user_id, address_id, subscribed) VALUES (TO_DATE('2023/03/03 17:42:54', 'yyyy/mm/dd hh24:mi:ss'), 'Despachada', 4200, 1, 2, 0);
INSERT INTO CORE_SALE (saleDate, status, total, user_id, address_id, subscribed) VALUES (TO_DATE('2023/04/04 16:22:43', 'yyyy/mm/dd hh24:mi:ss'), 'Pagada', 4200, 2, 3, 0);

INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Collar Azul', 'Esta es la descripción del producto Collar Azul', 'products/collarBlue.png', 2500, 30, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Collar Negro', 'Esta es la descripción del producto Collar Negro', 'products/collarBlack.png', 2600, 30, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Collar Verde', 'Esta es la descripción del producto Collar Verde', 'products/collarGreen.png', 2700, 30, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Collar Rosa', 'Esta es la descripción del producto Collar Rosa', 'products/collarPink.png', 2800, 30, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Collar Rojo', 'Esta es la descripción del producto Collar Rojo', 'products/collarRed.png', 2900, 30, 1);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Comida Gato Adulto', 'Esta es la descripción del producto Comida Gato Adulto', 'products/foodCatAdult.png', 3500, 30, 2);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Comida Gato Cachorro', 'Esta es la descripción del producto Comida Gato Cachorro', 'products/foodCatYoung.png', 3600, 30, 2);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Comida Perro Adulto', 'Esta es la descripción del producto Comida Perro Adulto', 'products/foodDogAdult.png', 3700, 30, 2);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Comida Perro Cachorro', 'Esta es la descripción del producto Comida Pero Cachorro', 'products/foodDogYoung.png', 3800, 30, 2);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Comida Mapache', 'Esta es la descripción del producto Comida Mapache', 'products/foodRaccoon.png', 3900, 30, 2);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Disco Volador', 'Esta es la descripción del producto Disco Volador', 'products/toyFlyingDisk.png', 4500, 30, 3);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Cuerda Anudada', 'Esta es la descripción del producto Cuerda Anudada', 'products/toyKnotRope.png', 4600, 30, 3);
INSERT INTO CORE_PRODUCT(name, description, image, price, stock, category_id) VALUES ('Pelota de Tenis', 'Esta es la descripción del producto Pelota de Tenis', 'products/toyTennisBall.png', 4700, 30, 3);
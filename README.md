# gowest-django
Sistema de tienda online para tienda de mascotas GoWest, usando django (Proyecto de Programación Web)

## Instalación
El sistema requiere una base de datos de Oracle v18+, y Python 3.9+ con el instalador pip.

 - Instalar Django: `pip install django`
 - Instalar Pllow: `pip install Pillow`
 - Instalar Framework API: `pip install djangorestframework`
 - Instalar Requests: `pip install requests`

El sistema interactúa con la base de datos mediante un usuario "gowest_admin" de contraseña "gowest".
Este usuario debe crearse en la base de datos (se puede ejecutar el script `prepareDB.sql`),
y luego debe crearse para django mediante el archivo `gowest/manage.py`, ejecutando en esa carpeta
`python manage.py createsuperuser`.

Para crear las tablas del sistema en la base de datos, ejecutar `python manage.py makemigrations`, y
luego `python manage.py migrate`.

Una vez estén las tablas creadas, se debe ejecutar el script `popDB.sql`. Este script
inserta en las tablas correspondientes los datos iniciales para el correcto funcionamiento del sistema.
*Nota: En las pruebas realizadas, el script se ejecutó mediante SQLPlus. Esto hizo que varios de los
datos de tipo texto quedaran mal codificados, y se muestren de manera incorrecta en la página.*
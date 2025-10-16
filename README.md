🧱 Migraciones en Django

Las migraciones son el mecanismo que utiliza Django para mantener sincronizados los modelos (definidos en el código) con la base de datos real.
Permiten aplicar, revertir o registrar los cambios estructurales del esquema de la base de datos (como crear tablas, agregar campos, cambiar tipos de datos, etc.) de manera controlada y segura.

🔹 **python3 manage.py makemigrations**

Este comando prepara los cambios que se deben aplicar en la base de datos.

Cuando Django detecta modificaciones en los modelos (models.py), ejecutamos este comando para que genere los archivos de migración dentro del directorio migrations/ de cada aplicación.

Cada archivo creado representa una instrucción de cambio que Django aplicará posteriormente a la base de datos.

🧩 Función:

Lee los modelos definidos en el código.

Detecta los cambios realizados (nuevos campos, tablas, eliminaciones, etc.).

Genera archivos Python con las instrucciones necesarias para aplicar esos cambios en la base de datos.

📘 Ejemplo:
python3 manage.py makemigrations minilibrary


Este comando genera un archivo como:

migrations/0001_initial.py


Dentro de este archivo encontraremos código Python con las instrucciones necesarias para crear las tablas y sus campos en la base de datos, de acuerdo a lo definido en los modelos.

🧠 Concepto general:

makemigrations no modifica aún la base de datos, solo crea el “plan de acción” o “guía” para que Django sepa qué hacer cuando se ejecute migrate.
Podemos verlo como un paso de preparación antes de aplicar los cambios reales.



🔹 **python3 manage.py showmigrations**

Este comando muestra todas las migraciones existentes en el proyecto, organizadas por aplicación.
Cada línea representa un módulo de migración que contiene los cambios estructurales aplicados o pendientes de aplicar en la base de datos.

🧩 Estados de las migraciones:

Sin “X” (☐):
Indica que el archivo de migración ha sido creado mediante makemigrations, pero aún no ha sido aplicado en la base de datos.
En este punto, Django solo ha generado el código que define cómo debería modificarse la estructura de la base de datos (por ejemplo, crear una tabla o agregar un campo), pero no ha ejecutado esos cambios.

Con “X” (✔):
Indica que la migración ya fue aplicada con migrate.
Por tanto, los cambios definidos en ese archivo ya se reflejan en la base de datos real.

🧠 Concepto general:

Podemos ver las migraciones como un historial de cambios estructurales de la base de datos.
Cada archivo dentro del directorio migrations/ representa un snapshot (instantánea) del estado de los modelos en un momento dado del desarrollo.

Esto permite:

Tener control sobre la evolución de la base de datos.

Aplicar o revertir cambios fácilmente.

Evitar errores al modificar los modelos durante el desarrollo.

Por ejemplo, si en una etapa del proyecto agregamos un nuevo campo a un modelo, Django generará un nuevo archivo de migración que contendrá solo los cambios necesarios para reflejar esa modificación en la base de datos.
Así, podemos mantener un registro claro y ordenado de la evolución del esquema sin perder consistencia.


🔹 python3 manage.py migrate

Este comando ejecuta las migraciones creadas por makemigrations, aplicando los cambios en la base de datos real.

Django utiliza los archivos de migración para crear, modificar o eliminar tablas y columnas, asegurando que la base de datos esté sincronizada con los modelos definidos en el código.

⚙️ Antes de crear nuestros modelos:

Antes de comenzar a desarrollar una aplicación, es necesario ejecutar migrate al menos una vez para que Django cree las tablas internas que necesita para funcionar (por ejemplo, las del sistema de autenticación, permisos, sesiones, y el panel de administración).

python3 manage.py migrate


Con esto, Django crea automáticamente las tablas básicas necesarias para operar.

⚙️ Durante el desarrollo:

Cada vez que realicemos cambios en los modelos y generemos nuevas migraciones con makemigrations, debemos ejecutar migrate para que dichos cambios se reflejen en la base de datos.

📘 Ejemplo:
python3 manage.py migrate minilibrary


Este comando aplica las migraciones del módulo minilibrary, convirtiendo nuestros modelos (clases en models.py) en tablas reales con sus respectivos campos y configuraciones.

🧠 Concepto general:

Podemos ver migrate como el paso final del proceso de migración, el que realmente transforma nuestro diseño lógico (los modelos de Django) en una estructura física en la base de datos.

🔹 Conceptos relacionados
🧩 Field Types (Tipos de Campos)

Los Field Types son clases que Django ofrece para definir el tipo de columna que tendrá cada atributo del modelo en la base de datos.
Ejemplos:

CharField → texto corto

IntegerField → número entero

DateField → fecha

BooleanField → valor verdadero o falso

Cada campo representa una columna en la tabla correspondiente.

⚙️ Field Options (Opciones de Campo)

Son parámetros adicionales que permiten configurar cómo Django debe definir esa columna en la base de datos.
Ejemplos:

max_length: longitud máxima de caracteres permitidos.

unique: indica que el campo no puede tener valores repetidos.

null: permite valores nulos en la base de datos.

default: define un valor por defecto.

Estas opciones ayudan a controlar la integridad y consistencia de los datos.

🧭 Flujo completo del proceso de migración en Django

Definimos o modificamos modelos en models.py.

Ejecutamos:

python3 manage.py makemigrations


Django genera los archivos de migración con los cambios detectados.

Verificamos las migraciones pendientes con:

python3 manage.py showmigrations


Aplicamos los cambios a la base de datos con:

python3 manage.py migrate

-- Crear tablas en SQL
CREATE TABLE author (
	id INTEGER PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	birth_day DATE
);


CREATE TABLE book (
	id INTEGER PRIMARY KEY NOT NULL,
	title VARCHAR(200) NOT NULL,
	publication_date DATE NOT NULL,
	-- on delete cascade es para que cuando se elimine un autor de la tabla author
	-- se eliminaran todos los book que tengan el id del autor en esta columna
	author_id INTEGER REFERENCES author(id) ON DELETE CASCADE 
);

-- Insertar registros en una tabla con SQL
INSERT INTO author (name, birth_day) VALUES ("Daniel Valdebenito", "1998-12-30");

-- Ingresar multiples registros
INSERT INTO author (name, birth_day) VALUES 
("J.K Rowling", "1965-07-31"),
("Gabriel Garcia Marquez", "1927-03-06"),
("Haruki Murakami", "1949-01-12"),
("Jane Austen", "1775-12-16"),
("Stephen King", "1947-09-21");

INSERT INTO book (title, publication_date, author_id) VALUES 
('Harry Potter y la piedra filosofal', '1997-06-26', 2),
('Harry Potter y la cámara secreta', '1998-07-02', 2),
('Cien años de soledad', '1967-06-05', 3),
('Kafka en la orilla', '2002-09-12', 4),
('Tokio Blues', '1987-09-04', 5),
('Orgullo y prejuicio', '1813-01-28', 5),
('El resplandor', '1997-01-28', 6);


-- Consultas Básicas con SQL
SELECT * FROM author;
SELECT name FROM author;
-- Unir 2 tablas por 1 columna.
-- Unir los registros de la tabla book con la tabla author donde la columna id de la tabla author sea igual
-- a la columna author_id de la tabla book, si existen multiples registros de la tabla book que tienen en
-- la columna author_id el mismo valor, simplemente repite los registros de author para unirlos a esos
-- registros de book sin importar que se repitan registros de author con total de cumplir con la union.
SELECT * FROM book JOIN author ON book.author_id = author.id; -- Todas las columnas del resultado de unir ambas tablas en una unica tabla

-- Traer todos los libros de un author
SELECT book.title, author.name FROM book JOIN author ON book.author_id = author.id;


-- Actualizar y Eliminar Registros
UPDATE author SET name = 'Ricardo Cuellar' WHERE id = 1; -- Actualiza el name del autor con id igual a 1
UPDATE author SET birth_day = '1995-08-10' WHERE id = 1;
DELETE FROM book WHERE id = 6;
-- Al habilitar cascada, elimina todos los libros asociados al autor con id 2
DELETE FROM author WHERE id = 5;

-- Verificar que este habilitada la eliminacion en cascada (0: deshabilitado - 1:habilitado)
PRAGMA foreign_keys;
-- Activar la eliminacion por cascada.
PRAGMA foreign_keys = ON;


-- Ordenar resultados
SELECT * FROM book ORDER BY publication_date; -- Regresa registros ordenados por su fecha de publicacion.
-- Modificar el orden
SELECT title, publication_date FROM book ORDER BY publication_date DESC;

 

-- Contar registros
SELECT COUNT(*) FROM book; -- Me cuenta todos los registros de la tabla books
-- En vez de decirle a SELECT que queremos una columna, le solicitamos o decimos que queremos una cuenta
SELECT COUNT(*) FROM author;


-- Filtrar Registros
SELECT * FROM author WHERE name = 'Stephen King'; -- El valor debe ser identico por el que estamos filtrando
SELECT * FROM author WHERE name LIKE 'Stephen%'; -- Like permite indicar que sea parecido, es decir que empieze con eso y luego % puede ser cualquier valor.


-- Consultas Anidadas

-- Ejemplo en el caso que no nos sepamos un id de un registro, lo cual es posible ya que es mas facil recordar
-- algun otro campo que un identificador que se genera aleatoriamente.

SELECT title FROM book WHERE author_id = (
	SELECT id FROM author WHERE name LIKE 'Stephen%'
);
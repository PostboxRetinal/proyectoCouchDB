### *"No olvidar especificar en el texto de la entrega el nombre de los integrantes"*
**Desarrollado por Sebastian Balanta**

Durante el semestre se desarrollará un sistema de recomendación de cursos y tutores usando algunas de las bases de datos NoSQL disponibles de forma comercial con el fin de evidenciar sus ventajas, desventajas y aplicar los conceptos implicados en su diseño e implementación, en contraste con las bases de datos relacionales.

# Enunciado

En esta entrega se deben diseñar e implementar las colecciones y un adelanto del CRUD con las operaciones especificadas en las instrucciones.

Los objetivos de esta actividad evaluativa, la cual se realizará por entregas, son los siguientes:

- Diseñar de forma apropiada un modelo de base de datos llave valor aplicando los principios de este tipo de BDs y que cumpla con los requerimientos planteados

- Realizar la implementación de la BD ajustándose a los requerimientos

- Implementar las consultas y procedimientos requeridos de tal forma que en algún momento dicho prototipo funcione como un sistema de recomendaciones

# Entrega (se realiza en parejas)

## Primer avance (Diseño e Implementación en CouchDB): 

Diseña e implementa un modelo de datos con colecciones de Usuarios (aprendices), Cursos y Tutores. 

Cada documento de cada colección debe tener las propiedades relevantes y deben implementarse de igual forma las relaciones pertinentes:

## Colecciones
- Usuarios (o aprendiz)
- Tutores
- Cursos
## Atributos

### Usuario
- Id del usuario
- Nombre
- Carrera
- Semestre
  
### Tutor
- Id del tutor
- Nombre
- Carrera
- Semestre
- Calificación 
- Promedio

### Curso
  - Id del curso
  - Nombre
  - Categoría (Artes y humanidades, Ciencias básicas Tecnología)
  - Modalidad (presencial, remoto)
  - Gratuito (V o F)
  - Precio
  - Duración (horas)
  - Certificado (V o F)
  - Calificación promedio (0.0 a 5.0)

### Relaciones
  - El Usuario (Aprendiz) asiste o toma un Curso
  - Usuario califica Curso (de 0.0 a 5.0)
  - Usuario Califica Tutor
  - Tutor dicta Curso
  - Curso es Similar a Curso
  
Las relaciones también tienen propiedades, útiles en las consultas.

### Implementa un CRUD en Python con las siguientes operaciones:

- Consulta de Usuario, Tutor y Curso por alguna llave (no necesariamente el id)
- Creación de Usuario, Tutor o Aprendiz

## 2. Entregable 

Enlace a repo de GitHub con los siguientes archivos.

    - [ x ] Código en Python con el módulo del CRUD implementado
    - [  ] Código en JSON de cada colección de documentos
    - [  ] Diseño de la vista o vistas en formato JSON




## 3. Enlaces de Referencia:

[Repo de referencia](https://github.com/dfloaizab/NonRelationalDBs/tree/main/Unit2_Material)

[Referencia de CouchDB - Creación de documentos](https://docs.couchdb.org/en/stable/ddocs/ddocs.html#creation-and-structure)

[Vistas en CouchDB](https://docs.couchdb.org/en/stable/ddocs/views/intro.html)
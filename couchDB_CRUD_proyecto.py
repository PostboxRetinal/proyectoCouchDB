#Proyecto Bases de Datos 2
#Desarrollado por Sebastian Balanta

#IMPORTS
import couchdb
import subprocess,time

#CODIGOS DE ERROR
    #1 SIN ERROR
    #2 USU/PASS INVALIDA

#DATOS
user = "testing" #USER
pwd = "testing123*-" #PASS
host = "127.0.0.1" #IP/LOCALHOST
port = "5984" #PORT
db_name = "cli_recommendation" #NOMBRE DOC BBDD

#CONEXION BBDD
couch_server = couchdb.Server(f"http://{user}:{pwd}@{host}:{port}/")

#MODULOS / CRUD OPs
def limpiarPantalla():
    '''Esta función se encarga de limpiar la pantalla con el  módulo subprocess 
    (none) -> (none)'''
    time.sleep(1.5)
    subprocess.run('clear',shell=True)

def validar_guardado(doc_id):
    if doc_id in db:
        print(f"El documento con ID: {doc_id} se ha guardado correctamente en la BBDD")
    else:
        print(f"El documento con ID: {doc_id} no se ha guardado correctamente en la BBDD")

def query(tipo,llave,valor):
    '''Función encargada de hacer querys requeridos con ayuda de 3 parámetros'''
    design_doc = f"_design/{tipo}"
    view_name = f"buscar_por_{llave}"
    resultados = db.view(f"{tipo}/{view_name}",key=valor)

def consultarUsuario(nombre):
    '''Función encargada de consultar en la BBDD filtrando por usuarios
    (str) -> obj'''
    for row in db.view('_all_docs', include_docs = True):
        doc = row['doc']
        if doc.get('nombre') == nombre:
            return doc
    limpiarPantalla()
    return print(f'No se encontró la entrada {nombre}')

def consultarTutor(nombre):
    '''Función encargada de consultar en la BBDD filtrando por Tutor
    (str) -> obj'''
    for row in db.view('_all_docs', include_docs = True):
        doc = row['doc']
        if doc.get('nombre') == nombre:
            return doc
    limpiarPantalla()
    return print(f'No se encontró la entrada {nombre}')

def consultarCurso(modalidad):
    '''Función encargada de consultar en la BBDD filtrando por modalidad
    (str) -> obj'''
    for row in db.view('_all_docs', include_docs = True):
        doc = row['doc']
        if doc.get('modalidad') == modalidad:
            return doc
    limpiarPantalla()
    return print(f'No se encontró la entrada {modalidad}')
    
def menuRol(opc):
    '''Función encargada de ejecutar según sea necesario la creación de objetos con ayuda de un argumento entero
    (int) -> none'''
    if opc == 1:
        tipo = "Aprendiz"
        id = input("Ingrese el ID del aprendiz: ")
        nombre = input("Ingrese el nombre del aprendiz: ")
        carrera = input("Ingrese la carrera del aprendiz: ")
        semestre = int(input("Ingrese el semestre cursado del aprendiz: "))

        aprendiz = {
            "tipo":tipo,
            "id":id,
            "nombre":nombre,
            "carrera":carrera,
            "semestre":semestre
        }

        db.save(aprendiz)
        validar_guardado(aprendiz["_id"])
    elif opc == 2:
        tipo = "Tutor"
        id = input("Ingrese el ID del tutor: ")
        nombre = input("Ingrese el nombre del tutor: ")
        carrera = input("Ingrese la carrera del tutor: ")
        semestre = int(input("Ingrese el semestre cursado del tutor: "))
        calPromedio = float(input("Ingrese la calificacion promedio del tutor: "))

        tutor = {
            "tipo":tipo,
            "id":id,
            "nombre":nombre,
            "carrera":carrera,
            "semestre":semestre,
            "calPromedio":calPromedio
        }

        db.save(tutor)
        validar_guardado(tutor["_id"])
    elif opc == 3:
        tipo = "Curso"
        id = input("Ingrese el ID del curso: ")
        nombre = input("Ingrese el nombre del curso: ")
        categoria = int(input("\n\n--- CATEGORIAS DIPONIBLES ---\n\n1. Artes y humanidades\n2. Ciencias básicas\n3. Tecnología\n\nSeleccione una opción: "))

        if categoria == 1:
            categoria = "Artes y humanidades"
        elif categoria == 2:
            categoria = "Ciencias básicas"
        elif categoria == 3:
            categoria = "Tecnología"
        else:
            print('Opción incorrecta. Intenta nuevamente')
            
        modalidad = int(input("\n\n--- MODALIDADES ---\n\n1. Presencial\n2. Remoto\n\nSeleccione una opción: "))
        if categoria == 1:
            categoria = "Presencial"
        elif categoria == 2:
            categoria = "Remoto"
        else:
            print('Opción incorrecta. Intenta nuevamente')
            modalidad = int(input("\n\n--- MODALIDADES ---\n\n1. Presencial\n2. Remoto\n\nSeleccione una opción: "))

        gratuito = int(input("¿Es el curso gratuito?\n\n1. Verdadero\n2. Falso)\n\nSeleccione una opción: "))

        if gratuito == 1:
            gratuito = True
        elif gratuito == 2:
            gratuito = False
        else:
            print('Opción incorrecta. Intenta nuevamente')

        precio = float(input("Ingrese el precio del curso: "))
        duracion = int(input("Ingrese la duración del curso (en horas): "))
        certificado = int(input("¿El curso tiene certificado?\n\n1. Verdadero\n2. Falso)\n\nSeleccione una opción: "))
        if certificado == 1:
            certificado = True
        elif certificado == 2:
            certificado = False
        else:
            print('Opción incorrecta. Intenta nuevamente')

        calPromedio = float(input("Ingrese la calificación promedio del curso (0.0 a 5.0): "))

        curso = {
            "tipo":tipo,
            "id":id,
            "nombre":nombre,
            "categoria":categoria,
            "modalidad":modalidad,
            "gratuito":gratuito,
            "precio":precio,
            "duracion":duracion,  
            "certificado":certificado,
            "calPromedio":calPromedio
        }

        db.save(curso)
        validar_guardado(curso["_id"]) 

def menu(nombre_user):
    '''Función encargada de ejecutar la funcionalidad completa de la app
    (none) -> (none)'''
    while True:
        limpiarPantalla()
        opcion = int(input(f"Holaaa {nombre_user}\n\n1.Creación\n2.Consulta por nombre\n3.Salir\n\nDigita una opción: "))
        
        #Creación de objetos
        if (opcion == 1):
            opc1 = int(input("¿Qué tipo de rol desea crear?: \n1.Aprendiz\n2.Tutor\n3.Curso\n"))
            if opc1 == 1:
                menuRol(1)
                pass
            
            elif opc1 == 2:
                menuRol(2)
                pass
                
            elif opc1 == 3:
                menuRol(3)
                pass

            else:
                print("Opción Inválida. Indique una opción correcta.")
        
        #Validacionees y consultas
        elif (opcion == 2):
            opc1 = int(input("Validación por nombre: \n1. Consultar Alumno\n2. Consultar Docente\n\nValidación por modalidad:\n 3. Consultar curso\n\nDigita una opción: "))
            
            if (opc1 == 1):
                res = consultarUsuario(input('Consultar nombre del aprendiz: '))
                print(res)
                pass

            elif (opc1 == 2):
                res = consultarTutor(input('Consultar nombre del tutor: '))
                print(res)
                pass

            elif (opc1 == 3):
                res = consultarCurso(input('Consultar modalidad del curso: ')).lower()
                print(res)
                pass

            elif (opc1 == 4):
                # Retorna arriba
                continue
            else:
                print("Opción Inválida. Proporcione una opción correcta.")
        
        elif opcion == 3:
            print("Salir")
            #Sale con código de error 1, básicamente sin error
            exit(1)

        else:
            print("Opción Inválida. Proporcione una opción correcta.")

#VALIDACION INICIAL
print(f"Estableciendo conexión con {host}:{port} ...")
time.sleep(1)

try:
    couch_server.login(user,pwd)
    if (db_name in couch_server):
        print(f'BBDD {db_name} encontrada')
        db = couch_server[db_name]
except couchdb.Unauthorized:
    print('Usuario o Clave Incorrectas. Intenta nuevamente')
    exit(2)
except:
    print(f'No se encontró la base de datos {db_name}, será creada')
    db = couch_server.create(db_name)


def ejecucion(nombre):
    '''Llama los módulos requeridos para la ejecución del programa
    (str) -> (none)'''
    try:
        menu(nombre)
    except KeyboardInterrupt:
        salida = input('\n¿Deseas salir de la aplicación? (S/N): ').lower()
        if salida == 's':
            exit(0)
        else:
            ejecucion()
            
#EJECUCION
nombre_user = input('BIENVENIDO\nIngresa tu nombre: ')
ejecucion(nombre_user)
    


""""
#(2)  Select: selección de un res por un determinado valor de llave ("_id")
doc_creado = db["1244324"]
print(doc_creado)
 #Otra forma de ejecutar queries usando el lenguaje "mango" de consultas de CouchDB (notación JSON)
 #referencia de queries más complejos en:
 #https://docs.couchdb.org/en/stable/api/database/find.html
query = {"selector":{"rep_legal": "Diana L"}}
docs = db.find(query)
result = [] 

#docs es un objeto iterable:
for i in docs:
  print(dict(i)) #i es un res de couchdb que puede convertirse a diccionario...
  result.append(dict(i)) #...y adicionarse a una lista

#(3) Update: Modificación de un res previamente consultado:
doc_creado["fondos"] = 1000000.0
db.save(doc_creado)
print(doc_creado)

#(4) Delete:Borrado de un res existente
doc_borrar = db["2"]
db.delete(doc_borrar)

#funciones del crud
def Create(collection, data):
    doc_id, doc_rev = db.save(data)

def Update(doc_id, data):
    doc = db[doc_id]
    doc.update(data)
    db.save(doc)
    
def SelectAll(collection): #el selectall selecciona todos los registros
    docs = [doc for doc in db.view(f"{collection}/all")]
    
def Select_By_Criteria(collection, criteria):
    docs = [doc for doc in db.view(f"{collection}/by_criteria", key=criteria)]

def Delete_Id(doc_id):
    doc = db[doc_id]
    db.delete(doc)

def Delete_Value(key, value):
    doc_id = db.get()
    
guitarra = {
    "id":"G001",
    "nombre":"Guitarra acustica base",
    "categoria":"musica",
    "descripcion":"Curso guitarra acustica basico",
    "duracion":40,
    "precio":120000.00,
    "remoto":False
}

pintura1 = {
    "id":"P001",
    "nombre":"Pintura al oleo",
    "categoria":"arte",
    "descripcion":"Pintura en oleo",
    "duracion":30,
    "precio":130000.00,
    "remoto":False
}

pintura2 = {
    "id":"P002",
    "nombre":"Pintura acrilica",
    "categoria":"arte",
    "descripcion":"Pintura acrilica",
    "duracion":30,
    "precio":130000.00,
    "remoto":False
}

Create ("cursos", guitarra)
Create ("cursos", pintura1)
Create ("cursos", pintura2)

#revisar update
guitarra ["duracion"]=45
Update (guitarra)

lista_cursos = SelectAll("cursos")
for c in lista_cursos:
    print(c)
    

criterios = "arte"
cursos_pintura = Select_By_Criteria("cursos", criterios)
"""
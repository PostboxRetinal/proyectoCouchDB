#Proyecto Bases de Datos 2
#Desarrollado por Sebastian Balanta

#IMPORTS
import couchdb
import subprocess,time,os,sys,json

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

def detectarArquitectura():
    '''Se encarga de usar la libreria os para detectar que SO corre actualmente
    none -> (str)'''

    if os.name == 'nt':
        return('Windows')
    elif os.name == 'posix':
        return ('Linux')
    else:
        return('Desconocido')

#MODULOS / CRUD OPs
def limpiarPantalla(aarch):
    '''Esta función se encarga de limpiar la pantalla con el  módulo subprocess 
    (none) -> (none)'''
    #Si es Windows
    if aarch == 'Windows':
        limpiar = 'cls'
    #Si es Linux
    elif aarch == 'Linux':
        limpiar = 'clear'
    time.sleep(0.8)
    subprocess.run(limpiar,shell=True)

def validar_guardado(doc_id):
    if doc_id in db:
        print(f"El documento con ID: {doc_id} se ha guardado correctamente en la BBDD")
    else:
        print(f"El documento con ID: {doc_id} no se ha guardado correctamente en la BBDD")

def query(tipo,llave,valor):
    '''Función encargada de hacer querys requeridos con ayuda de 3 parámetros y validar según se requiera'''
    try:
        documentoDisenno = f"_design/{tipo}"
        nombreVista = f"por_{llave}"
        db[documentoDisenno]
        try:
            resultados = db.view(f"{tipo}/{nombreVista}",key=valor)
            return (row.value for row in resultados)
        except couchdb.http.ResourceNotFound:
            return(f'ERROR: La vista {resultados} no es válida, intenta con otro valor')
    except couchdb.ResourceNotFound:
        return(f'ERROR: Docuemnto no encontrado')
    
def menuQuery(tipo):
    '''Método para llamar los querys por tipo y evitar repetir el condicional multiples veces
    (str) -> none'''
    parametro = input("Se puede buscar usando los siguientes parámetros\n- id\n- Nombre\n- Carrera\n- Semestre\n\n Digite el parámetro de búsqueda: ").lower()
    valorParametro = input(f"Ingrese el valor del parámetro '{parametro}': ")
    res = query(tipo, parametro, valorParametro)
    total = 0
    if res is None:
        print(f'ERROR: No se encontró algun registro con {parametro} {valorParametro}')
    else:
        try:
            for x in res:
                print(x)
                total =+ 1
            sys.stdout.write(f'Datos encontrados: {total}')
        except:
            print(f'ERROR: No se pueden mostrar los valores consultados')
        finally:
            esperarUsuario()

def esperarUsuario():
    '''Input que hace de validacion
    (none) -> (none)'''
    input('\nPresiona enter para continuar')
    
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
        categoria = int(input("\n\n--- CATEGORIAS DISPONIBLES ---\n\n1. Artes y humanidades\n2. Ciencias básicas\n3. Tecnología\n\nSeleccione una opción: "))

        if categoria == 1:
            categoria = "Artes y humanidades"
        elif categoria == 2:
            categoria = "Ciencias básicas"
        elif categoria == 3:
            categoria = "Tecnología"
        else:
            print('Opción incorrecta. Intenta nuevamente')
            categoria = int(input("\n\n--- CATEGORIAS DIPONIBLES ---\n\n1. Artes y humanidades\n2. Ciencias básicas\n3. Tecnología\n\nSeleccione una opción: "))

        modalidad = int(input("\n\n--- MODALIDADES ---\n\n1. Presencial\n2. Remoto\n\nSeleccione una opción: "))
        if modalidad == 1:
            modalidad = "Presencial"
        elif modalidad == 2:
            modalidad = "Remoto"
        else:
            print('Opción incorrecta. Intenta nuevamente')
            modalidad = int(input("\n\n--- MODALIDADES ---\n\n1. Presencial\n2. Remoto\n\nSeleccione una opción: "))

        gratuito = int(input("\n¿Es el curso gratuito?\n\n1. Verdadero\n2. Falso\n\nSeleccione una opción: "))

        if gratuito == 1:
            gratuito = True
        elif gratuito == 2:
            gratuito = False
        else:
            print('Opción incorrecta. Intenta nuevamente')
            gratuito = int(input("¿Es el curso gratuito?\n\n1. Verdadero\n2. Falso\n\nSeleccione una opción: "))
        
        #Si el curso es gratuito, su precio es 0, no?
        if gratuito == False:
            precio = float(input("\nIngrese el precio del curso: "))
        else:
            precio = 0

        duracion = int(input("\nIngrese la duración del curso (en horas): "))
        certificado = int(input("\n¿El curso tiene certificado?\n\n1. Verdadero\n2. Falso\n\nSeleccione una opción: "))

        if certificado == 1:
            certificado = True
        elif certificado == 2:
            certificado = False
        else:
            print('Opción incorrecta. Intenta nuevamente')
            certificado = int(input("¿El curso tiene certificado?\n\n1. Verdadero\n2. Falso)\n\nSeleccione una opción: "))


        calPromedio = float(input("\nIngrese la calificación promedio del curso (0.0 a 5.0): "))

        curso = {
            "tipo":tipo,
            "id":id,
            "nombre":nombre,
            "categoria":categoria,
            "modalidad":modalidad,
            "esGratuito":gratuito,
            "precio":precio,
            "duracion":duracion,  
            "esCertificable":certificado,
            "calPromedio":calPromedio
        }

        db.save(curso)
        validar_guardado(curso["_id"]) 

def menu(nombre_user,aarch):
    '''Función encargada de ejecutar la funcionalidad completa de la app
    (none) -> (none)'''
    while True:
        limpiarPantalla(aarch)
        opcion = int(input(f"\n\n\|..-Corriendo desde SO {aarch}-..|/\n\nHola {nombre_user}\n\n1. Creación de valores\n2. Consulta de valores\n3. Salir\n\nDigita una opción: "))
        
        #Creación de objetos
        if (opcion == 1):
            opc1 = int(input("¿Qué tipo de rol desea crear?: \n1. Aprendiz\n2. Tutor\n3. Curso\n"))
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
            opc1 = int(input("Validaciones disponibles\n\n1. Consultar aprendiz\n2. Consultar docente\n3. Consultar curso\n\nDigita una opción: "))
            
            if (opc1 == 1):
                tipo = "aprendiz"
                menuQuery(tipo)

            elif (opc1 == 2):
                tipo = "tutor"
                menuQuery(tipo)

            elif (opc1 == 3):
                tipo = "curso"
                parametro = input("- id\n- Nombre\n- Categoria\n- Modalidad\n- esGratuito\n- esCertificable\n- Precio \n- Duracion \n- Calificación\n\nDigite el parámetro de búsqueda (tal cual es mostrado): ")
                if parametro != 'esGratuito' or 'esCertificable':
                    parametro.lower()
                elif parametro == 'esGratuito' or 'esCertificable':
                    valorParametro = input(f'¿Buscas si {parametro} es verdadero o falso?: ')
                    if valorParametro == 'verdadero':
                        valorParametro = True
                    elif valorParametro  == 'falso':
                        valorParametro = False
                    else:
                        print('ERROR: Debes escribir si es "verdadero" o "falso"')
                        valorParametro = input(f'¿Buscas si {parametro} es verdadero o falso?: ')

                elif parametro == 'precio' or 'duracion' or 'calificacion':
                    parametro = float(parametro)
                else:
                    valorParametro = input(f"Ingrese el valor del parámetro '{parametro}': ")
                    res = query(tipo, parametro, valorParametro)
                    total = 0
                    if res is None:
                        print(f'ERROR: No se encontró algun registro con {parametro} {valorParametro}')
                    else:
                        try:
                            for x in res:
                                print(x)
                                total =+ 1
                            sys.stdout.write(f'Datos encontrados: {total}')
                        except:
                            print(f'ERROR: No se pueden mostrar los valores consultados')
                        finally:
                            esperarUsuario()
            else:
                print("Opción Inválida. Proporcione una opción correcta\n")
                opc1 = int(input("Validaciones disponibles\n\n1. Consultar aprendiz\n2. Consultar docente\n3. Consultar curso\n\nDigita una opción: "))

        
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
        print(f'\nBBDD {db_name} encontrada')
        db = couch_server[db_name]
except couchdb.Unauthorized:
    print('Usuario o Clave Incorrectas. Intenta nuevamente')
    exit(2)
except:
    print(f'No se encontró la base de datos {db_name}, será creada')
    db = couch_server.create(db_name)

def main(aarch):
    '''Llama los módulos requeridos para la ejecución del programa
    (none) -> (none)'''
    try:
        nombre_user = input('BIENVENIDO\nIngresa tu nombre: ')
        menu(nombre_user,aarch)
    except KeyboardInterrupt:
        salida = input('\n¿Deseas salir de la aplicación? (S/N): ').lower()
        if salida == 's':
            exit(0)
        else:
            menu(nombre_user,aarch)

#EJECUCION
if __name__ == '__main__':
    aarch = detectarArquitectura()
    main(aarch)
    


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
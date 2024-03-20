#Proyecto Bases de Datos 2
#Desarrollado por Sebastian Balanta

#IMPORTS
import couchdb
import subprocess,time,os,sys

#CODIGOS DE ERROR
    #1 SIN ERROR
    #2 USU/PASS INVALIDA
    #3 CONEXION RECHAZADA / SERVICIO NO DISPONIBLE

#DATOS
user = "testing" #USER
pwd = "testing123*-" #PASS
host = "127.0.0.1" #IP/LOCALHOST
port = "5984" #PORT
db = "cli_recommendation" #NOMBRE DOC BBDD
url = (f'http://{user}:{pwd}@{host}:{port}/')

#CONEXION BBDD
try:
    couch_server = couchdb.Server(url)
except:
    print(f'ERROR: No se puede conectar a {host}. Abortando')
    exit(3)

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
    esperarUsuario()

def query(tipoQuery, tipoFiltro, llave, valor):
    '''Función encargada de hacer querys requeridos con ayuda de 4 parámetros y validar según se requiera
    \ntipoQuery\n\n1) Consulta\n2) Actualiza\n3) Elimina\n'''
    
    documentoDisenno = f"_design/{tipoFiltro}"
    nombreVista = f"por{llave}"

    if tipoQuery == 1:
        #Consultar | PRINCIPAL
        try:
            db[documentoDisenno]
            resultados = db.view(f"{tipoFiltro}/{nombreVista}",key=valor)
            return (list(row.value for row in resultados))
        
        except couchdb.http.ResourceNotFound:
            return(f'ERROR: La vista {documentoDisenno} no es válida, intenta con otro valor')
        
    elif tipoQuery == 2:
        #Actualizar

        # def Update(doc_id, data):
        #     doc = db[doc_id]
        #     doc.update(data)
        #     db.save(doc)
        try:
            db[documentoDisenno]
            resultados = db.view(f"{tipoFiltro}/{nombreVista}",key=valor)
            linea = 0
            for line in resultados:
                datos = (f'{linea}. {line}')
                linea += 1
            return (datos)
        
        except couchdb.http.ResourceNotFound:
            return(f'ERROR: La vista {documentoDisenno} no es válida, intenta con otro valor')
    #Eliminar
    elif tipoQuery == 3:
        try:
            db[documentoDisenno]
            resultados = db.view(f"{tipoFiltro}/{nombreVista}",key=valor)

            for dato in resultados:
                db.delete(db[dato.id])
            return (True)
        
        except couchdb.http.ResourceNotFound:
            print(f'ERROR: La vista {documentoDisenno} no es válida, intenta con otro valor')
            return (False)
    else:
        return(f'ERROR GENERAL. Intenta nuevamente')
    
def menuQuery(tipoQuery,tipoFiltro):
    '''Método para llamar los querys por tipo y evitar repetir el condicional multiples veces'''

    parametro = input("Se puede buscar usando los siguientes parámetros\n- id\n- Nombre\n- Carrera\n- Semestre\n\n Digite el parámetro de búsqueda: ").title()
    valorParametro = input(f"Ingrese el valor del parámetro {parametro}: ")
    res = query(tipoQuery, tipoFiltro, parametro, valorParametro)
    total = 0
    if len(res) == 0:
        print(f'ERROR: No se encontró algun registro de {valorParametro} con {parametro}')
        esperarUsuario()
        sys.stdout.write(f'\nDatos encontrados: {total}')
    else:
        try:
            for x in res:
                print(x)
                total += 1
            sys.stdout.write(f'\nDatos encontrados: {total}')
        except:
            print(f'\nERROR: No se pueden mostrar los valores consultados')
        finally:
            esperarUsuario()

def esperarUsuario():
    '''Funcion con input que juega el papel de validador'''

    input('\nPresiona enter para continuar... ')
    
def creacionRol(opc):
    '''Función encargada de ejecutar según sea necesario la creación de objetos con ayuda de un argumento entero'''

    cursos = []
    if opc == 1:
        tipo = "Aprendiz"
        id = input("Ingrese el ID del aprendiz: ")
        nombre = input("Ingrese el nombre del aprendiz: ")
        carrera = input("Ingrese la carrera del aprendiz: ")
        semestre = int(input("Ingrese el semestre cursado del aprendiz: "))
        agregarCurso = input('\nLe gustaria agregar a este estudiante un curso previamente creado? (S/N): ').lower()

        if agregarCurso == 's':
            curso =  int(input("Ingrese ID del curso al cual asiste el aprendiz"))
            cursos.append(curso)
        else:
            print('\nAprendiz nuevo, no será agregado a ningún curso')
            esperarUsuario()

        aprendiz = {
            "tipo":tipo,
            "id":id,
            "nombre":nombre,
            "carrera":carrera,
            "cursos":cursos,
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
        alumnos = []
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
        estudiante = input('\nDesea agregar algún estudiante por ID al curso? (S/N): ').lower()
        if estudiante == 's':
            identificacionEstudiante = int(input('Ingrese el código del estudiante: '))
            alumnos.append(identificacionEstudiante)
        else:
            print('\nAprendiz nuevo, no será agregado a ningún curso')
            esperarUsuario()

        curso = {
            "tipo":tipo,
            "id":id,
            "nombre":nombre,
            "categoria":categoria,
            "modalidad":modalidad,
            "gratuito":gratuito,
            "precio":precio,
            "duracion":duracion,  
            "certificable":certificado,
            "alumnos":alumnos,
            "calPromedio":calPromedio
        }

        db.save(curso)
        validar_guardado(curso["_id"]) 

def menu(nombre_user,aarch):
    '''Función encargada de manejar el menu principal'''
    while True:
        limpiarPantalla(aarch)
        opcion = int(input(f"\n\n\|..-  Corriendo desde SO: {aarch}  -..|/\n\nHola {nombre_user}\n\n1. Creación de valores\n2. Consulta de valores\n3. Actualización de valores\n4. Eliminación de valores\n5. Salir\n\nDigita una opción: "))
        
        #Creación
        if (opcion == 1):
            limpiarPantalla(aarch)
            opc1 = int(input('--ROLES DISPONIBLES-- \n\n1. Aprendiz\n2. Tutor\n3. Curso\n\n¿Qué tipo de rol deseas crear?: '))
            if opc1 == 1:
                creacionRol(1)
                pass
            
            elif opc1 == 2:
                creacionRol(2)
                pass
                
            elif opc1 == 3:
                creacionRol(3)
                pass

            else:
                print("Opción Inválida. Indique una opción correcta.")
        
        #Consulta
        elif (opcion == 2):
            limpiarPantalla(aarch)
            opc1 = int(input("Validaciones disponibles\n\n1. Consultar aprendiz\n2. Consultar tutor\n3. Consultar curso\n\nDigita una opción: "))
            
            if (opc1 == 1):
                tipoFiltro = "aprendiz"
                tipoQuery = 1
                menuQuery(tipoQuery, tipoFiltro)

            elif (opc1 == 2):
                tipoFiltro = "tutor"
                tipoQuery = 1
                menuQuery(tipoQuery, tipoFiltro)

            elif (opc1 == 3):
                tipoFiltro = "curso"
                tipoQuery = 1
                parametro = input("- id\n- Nombre\n- Categoria\n- Modalidad\n- Gratuito\n- Certificable\n- Precio \n- Duración \n- Calificación\n\nDigite el parámetro de búsqueda sin tíldes: ").title()
                if parametro == 'Gratuito' or 'Certificable':
                    valorParametro = input(f'¿Buscas si el {tipoFiltro} es {parametro}? (Escribe verdadero/falso según corresponda): ')
                    if valorParametro == 'verdadero':
                        valorParametro = True
                    elif valorParametro  == 'falso':
                        valorParametro = False
                    else:
                        print('ERROR: Debes escribir si es "verdadero" o "falso"')
                        valorParametro = input(f'¿Buscas si el {tipoFiltro} es {parametro}? (Escribe verdadero/falso según corresponda): ')

                if parametro == 'Precio' or 'Duracion' or 'Calificacion':
                    parametro = float(parametro)
                
                valorParametro = input(f"Ingrese el valor del parámetro {parametro}: ")
                res = query(tipoQuery, tipoFiltro, parametro, valorParametro)
                total = 0

                if len(res) == 0:
                    print(f'ERROR: No se encontró algún registro de {valorParametro} por {parametro}')
                else:
                    try:
                        for x in res:
                            print(x)
                            total =+ 1
                        sys.stdout.write(f'\nDatos encontrados: {total}')
                    except:
                        print(f'\nERROR: No se pueden mostrar los valores consultados')
                    finally:
                        esperarUsuario()
            else:
                print("Opción Inválida. Proporcione una opción correcta\n")
                opc1 = int(input("Validaciones disponibles\n\n1. Consultar aprendiz\n2. Consultar docente\n3. Consultar curso\n\nDigita una opción: "))

        #Actualización
        elif (opcion == 3):
            id = input('Ingrese el ID del objeto que desea actualizar (se puede obtener usando el módulo de consulta): ')
            query
            
        #Eliminación
        elif (opcion == 4):
            tipo = int(input('--TIPOS DISPONIBLE--\n\n1. Aprendiz\n2. Tutor\n3. Curso\n\nIngrese qué tipo de entrada desea borrar: '))
            id = input('Ingrese el ID asigando del tipo que desea eliminar (se puede obtener usando el módulo de consulta): ')
            #Eliminar Aprendiz
            if tipo == 1:
                tipo = 'aprendiz'
                valor = query(3,tipo,'Id',id)
                if valor == True:
                    print(f'El {tipo} identificado con {id} ha sido eliminado exitosamente!\n')
                else:
                    print(f'El {tipo} identificado con {id} NO ha podido ser eliminado!\n')
                esperarUsuario()
            #Eliminar Tutor
            elif tipo == 2:
                tipo = 'tutor'
                valor = query(3,tipo,'Id',id)
                if valor == True:
                    print(f'El {tipo} identificado con {id} ha sido eliminado exitosamente!\n')
                else:
                    print(f'El {tipo} identificado con {id} NO ha podido ser eliminado!\n')
                esperarUsuario()
            #Eliminar Curso
            elif tipo == 3:
                tipo = 'curso'
                valor = query(3,tipo,'Id',id)
                if valor == True:
                    print(f'El {tipo} identificado con {id} ha sido eliminado exitosamente!\n')
                else:
                    print(f'El {tipo} identificado con {id} NO ha podido ser eliminado!\n')
                esperarUsuario()

            else:
                print('\nERROR: Sus parámetros de búsqueda no coinciden con los nuestros\n')                        
        #Salida
        elif (opcion == 5): 
            exit(1) #Sale con código de error 1, básicamente sin error

        else:
            print("Opción Inválida. Proporcione una opción correcta.")

def main(aarch):
    '''Llama los módulos requeridos para la ejecución del programa
    (none) -> (none)'''
    try:
        nombre_user = input('\nBIENVENIDO\nIngresa tu nombre: ')
        esperarUsuario()
        menu(nombre_user,aarch)
    except KeyboardInterrupt:
        salida = input('\n¿Deseas salir de la aplicación? (S/N): ').lower()
        if salida == 's':
            exit(0)
        else:
            menu(nombre_user,aarch)

#EJECUCION
if (__name__ == '__main__'):
    aarch = detectarArquitectura()
    limpiarPantalla(aarch)
    try:
        #Login
        print(f"\nEstableciendo conexión con {host}:{port} ...")
        time.sleep(0.8)
        couch_server.login(user,pwd)
        if (db in couch_server):
            print(f'\nBBDD {db} encontrada')
            db = couch_server[db]
            main(aarch)

    except couchdb.HTTPError:
        print(f'ERROR COUCHDB: Credenciales inválidas. Intenta nuevamente')
        exit(2)
    except ConnectionRefusedError:
        print(f'\nERROR: El host {host}:{port} no se encuentra disponible. ¿Está corriendo el servicio de couchDB?\n')
        exit(3)
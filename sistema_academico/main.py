from views import (
    crear_estudiante,
    obtener_estudiante,
    buscar_estudiantes,
    actualizar_estudiante,
    eliminar_estudiante,
    agregar_nota,
    materias_ofertadas,
    estudiantes_en_comun,
    
    crear_docente,
    obtener_docentes,
    obtener_docente,
    buscar_docentes,
    actualizar_docente,
    eliminar_docente,

    crear_asignatura,
    obtener_asignaturas,
    obtener_asignatura,
    buscar_asignaturas,
    actualizar_asignatura,
    eliminar_asignatura,

    crear_curso,
    obtener_cursos,
    obtener_curso,
    buscar_cursos,
    actualizar_curso,
    eliminar_curso
)

def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_estudiantes(estudiantes):
    print("\n--- ESTUDIANTES ---")
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return

    for estudiante in estudiantes:
        print(estudiante)

def opcion_agregar_nota():
    print("\n--- AGREGAR NOTA ---")

    try:
        id_estudiante = int(input("ID del estudiante: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        pausa()
        return

    materia = input("Materia: ")

    try:
        nota = float(input("Nota (0-20): "))
    except ValueError:
        print("La nota debe ser un número.")
        pausa()
        return

    exito, mensaje = agregar_nota(
        id_estudiante,
        materia,
        nota
    )

    print(mensaje)
    pausa()

def opcion_ver_promedio():
    print("\n--- VER PROMEDIO ---")

    try:
        id_estudiante = int(input("ID del estudiante: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        pausa()
        return

    estudiante = obtener_estudiante(id_estudiante)

    if estudiante is None:
        print(f"No existe un estudiante con id {id_estudiante}.")
    else:
        print(
            f"Estudiante: {estudiante.obtener_nombre_completo()}"
        )
        print(
            f"Promedio: {estudiante.obtener_promedio():.2f}"
        )

    pausa()

def opcion_materias_comunes():
    print("\n--- MATERIAS EN COMÚN ---")

    try:
        id_a = int(input("ID del primer estudiante: "))
        id_b = int(input("ID del segundo estudiante: "))
    except ValueError:
        print("Los IDs deben ser números enteros.")
        pausa()
        return

    resultado = estudiantes_en_comun(id_a, id_b)

    if resultado[0] is False:
        print(resultado[1])
    else:
        materias = resultado[1]

        if materias:
            print("\nMaterias en común:")
            for materia in sorted(materias):
                print(f"- {materia}")
        else:
            print("Los estudiantes no tienen materias en común.")

    pausa()

def mostrar_docentes(docentes):
    print("\n--- DOCENTES ---")

    if not docentes:
        print("No hay docentes registrados.")
        return

    for docente in docentes:
        print(
            f"[{docente.id}] "
            f"{docente.obtener_nombre_completo()} - "
            f"{docente.especialidad}"
        )


def mostrar_asignaturas(asignaturas):
    print("\n--- ASIGNATURAS ---")

    if not asignaturas:
        print("No hay asignaturas registradas.")
        return

    for asignatura in asignaturas:
        print(
            f"[{asignatura.id}] "
            f"{asignatura.nombre} - "
            f"{asignatura.creditos} créditos"
        )


def mostrar_cursos(cursos):
    print("\n--- CURSOS ---")

    if not cursos:
        print("No hay cursos registrados.")
        return

    for curso in cursos:
        print(
            f"[{curso.id}] "
            f"{curso.nombre} - "
            f"Asignatura: {curso.asignatura_id} - "
            f"Docente: {curso.docente_id}"
        )


# =========================================================
# ESTUDIANTES
# =========================================================

def menu_estudiantes():
    while True:
        print("\n========== ESTUDIANTES ==========")
        print("1. Crear estudiante")
        print("2. Ver estudiantes")
        print("3. Ver estudiante por ID")
        print("4. Buscar estudiantes")
        print("5. Actualizar estudiante")
        print("6. Eliminar estudiante")
        print("7. Agregar nota")
        print("8. Ver promedio")
        print("9. Materias en común")
        print("0. Regresar")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            email = input("Email: ")
            carnet = input("Carnet: ")

            exito, mensaje = crear_estudiante(
                nombre,
                apellido,
                email,
                carnet
            )

            print(mensaje)
            pausa()

        elif opcion == "2":
            mostrar_estudiantes()

        elif opcion == "3":
            try:
                id_estudiante = int(
                    input("ID del estudiante: ")
                )
            except ValueError:
                print("El ID debe ser un número entero.")
                pausa()
                continue

            estudiante = obtener_estudiante(id_estudiante)

            if estudiante:
                print(estudiante)
                print(f"Materias: {sorted(estudiante.materias)}")
                print(f"Notas: {estudiante.notas}")
            else:
                print(
                    f"No existe un estudiante con id {id_estudiante}."
                )

            pausa()

        elif opcion == "4":
            termino = input(
                "Ingrese nombre, apellido, email o carnet: "
            )

            resultados = buscar_estudiantes(termino)

            if resultados:
                mostrar_estudiantes(resultados)
            else:
                print("No se encontraron estudiantes.")
                pausa()

        elif opcion == "5":
            try:
                id_estudiante = int(
                    input("ID del estudiante: ")
                )
            except ValueError:
                print("El ID debe ser un número entero.")
                pausa()
                continue

            nombre = input("Nuevo nombre: ")
            apellido = input("Nuevo apellido: ")
            email = input("Nuevo email: ")
            carnet = input("Nuevo carnet: ")

            cambios = {
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "carnet": carnet
            }

            exito, mensaje = actualizar_estudiante(
                id_estudiante,
                cambios
            )

            print(mensaje)
            pausa()

        elif opcion == "6":
            try:
                id_estudiante = int(
                    input("ID del estudiante: ")
                )
            except ValueError:
                print("El ID debe ser un número entero.")
                pausa()
                continue

            exito, mensaje = eliminar_estudiante(
                id_estudiante
            )

            print(mensaje)
            pausa()

        elif opcion == "7":
            opcion_agregar_nota()

        elif opcion == "8":
            opcion_ver_promedio()

        elif opcion == "9":
            opcion_materias_comunes()

        elif opcion == "0":
            break

        else:
            print("Opción no válida.")
            pausa()

# =========================================================
# DOCENTES
# =========================================================

def menu_docentes():
    while True:
        print("\n===== DOCENTES =====")
        print("1. Crear docente")
        print("2. Listar docentes")
        print("3. Buscar docente")
        print("4. Actualizar docente")
        print("5. Eliminar docente")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            email = input("Email: ")
            especialidad = input("Especialidad: ")

            exito, mensaje = crear_docente(
                nombre,
                apellido,
                email,
                especialidad
            )

            print(mensaje)
            pausa()

        elif opcion == "2":
            mostrar_docentes(obtener_docentes())
            pausa()

        elif opcion == "3":
            termino = input("Ingrese nombre, apellido, email o especialidad: ")
            mostrar_docentes(buscar_docentes(termino))
            pausa()

        elif opcion == "4":
            try:
                id_docente = int(input("ID del docente: "))
            except ValueError:
                print("El ID debe ser un número.")
                pausa()
                continue

            docente = obtener_docente(id_docente)

            if docente is None:
                print("No existe ese docente.")
            else:
                nombre = input(f"Nombre [{docente.nombre}]: ")
                apellido = input(f"Apellido [{docente.apellido}]: ")
                email = input(f"Email [{docente.email}]: ")
                especialidad = input(
                    f"Especialidad [{docente.especialidad}]: "
                )

                nombre = nombre or docente.nombre
                apellido = apellido or docente.apellido
                email = email or docente.email
                especialidad = especialidad or docente.especialidad

                exito, mensaje = actualizar_docente(
                    id_docente,
                    nombre,
                    apellido,
                    email,
                    especialidad
                )

                print(mensaje)

            pausa()

        elif opcion == "5":
            try:
                id_docente = int(input("ID del docente: "))
            except ValueError:
                print("El ID debe ser un número.")
                pausa()
                continue

            exito, mensaje = eliminar_docente(id_docente)
            print(mensaje)
            pausa()

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")


# =========================================================
# ASIGNATURAS
# =========================================================

def menu_asignaturas():
    while True:
        print("\n===== ASIGNATURAS =====")
        print("1. Crear asignatura")
        print("2. Listar asignaturas")
        print("3. Buscar asignatura")
        print("4. Actualizar asignatura")
        print("5. Eliminar asignatura")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            creditos = input("Créditos: ")

            exito, mensaje = crear_asignatura(
                nombre,
                creditos
            )

            print(mensaje)
            pausa()

        elif opcion == "2":
            mostrar_asignaturas(obtener_asignaturas())
            pausa()

        elif opcion == "3":
            termino = input("Nombre de la asignatura: ")
            mostrar_asignaturas(buscar_asignaturas(termino))
            pausa()

        elif opcion == "4":
            try:
                id_asignatura = int(input("ID de la asignatura: "))
            except ValueError:
                print("El ID debe ser un número.")
                pausa()
                continue

            asignatura = obtener_asignatura(id_asignatura)

            if asignatura is None:
                print("No existe esa asignatura.")
            else:
                nombre = input(f"Nombre [{asignatura.nombre}]: ")
                creditos = input(
                    f"Créditos [{asignatura.creditos}]: "
                )

                nombre = nombre or asignatura.nombre
                creditos = creditos or str(asignatura.creditos)

                exito, mensaje = actualizar_asignatura(
                    id_asignatura,
                    nombre,
                    creditos
                )

                print(mensaje)

            pausa()

        elif opcion == "5":
            try:
                id_asignatura = int(
                    input("ID de la asignatura: ")
                )
            except ValueError:
                print("El ID debe ser un número.")
                pausa()
                continue

            exito, mensaje = eliminar_asignatura(id_asignatura)
            print(mensaje)
            pausa()

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")


# =========================================================
# CURSOS
# =========================================================

def menu_cursos():
    while True:
        print("\n===== CURSOS =====")
        print("1. Crear curso")
        print("2. Listar cursos")
        print("3. Buscar curso")
        print("4. Actualizar curso")
        print("5. Eliminar curso")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del curso: ")
            asignatura_id = input("ID de la asignatura: ")
            docente_id = input("ID del docente: ")

            exito, mensaje = crear_curso(
                nombre,
                asignatura_id,
                docente_id
            )

            print(mensaje)
            pausa()

        elif opcion == "2":
            mostrar_cursos(obtener_cursos())
            pausa()

        elif opcion == "3":
            termino = input("Nombre del curso: ")
            mostrar_cursos(buscar_cursos(termino))
            pausa()

        elif opcion == "4":
            try:
                id_curso = int(input("ID del curso: "))
            except ValueError:
                print("El ID debe ser un número.")
                pausa()
                continue

            curso = obtener_curso(id_curso)

            if curso is None:
                print("No existe ese curso.")
            else:
                nombre = input(f"Nombre [{curso.nombre}]: ")
                asignatura_id = input(
                    f"ID asignatura [{curso.asignatura_id}]: "
                )
                docente_id = input(
                    f"ID docente [{curso.docente_id}]: "
                )

                nombre = nombre or curso.nombre
                asignatura_id = (
                    asignatura_id or str(curso.asignatura_id)
                )
                docente_id = (
                    docente_id or str(curso.docente_id)
                )

                exito, mensaje = actualizar_curso(
                    id_curso,
                    nombre,
                    asignatura_id,
                    docente_id
                )

                print(mensaje)

            pausa()

        elif opcion == "5":
            try:
                id_curso = int(input("ID del curso: "))
            except ValueError:
                print("El ID debe ser un número.")
                pausa()
                continue

            exito, mensaje = eliminar_curso(id_curso)
            print(mensaje)
            pausa()

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")


# =========================================================
# MENÚ PRINCIPAL
# =========================================================

def main():
    while True:
        print("\n================================")
        print("     SISTEMA ACADÉMICO")
        print("================================")
        print("1. Estudiantes")
        print("2. Docentes")
        print("3. Asignaturas")
        print("4. Cursos")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_estudiantes()

        elif opcion == "2":
            menu_docentes()

        elif opcion == "3":
            menu_asignaturas()

        elif opcion == "4":
            menu_cursos()

        elif opcion == "0":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
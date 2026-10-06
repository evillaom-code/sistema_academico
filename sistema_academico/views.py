from models import Estudiante, Docente, Asignatura, Curso
from shared.json_manager import GestorJSON
from shared.herramientas import es_texto_valido, es_email_valido


# =========================================================
# GESTORES JSON
# =========================================================

gestor_estudiantes = GestorJSON("data/estudiantes.json")
gestor_docentes = GestorJSON("data/docentes.json")
gestor_asignaturas = GestorJSON("data/asignaturas.json")
gestor_cursos = GestorJSON("data/cursos.json")

def carnets_registrados(excepto_id=None):
    """Devuelve un SET con los carnets ya utilizados."""
    return {
        registro["carnet"].lower()
        for registro in gestor_estudiantes.leer()
        if registro["id"] != excepto_id
    }
# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def siguiente_id(gestor):
    registros = gestor.leer()

    if not registros:
        return 1

    return max(registro["id"] for registro in registros) + 1


# =========================================================
# ESTUDIANTES
# =========================================================

def crear_estudiante(nombre, apellido, email, carnet):
    if not es_texto_valido(nombre):
        return False, "El nombre es obligatorio"

    if not es_texto_valido(apellido):
        return False, "El apellido es obligatorio"

    if not es_email_valido(email):
        return False, "El email no tiene un formato válido"

    if not es_texto_valido(carnet):
        return False, "El carnet es obligatorio"

    if carnet.lower() in carnets_registrados():
        return False, "Ese carnet ya está registrado"

    estudiante = Estudiante(
        siguiente_id(gestor_estudiantes),
        nombre.strip(),
        apellido.strip(),
        email.strip(),
        carnet.strip()
    )

    registros = gestor_estudiantes.leer()
    registros.append(estudiante.a_diccionario())

    if not gestor_estudiantes.guardar(registros):
        return False, "No se pudo guardar el estudiante"

    return (
        True,
        f"Estudiante {estudiante.obtener_nombre_completo()} "
        f"creado con id {estudiante.id}"
    )

def obtener_estudiantes():
    registros = gestor_estudiantes.leer()

    return [
        Estudiante.desde_diccionario(registro)
        for registro in registros
    ]


def obtener_estudiante(id_estudiante):
    estudiantes = obtener_estudiantes()

    for estudiante in estudiantes:
        if estudiante.id == id_estudiante:
            return estudiante

    return None


def buscar_estudiantes(termino):
    termino = termino.lower().strip()

    estudiantes = obtener_estudiantes()

    encontrados = []

    for estudiante in estudiantes:
        if (
            termino in estudiante.nombre.lower()
            or termino in estudiante.apellido.lower()
            or termino in estudiante.email.lower()
            or termino in estudiante.carnet.lower()
        ):
            encontrados.append(estudiante)

    return encontrados


def actualizar_estudiante(id_estudiante, nombre, apellido, email, carnet):
    registros = gestor_estudiantes.leer()

    for registro in registros:
        if registro["id"] == id_estudiante:

            if not es_texto_valido(nombre):
                return False, "El nombre es obligatorio."

            if not es_texto_valido(apellido):
                return False, "El apellido es obligatorio."

            if not es_email_valido(email):
                return False, "El email no es válido."

            if not es_texto_valido(carnet):
                return False, "El carnet es obligatorio."

            for otro in registros:
                if otro["id"] != id_estudiante:
                    if otro["carnet"].lower() == carnet.lower():
                        return False, "Ese carnet ya pertenece a otro estudiante."

                    if otro["email"].lower() == email.lower():
                        return False, "Ese email ya pertenece a otro estudiante."

            registro["nombre"] = nombre
            registro["apellido"] = apellido
            registro["email"] = email
            registro["carnet"] = carnet

            gestor_estudiantes.guardar(registros)

            return True, "Estudiante actualizado correctamente."

    return False, "No existe ese estudiante."


def eliminar_estudiante(id_estudiante):
    registros = gestor_estudiantes.leer()

    nuevos_registros = [
        registro
        for registro in registros
        if registro["id"] != id_estudiante
    ]

    if len(nuevos_registros) == len(registros):
        return False, "No existe ese estudiante."

    gestor_estudiantes.guardar(nuevos_registros)

    return True, "Estudiante eliminado correctamente."

def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota a un estudiante."""

    if not es_texto_valido(materia):
        return False, "La materia es obligatoria"

    try:
        nota = float(nota)
    except (ValueError, TypeError):
        return False, "La nota debe ser un número"

    # La guía exige notas entre 0 y 20
    if nota < 0 or nota > 20:
        return False, "La nota debe estar entre 0 y 20"

    estudiante = obtener_estudiante(id_estudiante)

    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"

    estudiante.agregar_nota(materia.strip(), nota)

    registros = gestor_estudiantes.leer()

    for indice, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            registros[indice] = estudiante.a_diccionario()
            break

    if not gestor_estudiantes.guardar(registros):
        return False, "No se pudo guardar la nota"

    return (
        True,
        f"Nota {nota} agregada en {materia} "
        f"al estudiante {estudiante.obtener_nombre_completo()}"
    )

def materias_ofertadas():
    """Devuelve un SET con todas las materias de todos los estudiantes."""

    materias = set()

    for estudiante in obtener_estudiantes():
        materias.update(estudiante.materias)

    return materias

def estudiantes_en_comun(id_a, id_b):
    """Devuelve las materias que comparten dos estudiantes."""

    estudiante_a = obtener_estudiante(id_a)
    estudiante_b = obtener_estudiante(id_b)

    if estudiante_a is None:
        return False, f"No existe el estudiante con id {id_a}"

    if estudiante_b is None:
        return False, f"No existe el estudiante con id {id_b}"

    materias_comunes = estudiante_a.materias_en_comun(estudiante_b)

    return True, materias_comunes


# =========================================================
# DOCENTES
# =========================================================

def crear_docente(nombre, apellido, email, especialidad):
    if not es_texto_valido(nombre):
        return False, "El nombre es obligatorio."

    if not es_texto_valido(apellido):
        return False, "El apellido es obligatorio."

    if not es_email_valido(email):
        return False, "El email no es válido."

    if not es_texto_valido(especialidad):
        return False, "La especialidad es obligatoria."

    registros = gestor_docentes.leer()

    for registro in registros:
        if registro["email"].lower() == email.lower():
            return False, "Ya existe un docente con ese email."

    docente = Docente(
        siguiente_id(gestor_docentes),
        nombre,
        apellido,
        email,
        especialidad
    )

    registros.append(docente.a_diccionario())
    gestor_docentes.guardar(registros)

    return True, "Docente creado correctamente."


def obtener_docentes():
    registros = gestor_docentes.leer()

    return [
        Docente.desde_diccionario(registro)
        for registro in registros
    ]


def obtener_docente(id_docente):
    docentes = obtener_docentes()

    for docente in docentes:
        if docente.id == id_docente:
            return docente

    return None


def buscar_docentes(termino):
    termino = termino.lower().strip()

    docentes = obtener_docentes()
    encontrados = []

    for docente in docentes:
        if (
            termino in docente.nombre.lower()
            or termino in docente.apellido.lower()
            or termino in docente.email.lower()
            or termino in docente.especialidad.lower()
        ):
            encontrados.append(docente)

    return encontrados


def actualizar_docente(
    id_docente,
    nombre,
    apellido,
    email,
    especialidad
):
    registros = gestor_docentes.leer()

    for registro in registros:
        if registro["id"] == id_docente:

            if not es_texto_valido(nombre):
                return False, "El nombre es obligatorio."

            if not es_texto_valido(apellido):
                return False, "El apellido es obligatorio."

            if not es_email_valido(email):
                return False, "El email no es válido."

            if not es_texto_valido(especialidad):
                return False, "La especialidad es obligatoria."

            registro["nombre"] = nombre
            registro["apellido"] = apellido
            registro["email"] = email
            registro["especialidad"] = especialidad

            gestor_docentes.guardar(registros)

            return True, "Docente actualizado correctamente."

    return False, "No existe ese docente."


def eliminar_docente(id_docente):
    registros = gestor_docentes.leer()

    nuevos_registros = [
        registro
        for registro in registros
        if registro["id"] != id_docente
    ]

    if len(nuevos_registros) == len(registros):
        return False, "No existe ese docente."

    gestor_docentes.guardar(nuevos_registros)

    return True, "Docente eliminado correctamente."


# =========================================================
# ASIGNATURAS
# =========================================================

def crear_asignatura(nombre, creditos):
    if not es_texto_valido(nombre):
        return False, "El nombre es obligatorio."

    try:
        creditos = int(creditos)
    except ValueError:
        return False, "Los créditos deben ser un número entero."

    if creditos <= 0:
        return False, "Los créditos deben ser mayores que cero."

    registros = gestor_asignaturas.leer()

    for registro in registros:
        if registro["nombre"].lower() == nombre.lower():
            return False, "Ya existe esa asignatura."

    asignatura = Asignatura(
        siguiente_id(gestor_asignaturas),
        nombre,
        creditos
    )

    registros.append(asignatura.a_diccionario())
    gestor_asignaturas.guardar(registros)

    return True, "Asignatura creada correctamente."


def obtener_asignaturas():
    registros = gestor_asignaturas.leer()

    return [
        Asignatura.desde_diccionario(registro)
        for registro in registros
    ]


def obtener_asignatura(id_asignatura):
    asignaturas = obtener_asignaturas()

    for asignatura in asignaturas:
        if asignatura.id == id_asignatura:
            return asignatura

    return None


def buscar_asignaturas(termino):
    termino = termino.lower().strip()

    asignaturas = obtener_asignaturas()
    encontrados = []

    for asignatura in asignaturas:
        if termino in asignatura.nombre.lower():
            encontrados.append(asignatura)

    return encontrados


def actualizar_asignatura(id_asignatura, nombre, creditos):
    registros = gestor_asignaturas.leer()

    for registro in registros:
        if registro["id"] == id_asignatura:

            if not es_texto_valido(nombre):
                return False, "El nombre es obligatorio."

            try:
                creditos = int(creditos)
            except ValueError:
                return False, "Los créditos deben ser un número entero."

            if creditos <= 0:
                return False, "Los créditos deben ser mayores que cero."

            registro["nombre"] = nombre
            registro["creditos"] = creditos

            gestor_asignaturas.guardar(registros)

            return True, "Asignatura actualizada correctamente."

    return False, "No existe esa asignatura."


def eliminar_asignatura(id_asignatura):
    registros = gestor_asignaturas.leer()

    nuevos_registros = [
        registro
        for registro in registros
        if registro["id"] != id_asignatura
    ]

    if len(nuevos_registros) == len(registros):
        return False, "No existe esa asignatura."

    gestor_asignaturas.guardar(nuevos_registros)

    return True, "Asignatura eliminada correctamente."


# =========================================================
# CURSOS
# =========================================================

def crear_curso(nombre, asignatura_id, docente_id):
    if not es_texto_valido(nombre):
        return False, "El nombre es obligatorio."

    try:
        asignatura_id = int(asignatura_id)
        docente_id = int(docente_id)
    except ValueError:
        return False, "Los IDs deben ser números enteros."

    if obtener_asignatura(asignatura_id) is None:
        return False, "La asignatura no existe."

    if obtener_docente(docente_id) is None:
        return False, "El docente no existe."

    registros = gestor_cursos.leer()

    curso = Curso(
        siguiente_id(gestor_cursos),
        nombre,
        asignatura_id,
        docente_id
    )

    registros.append(curso.a_diccionario())
    gestor_cursos.guardar(registros)

    return True, "Curso creado correctamente."


def obtener_cursos():
    registros = gestor_cursos.leer()

    return [
        Curso.desde_diccionario(registro)
        for registro in registros
    ]


def obtener_curso(id_curso):
    cursos = obtener_cursos()

    for curso in cursos:
        if curso.id == id_curso:
            return curso

    return None


def buscar_cursos(termino):
    termino = termino.lower().strip()

    cursos = obtener_cursos()
    encontrados = []

    for curso in cursos:
        if termino in curso.nombre.lower():
            encontrados.append(curso)

    return encontrados


def actualizar_curso(
    id_curso,
    nombre,
    asignatura_id,
    docente_id
):
    registros = gestor_cursos.leer()

    for registro in registros:
        if registro["id"] == id_curso:

            if not es_texto_valido(nombre):
                return False, "El nombre es obligatorio."

            try:
                asignatura_id = int(asignatura_id)
                docente_id = int(docente_id)
            except ValueError:
                return False, "Los IDs deben ser números enteros."

            if obtener_asignatura(asignatura_id) is None:
                return False, "La asignatura no existe."

            if obtener_docente(docente_id) is None:
                return False, "El docente no existe."

            registro["nombre"] = nombre
            registro["asignatura_id"] = asignatura_id
            registro["docente_id"] = docente_id

            gestor_cursos.guardar(registros)

            return True, "Curso actualizado correctamente."

    return False, "No existe ese curso."


def eliminar_curso(id_curso):
    registros = gestor_cursos.leer()

    nuevos_registros = [
        registro
        for registro in registros
        if registro["id"] != id_curso
    ]

    if len(nuevos_registros) == len(registros):
        return False, "No existe ese curso."

    gestor_cursos.guardar(nuevos_registros)

    return True, "Curso eliminado correctamente."
class Estudiante:
    """MODELO: representa a un estudiante. Usa las cuatro colecciones."""

    def __init__(
        self,
        id_estudiante,
        nombre,
        apellido,
        email,
        carnet,
        notas=None,
        materias=None
    ):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet

        # DICCIONARIO DE LISTAS:
        self.notas = notas if notas is not None else {}

        # CONJUNTO:
        self.materias = set(materias) if materias is not None else set()

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        self.inscribir_materia(materia)

        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        todas_las_notas = []

        for lista_notas in self.notas.values():
            todas_las_notas.extend(lista_notas)

        if not todas_las_notas:
            return 0

        return round(
            sum(todas_las_notas) / len(todas_las_notas),
            2
        )

    def materias_en_comun(self, otro_estudiante):
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,

           
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            materias=set(datos.get("materias", [])),
        )

    def __str__(self):
        return (
            f"[{self.carnet}] "
            f"{self.obtener_nombre_completo()} "
            f"- Promedio: {self.obtener_promedio():.2f}"
        )
class Docente:

    def __init__(
        self,
        id_docente,
        nombre,
        apellido,
        email,
        especialidad
    ):
        self.id = id_docente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.especialidad = especialidad

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "especialidad": self.especialidad,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["especialidad"],
        )


class Asignatura:

    def __init__(self, id_asignatura, nombre, creditos):
        self.id = id_asignatura
        self.nombre = nombre
        self.creditos = creditos

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "creditos": self.creditos,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["creditos"],
        )

class Curso:

    def __init__(
        self,
        id_curso,
        nombre,
        asignatura_id,
        docente_id
    ):
        self.id = id_curso
        self.nombre = nombre
        self.asignatura_id = asignatura_id
        self.docente_id = docente_id

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "asignatura_id": self.asignatura_id,
            "docente_id": self.docente_id,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["asignatura_id"],
            datos["docente_id"],
        )
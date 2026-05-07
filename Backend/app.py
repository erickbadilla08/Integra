from flask import Flask, request, jsonify
from flask_cors import CORS
from conexion import obtener_conexion

app = Flask(__name__)
CORS(app)


# -------------------------------------------------------
# Función para convertir CLOB/LOB de Oracle a texto normal
# -------------------------------------------------------
def convertir_lob(valor):
    if valor is None:
        return None

    # Oracle puede devolver CLOB como objeto LOB
    if hasattr(valor, "read"):
        return valor.read()

    return valor


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "Backend de Integra funcionando correctamente con Oracle"
    })


@app.route("/api/citas", methods=["POST"])
def registrar_cita():
    try:
        datos = request.get_json()

        nombre_completo = datos.get("nombre_completo")
        correo = datos.get("correo")
        telefono = datos.get("telefono")
        tipo_servicio = datos.get("tipo_servicio")
        modalidad = datos.get("modalidad")
        fecha_preferida = datos.get("fecha_preferida")
        hora_preferida = datos.get("hora_preferida")
        mensaje = datos.get("mensaje")

        if not nombre_completo or not correo or not telefono or not tipo_servicio or not modalidad or not fecha_preferida or not hora_preferida:
            return jsonify({
                "error": "Por favor complete los campos obligatorios."
            }), 400

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO citas (
                nombre_completo,
                correo,
                telefono,
                tipo_servicio,
                modalidad,
                fecha_preferida,
                hora_preferida,
                mensaje
            )
            VALUES (
                :nombre_completo,
                :correo,
                :telefono,
                :tipo_servicio,
                :modalidad,
                TO_DATE(:fecha_preferida, 'YYYY-MM-DD'),
                :hora_preferida,
                :mensaje
            )
        """

        cursor.execute(sql, {
            "nombre_completo": nombre_completo,
            "correo": correo,
            "telefono": telefono,
            "tipo_servicio": tipo_servicio,
            "modalidad": modalidad,
            "fecha_preferida": fecha_preferida,
            "hora_preferida": hora_preferida,
            "mensaje": mensaje
        })

        conexion.commit()

        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": "Solicitud enviada correctamente."
        }), 201

    except Exception as error:
        return jsonify({
            "error": "Ocurrió un error al registrar la cita.",
            "detalle": str(error)
        }), 500


@app.route("/api/contacto", methods=["POST"])
def registrar_contacto():
    try:
        datos = request.get_json()

        nombre = datos.get("nombre")
        correo = datos.get("correo")
        asunto = datos.get("asunto")
        mensaje = datos.get("mensaje")

        if not nombre or not correo or not asunto or not mensaje:
            return jsonify({
                "error": "Por favor complete los campos obligatorios."
            }), 400

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO mensajes_contacto (
                nombre,
                correo,
                asunto,
                mensaje
            )
            VALUES (
                :nombre,
                :correo,
                :asunto,
                :mensaje
            )
        """

        cursor.execute(sql, {
            "nombre": nombre,
            "correo": correo,
            "asunto": asunto,
            "mensaje": mensaje
        })

        conexion.commit()

        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": "Mensaje enviado correctamente."
        }), 201

    except Exception as error:
        return jsonify({
            "error": "Ocurrió un error al registrar el mensaje.",
            "detalle": str(error)
        }), 500


@app.route("/api/citas", methods=["GET"])
def obtener_citas():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT 
                id_cita,
                nombre_completo,
                correo,
                telefono,
                tipo_servicio,
                modalidad,
                TO_CHAR(fecha_preferida, 'YYYY-MM-DD') AS fecha_preferida,
                hora_preferida,
                mensaje,
                TO_CHAR(fecha_registro, 'YYYY-MM-DD HH24:MI:SS') AS fecha_registro
            FROM citas
            ORDER BY fecha_registro DESC
        """)

        citas = []

        for fila in cursor.fetchall():
            citas.append({
                "id_cita": fila[0],
                "nombre_completo": fila[1],
                "correo": fila[2],
                "telefono": fila[3],
                "tipo_servicio": fila[4],
                "modalidad": fila[5],
                "fecha_preferida": fila[6],
                "hora_preferida": fila[7],
                "mensaje": convertir_lob(fila[8]),
                "fecha_registro": fila[9]
            })

        cursor.close()
        conexion.close()

        return jsonify(citas), 200

    except Exception as error:
        return jsonify({
            "error": "Ocurrió un error al obtener las citas.",
            "detalle": str(error)
        }), 500


@app.route("/api/mensajes", methods=["GET"])
def obtener_mensajes():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT 
                id_mensaje,
                nombre,
                correo,
                asunto,
                mensaje,
                TO_CHAR(fecha_registro, 'YYYY-MM-DD HH24:MI:SS') AS fecha_registro
            FROM mensajes_contacto
            ORDER BY fecha_registro DESC
        """)

        mensajes = []

        for fila in cursor.fetchall():
            mensajes.append({
                "id_mensaje": fila[0],
                "nombre": fila[1],
                "correo": fila[2],
                "asunto": fila[3],
                "mensaje": convertir_lob(fila[4]),
                "fecha_registro": fila[5]
            })

        cursor.close()
        conexion.close()

        return jsonify(mensajes), 200

    except Exception as error:
        return jsonify({
            "error": "Ocurrió un error al obtener los mensajes.",
            "detalle": str(error)
        }), 500


@app.route("/api/servicios", methods=["GET"])
def obtener_servicios():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT 
                id_servicio,
                nombre,
                descripcion,
                estado
            FROM servicios
            ORDER BY id_servicio
        """)

        servicios = []

        for fila in cursor.fetchall():
            servicios.append({
                "id_servicio": fila[0],
                "nombre": fila[1],
                "descripcion": convertir_lob(fila[2]),
                "estado": fila[3]
            })

        cursor.close()
        conexion.close()

        return jsonify(servicios), 200

    except Exception as error:
        return jsonify({
            "error": "Ocurrió un error al obtener los servicios.",
            "detalle": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
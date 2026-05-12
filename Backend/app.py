import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# =====================================================
# CARGAR VARIABLES DE ENTORNO
# =====================================================
load_dotenv()

app = Flask(__name__)

# =====================================================
# CONFIGURACIÓN CORS
# Permite que el frontend en Netlify se comunique con Railway
# =====================================================
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://localhost:3000",
            "https://integra-psicologia.netlify.app",
            "https://splendorous-semolina-f3ceb6.netlify.app"
        ]
    }
})


# =====================================================
# CONEXIÓN A POSTGRESQL EN RAILWAY
# Railway entrega la variable DATABASE_URL automáticamente
# cuando agregas PostgreSQL al proyecto.
# =====================================================
def obtener_conexion():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise Exception("No se encontró la variable DATABASE_URL")

    conexion = psycopg2.connect(database_url)
    return conexion


# =====================================================
# CREACIÓN AUTOMÁTICA DE TABLAS
# Esta función crea las tablas si todavía no existen.
# =====================================================
def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id SERIAL PRIMARY KEY,
            servicio VARCHAR(120) NOT NULL,
            modalidad VARCHAR(50) NOT NULL,
            nombre_completo VARCHAR(150) NOT NULL,
            correo VARCHAR(150) NOT NULL,
            telefono VARCHAR(50) NOT NULL,
            fecha_hora_deseada VARCHAR(100) NOT NULL,
            mensaje TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes_contacto (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            correo VARCHAR(150) NOT NULL,
            mensaje TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conexion.commit()
    cursor.close()
    conexion.close()


# =====================================================
# IMPORTANTE PARA RAILWAY
# Railway ejecuta la app con Gunicorn.
# Por eso no siempre se ejecuta el bloque:
# if __name__ == "__main__":
#
# Este bloque verifica/crea las tablas al iniciar la app.
# =====================================================
with app.app_context():
    try:
        crear_tablas()
        print("Tablas verificadas correctamente.")
    except Exception as error:
        print("No se pudieron crear/verificar las tablas automáticamente:", error)


# =====================================================
# RUTA PRINCIPAL
# =====================================================
@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "Backend de Integra Psicoterapia funcionando correctamente en Railway"
    })


# =====================================================
# RUTA DE PRUEBA
# =====================================================
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "estado": "ok",
        "servicio": "Integra Psicoterapia API"
    })


# =====================================================
# REGISTRAR CITA
# =====================================================
@app.route("/api/citas", methods=["POST"])
def registrar_cita():
    try:
        datos = request.get_json()

        servicio = datos.get("service") or datos.get("servicio")
        modalidad = datos.get("modality") or datos.get("modalidad")
        nombre = datos.get("name") or datos.get("nombre_completo")
        correo = datos.get("email") or datos.get("correo")
        telefono = datos.get("phone") or datos.get("telefono")
        fecha_hora = datos.get("datetime") or datos.get("fecha_hora_deseada")
        mensaje = datos.get("reason") or datos.get("mensaje")

        if not servicio or not modalidad or not nombre or not correo or not telefono or not fecha_hora:
            return jsonify({
                "error": "Parece que falta algo aquí. Revisa los campos obligatorios."
            }), 400

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO citas (
                servicio,
                modalidad,
                nombre_completo,
                correo,
                telefono,
                fecha_hora_deseada,
                mensaje
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            servicio,
            modalidad,
            nombre,
            correo,
            telefono,
            fecha_hora,
            mensaje
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": "Solicitud enviada correctamente. Te contactaremos pronto."
        }), 201

    except Exception as error:
        return jsonify({
            "error": "Ocurrió un error al registrar la cita.",
            "detalle": str(error)
        }), 500


# =====================================================
# OBTENER CITAS
# =====================================================
@app.route("/api/citas", methods=["GET"])
def obtener_citas():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT 
                id,
                servicio,
                modalidad,
                nombre_completo,
                correo,
                telefono,
                fecha_hora_deseada,
                mensaje,
                TO_CHAR(fecha_registro, 'YYYY-MM-DD HH24:MI:SS') AS fecha_registro
            FROM citas
            ORDER BY fecha_registro DESC
        """)

        citas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return jsonify(citas), 200

    except Exception as error:
        return jsonify({
            "error": "Ocurrió un error al obtener las citas.",
            "detalle": str(error)
        }), 500


# =====================================================
# REGISTRAR MENSAJE DE CONTACTO
# =====================================================
@app.route("/api/contacto", methods=["POST"])
def registrar_contacto():
    try:
        datos = request.get_json()

        nombre = datos.get("name") or datos.get("nombre")
        correo = datos.get("email") or datos.get("correo")
        mensaje = datos.get("message") or datos.get("mensaje")

        if not nombre or not correo or not mensaje:
            return jsonify({
                "error": "Parece que falta algo aquí. Revisa los campos obligatorios."
            }), 400

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO mensajes_contacto (
                nombre,
                correo,
                mensaje
            )
            VALUES (%s, %s, %s)
        """, (
            nombre,
            correo,
            mensaje
        ))

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


# =====================================================
# OBTENER MENSAJES DE CONTACTO
# =====================================================
@app.route("/api/mensajes", methods=["GET"])
def obtener_mensajes():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT 
                id,
                nombre,
                correo,
                mensaje,
                TO_CHAR(fecha_registro, 'YYYY-MM-DD HH24:MI:SS') AS fecha_registro
            FROM mensajes_contacto
            ORDER BY fecha_registro DESC
        """)

        mensajes = cursor.fetchall()

        cursor.close()
        conexion.close()

        return jsonify(mensajes), 200

    except Exception as error:
        return jsonify({
            "error": "Ocurrió un error al obtener los mensajes.",
            "detalle": str(error)
        }), 500


# =====================================================
# EJECUCIÓN LOCAL
# Railway usa Gunicorn, pero esto sirve para probar local.
# =====================================================
if __name__ == "__main__":
    puerto = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=True)
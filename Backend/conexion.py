# =======================================================
# CONEXIÓN A BASE DE DATOS ORACLE
# Proyecto: Integra
# =======================================================

import oracledb

def obtener_conexion():
    """
    Crea la conexión con Oracle.
    Estos datos deben coincidir con la conexión que hiciste en SQL Developer.
    """

    conexion = oracledb.connect(
        user="integra",
        password="integra123",
        dsn="localhost:1521/orclpdb"
    )

    return conexion
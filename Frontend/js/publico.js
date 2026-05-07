// =======================================================
// JS PÚBLICO - INTEGRA
// Validaciones básicas y envío de formularios al backend
// =======================================================

// URL base del backend Flask.
// En local normalmente es http://127.0.0.1:5000
const API_URL = "http://127.0.0.1:5000";

// Espera a que cargue todo el documento HTML
document.addEventListener("DOMContentLoaded", function () {
    configurarFormularioCita();
    configurarFormularioContacto();
});

// -------------------------------------------------------
// Formulario de agenda de cita
// -------------------------------------------------------
function configurarFormularioCita() {
    const formCita = document.getElementById("formCita");

    if (!formCita) {
        return;
    }

    formCita.addEventListener("submit", async function (event) {
        event.preventDefault();

        const datos = {
            nombre_completo: document.getElementById("nombreCompleto").value.trim(),
            correo: document.getElementById("correoCita").value.trim(),
            telefono: document.getElementById("telefonoCita").value.trim(),
            tipo_servicio: document.getElementById("tipoServicio").value,
            modalidad: document.getElementById("modalidad").value,
            fecha_preferida: document.getElementById("fechaPreferida").value,
            hora_preferida: document.getElementById("horaPreferida").value,
            mensaje: document.getElementById("mensajeCita").value.trim()
        };

        if (
            !datos.nombre_completo ||
            !datos.correo ||
            !datos.telefono ||
            !datos.tipo_servicio ||
            !datos.modalidad ||
            !datos.fecha_preferida ||
            !datos.hora_preferida
        ) {
            mostrarMensaje(
                "mensajeCitaRespuesta",
                "Por favor complete los campos obligatorios.",
                "error"
            );
            return;
        }

        try {
            const respuesta = await fetch(`${API_URL}/api/citas`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(datos)
            });

            const resultado = await respuesta.json();

            if (respuesta.ok) {
                mostrarMensaje(
                    "mensajeCitaRespuesta",
                    "Solicitud enviada correctamente.",
                    "success"
                );
                formCita.reset();
            } else {
                mostrarMensaje(
                    "mensajeCitaRespuesta",
                    resultado.error || "Ocurrió un error al enviar la información.",
                    "error"
                );
            }

        } catch (error) {
            mostrarMensaje(
                "mensajeCitaRespuesta",
                "Ocurrió un error al enviar la información.",
                "error"
            );
        }
    });
}

// -------------------------------------------------------
// Formulario de contacto
// -------------------------------------------------------
function configurarFormularioContacto() {
    const formContacto = document.getElementById("formContacto");

    if (!formContacto) {
        return;
    }

    formContacto.addEventListener("submit", async function (event) {
        event.preventDefault();

        const datos = {
            nombre: document.getElementById("nombreContacto").value.trim(),
            correo: document.getElementById("correoContacto").value.trim(),
            asunto: document.getElementById("asuntoContacto").value.trim(),
            mensaje: document.getElementById("mensajeContacto").value.trim()
        };

        if (!datos.nombre || !datos.correo || !datos.asunto || !datos.mensaje) {
            mostrarMensaje(
                "mensajeContactoRespuesta",
                "Por favor complete los campos obligatorios.",
                "error"
            );
            return;
        }

        try {
            const respuesta = await fetch(`${API_URL}/api/contacto`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(datos)
            });

            const resultado = await respuesta.json();

            if (respuesta.ok) {
                mostrarMensaje(
                    "mensajeContactoRespuesta",
                    "Mensaje enviado correctamente.",
                    "success"
                );
                formContacto.reset();
            } else {
                mostrarMensaje(
                    "mensajeContactoRespuesta",
                    resultado.error || "Ocurrió un error al enviar la información.",
                    "error"
                );
            }

        } catch (error) {
            mostrarMensaje(
                "mensajeContactoRespuesta",
                "Ocurrió un error al enviar la información.",
                "error"
            );
        }
    });
}

// -------------------------------------------------------
// Mostrar mensajes en pantalla
// -------------------------------------------------------
function mostrarMensaje(idElemento, texto, tipo) {
    const contenedor = document.getElementById(idElemento);

    if (!contenedor) {
        return;
    }

    contenedor.textContent = texto;
    contenedor.className = "alert-message";

    if (tipo === "success") {
        contenedor.classList.add("alert-success-integra");
    } else {
        contenedor.classList.add("alert-error-integra");
    }
}
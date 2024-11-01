//! Integrar en el HTML  el código JavaScript que se encuentra en el archivo `script.js` 
//! Agregar <script src="https://unpkg.com/html5-qrcode/minified/html5-qrcode.min.js"></script> en el HTML
//! Agregar funcion de leer QR, Agregar funcion que muestra la explicacion, Agrega funcion al boton de finalizar recorrido
function onScanSuccess(decodedText) {
    console.log(`Código QR escaneado: ${decodedText}`);

    // Obtener el id_visitante de las cookies
    const idVisitante = getCookie("id_visitante");
    if (!idVisitante) {
        console.error("ID de visitante no encontrado en las cookies.");
        alert("Error: ID de visitante no encontrado. Por favor, inicia sesión nuevamente.");
        return;
    }

    // Realizar solicitud al backend con el QR decodificado y el id_visitante
    fetch("http://127.0.0.1:8000/scan_qr", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ qr_data: decodedText, id_visitante: idVisitante })
    })
    .then(response => response.json())
    .then(data => {
        // Insertar el resumen en el elemento <p class="text-scan">
        document.querySelector(".text-scan").textContent = data.resumen;
    })
    .catch(error => console.error("Error al obtener el resumen:", error));

    // Detener el escáner después de un escaneo exitoso
    html5QrCode.stop().then(() => {
        console.log("Escáner detenido.");
    }).catch((err) => {
        console.error("No se pudo detener el escáner:", err);
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


function onScanFailure(error) {
    console.warn(`Error de escaneo: ${error}`);
}

const html5QrCode = new Html5Qrcode("qr-reader");

document.addEventListener("DOMContentLoaded", () => {
    const config = { fps: 10, qrbox: { width: 250, height: 250 } };

    // Iniciar el escáner
    html5QrCode.start(
        { facingMode: "environment" },
        config,
        onScanSuccess,
        onScanFailure
    ).catch((err) => {
        console.error("Error al iniciar el escáner QR:", err);
    });
});
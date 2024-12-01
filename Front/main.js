const config = { fps: 10, qrbox:{ width: 250, height: 250 }}; // Configuración global para html5QrCode
let scanCount = 0; // Contador de escaneos

// Obtener los elementos del DOM
const textScanElement = document.querySelector(".text-scan");
const finalizarRecorridoButton = document.getElementById("finalizar-recorrido");
const continuarRecorridoButton = document.getElementById("continuar-recorrido");
const html5QrCode = new Html5Qrcode("qr-reader");
const startButton = document.querySelector(".start-button");
const modal = document.getElementById("modal");
const closeButton = document.querySelector(".close-button");
const userForm = document.getElementById("userForm");
const questionBox = document.getElementById("question");

// Mostrar el modal al hacer clic en el botón "INICIAR"
startButton.addEventListener("click", () => {
    modal.style.display = "block";
});

// Cerrar el modal al hacer clic en el botón de cerrar
closeButton.addEventListener("click", () => {
    modal.style.display = "none";
});

// Cerrar el modal al hacer clic fuera del contenido del modal
window.addEventListener("click", (event) => {
    if (event.target == modal) {
        modal.style.display = "none";
    }
});

// Manejar el envío del formulario
userForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    document.cookie = `name=${name}; path=/`;
    document.cookie = `age=${age}; path=/`;
    modal.style.display = "none";
    alert("Datos guardados correctamente.");
});

// Función para el escaneo exitoso
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
        console.log("Respuesta del backend:", data);
        // Mostrar el resumen con el efecto de escritura
        typeText(textScanElement, data.resumen, 25);

        // Incrementar el contador de escaneos
        scanCount += 1;
        console.log(`Escaneos realizados: ${scanCount}`);

        // Mostrar el botón "Finalizar recorrido" si se han escaneado 10 o más códigos QR
        if (scanCount >= 10) {
            finalizarRecorridoButton.style.display = "block";
        }
    })
    .catch(error => console.error("Error al obtener el resumen:", error));

    // Detener el escáner después de un escaneo exitoso
    html5QrCode.stop().then(() => {
        console.log("Escáner detenido.");
    }).catch((err) => {
        console.error("No se pudo detener el escáner:", err);
    });
}

//Funcion para mostrar la trivia
/*function showTrivia(){
    fetch ("http://127.0.0.1:8000/trivia"){
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ })
    }
}*/

// Función para obtener la cookie por su id_visitante
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Función para manejar errores en el escaneo
function onScanFailure(error) {
    console.warn(`Error de escaneo: ${error}`);
}

// Función para simular el efecto de escritura en un elemento
function typeText(element, text, delay = 25) {
    element.textContent = "";
    let index = 0;

    function type() {
        if (index < text.length) {
            element.textContent += text[index];
            index++;
            setTimeout(type, delay);
        }
    }

    type();
}

document.addEventListener("DOMContentLoaded", () => {
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

// Botón de continuar recorrido
continuarRecorridoButton.addEventListener("click", () => {
    // Limpiar el resumen
    textScanElement.textContent = "";

    // Detener el escáner si está activo y luego reiniciarlo
    html5QrCode.start(
        { facingMode: "environment" },
        config,
        onScanSuccess,
        onScanFailure
    ).catch((err) => {
        console.error("Error al iniciar el escáner QR:", err);
    });
});

// Botón de finalizar recorrido
finalizarRecorridoButton.addEventListener("click", () => {

    // Redirigir a la página de trivia
    window.location.href = "trivia.html";
});
// Obtener los elementos del DOM
const textScanElement = document.querySelector(".info-box");
const finalizarRecorridoButton = document.getElementById("finalizar-recorrido");
const continuarRecorridoButton = document.getElementById("continuar-recorrido");
const html5QrCode = new Html5Qrcode("qr-reader");

const questionBox = document.getElementById("question");
const triviaButton1 = document.getElementsByClassName("option1")
const triviaButton2 = document.getElementsByClassName("option2")
const triviaButton3 = document.getElementsByClassName("option3")
const triviaButton4 = document.getElementsByClassName("option4")

let scanCount = 0; // Contador de escaneos

// Función para enviar los datos del visitante al backend
function enviarDatos(nombre, edad) {
    fetch("http://127.0.0.1:8000/registrar_visitante", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, edad })
    })
    .then(response => {
        if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
        return response.json();
    })
    .then(data => {
        // Guardar el ID del visitante en las cookies
        document.cookie = `id_visitante=${data.id_visitante}; path=/; SameSite=Lax`;

    })
    .catch(error => {
        console.error("Error al enviar datos:", error);
        alert("Hubo un problema al registrar tus datos. Por favor, inténtalo de nuevo.");
    });
}

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

        // Detener el escáner después de un escaneo exitoso
        html5QrCode.stop().then(() => {
            console.log("Escáner detenido.");
        }).catch((err) => {
            console.error("No se pudo detener el escáner:", err);
        });
    })
    .catch(error => console.error("Error al obtener el resumen:", error));
}

//Funcion para mostrar la trivia
function showTrivia(){
    fetch ("http://127.0.0.1:8000/trivia", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // body: JSON.stringify({ })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Respuesta del backend:", data);
        // Mostrar la pregunta con el efecto de escritura
        typeText(questionBox, data["pregunta"], 25);
        // Mostrar las opciones de respuesta
        typeText(triviaButton1, data["opciones"][0], 25);
        typeText(triviaButton2, data["opciones"][1], 25);
        typeText(triviaButton3, data["opciones"][2], 25);
        typeText(triviaButton4, data["opciones"][3], 25);
    })
    .catch(error => console.error("Error al obtener la trivia:", error));
}

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
    // Selección de elementos
    const modal = document.getElementById("modal");
    const startButton = document.querySelector(".start-button");
    const closeButton = document.querySelector(".close-button");
    const userForm = document.getElementById("userForm");
    
        // Abrir el modal al hacer clic en el botón INICIAR
        startButton.addEventListener("click", () => {
        modal.style.display = "flex"; // Mostrar el modal
        });
    
        // Cerrar el modal al hacer clic en la "X"
        closeButton.addEventListener("click", () => {
        modal.style.display = "none"; // Ocultar el modal
        });
    
        // Cerrar el modal al hacer clic fuera del contenido del modal
        window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none"; // Ocultar el modal
        }
        });
    
        // Manejar el envío del formulario
        userForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Evitar el envío predeterminado
    
        // Obtener valores del formulario
        const name = document.getElementById("name").value;
        const age = document.getElementById("age").value;
    
        
        // Enviar los datos al backend
        enviarDatos(name, age);
    
        // Ocultar el modal
        modal.style.display = "none";
    
        // Scroll automático hacia el final de la página
        window.scrollTo({
            top: document.body.scrollHeight, // Posición final de la página
            behavior: "smooth", // Desplazamiento suave
        });
        });
    
});

document.addEventListener("DOMContentLoaded", () => {
    const qrReader = new Html5Qrcode("qr-reader");

    qrReader.start(
        { facingMode: "environment" }, // Usa la cámara trasera
        {
            fps: 1, // Velocidad de escaneo
            qrbox: { width: 250, height: 250 }, // Tamaño del área de escaneo
        },
        onScanSuccess, // Función para manejar un escaneo exitoso
        onScanFailure // Función para manejar errores en el escaneo
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
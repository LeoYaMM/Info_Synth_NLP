const questionBox = document.getElementById("question");
const triviaButton1 = document.getElementById("option1")
const triviaButton2 = document.getElementById("option2")
const triviaButton3 = document.getElementById("option3")
const triviaButton4 = document.getElementById("option4")

//Funcion para mostrar la trivia
function showTrivia(){
    const idVisitante = getCookie("id_visitante");
    if (!idVisitante) {
        console.error("ID del visitante no encontrado en las cookies");
        return;
    }

    fetch ("http://127.0.0.1:8000/trivia", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({id_visitante: idVisitante})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor: " + response.status);
        }
        return response.json();
    })
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

// Función para obtener la cookie por su id_visitante
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener("DOMContentLoaded", function() {
    // Mostrar la trivia al cargar la página
    showTrivia();
});
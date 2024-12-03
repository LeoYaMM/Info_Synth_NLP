// const questionBox = document.getElementById("question");
// const triviaButton1 = document.getElementById("option1")
// const triviaButton2 = document.getElementById("option2")
// const triviaButton3 = document.getElementById("option3")
// const triviaButton4 = document.getElementById("option4")
// const numeroResumenes = getCookie("scanCount");

// //Funcion para mostrar la trivia
// function showTrivia(scanCount) {
//     const idVisitante = getCookie("id_visitante");
//     if (!idVisitante) {
//         console.error("ID del visitante no encontrado en las cookies");
//         return;
//     }

//     fetch ("http://127.0.0.1:8000/trivia", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({id_visitante: idVisitante, noResumenes: scanCount})
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error("Error en la respuesta del servidor: " + response.status);
//         }
//         return response.json();
//     })
//     .then(data => {
//         console.log("Respuesta del backend:", data);
//         // Mostrar la pregunta con el efecto de escritura
//         typeText(questionBox, data["pregunta"], 25);
//         // Mostrar las opciones de respuesta
//         typeText(triviaButton1, data["opciones"][0], 25);
//         typeText(triviaButton2, data["opciones"][1], 25);
//         typeText(triviaButton3, data["opciones"][2], 25);
//         typeText(triviaButton4, data["opciones"][3], 25);
//     })
//     .catch(error => console.error("Error al obtener la trivia:", error));
// }

// // Función para simular el efecto de escritura en un elemento
// function typeText(element, text, delay = 25) {
//     element.textContent = "";
//     let index = 0;
//     function type() {
//         if (index < text.length) {
//             element.textContent += text[index];
//             index++;
//             setTimeout(type, delay);
//         }
//     }

//     type();
// }

// // Función para obtener la cookie por su id_visitante
// function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
// }

// // Esta función se ejecutará cuando el usuario seleccione una opción
// function selectOption(option) {
//     console.log("Seleccionaste la opción " + option);
//     // Aquí podrías enviar la respuesta seleccionada al servidor
// }

// document.addEventListener("DOMContentLoaded", () => {
//     // Mostrar la trivia al cargar la página
//     console.log("ScanCount=", numeroResumenes)
//     for (let index = 1; index <= numeroResumenes; index++) {
//         showTrivia(index);
//     }
    
// });

const questionBox = document.getElementById("question");
const triviaButton1 = document.getElementById("option1")
const triviaButton2 = document.getElementById("option2")
const triviaButton3 = document.getElementById("option3")
const triviaButton4 = document.getElementById("option4")
const numeroResumenes = getCookie("scanCount");
let currentQuestionIndex = 0; // Índice de la pregunta actual
let correctAnswers = 0; // Contador de respuestas correctas
let totalQuestions = 0; // Total de preguntas
let questions = []; // Array para almacenar las preguntas

// Función para cargar las preguntas desde el servidor
function loadQuestions() {
    const idVisitante = getCookie("id_visitante");
    if (!idVisitante) {
        console.error("ID del visitante no encontrado en las cookies");
        return;
    }

    fetch("http://127.0.0.1:8000/trivia", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_visitante: idVisitante, noResumen: numeroResumenes })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor: " + response.status);
        }
        return response.json();
    })
    .then(data => {
        questions = data.preguntas;
        totalQuestions = questions.length;
        showQuestion(); // Mostrar la primera pregunta
    })
    .catch(error => console.error("Error al obtener la trivia:", error));
}

// Función para mostrar una pregunta
function showQuestion() {
    if (currentQuestionIndex >= totalQuestions) {
        // Mostrar el resumen al final
        alert(`Has respondido correctamente ${correctAnswers} de ${totalQuestions} preguntas.`);
        return;
    }

    const currentQuestion = questions[currentQuestionIndex];
    questionBox.textContent = ""; // Limpiar la pregunta anterior
    typeText(questionBox, currentQuestion.pregunta, 25); // Mostrar la pregunta actual

    // Mostrar las opciones
    triviaButton1.textContent = currentQuestion.opciones[0];
    triviaButton2.textContent = currentQuestion.opciones[1];
    triviaButton3.textContent = currentQuestion.opciones[2];
    triviaButton4.textContent = currentQuestion.opciones[3];

    // Agregar manejadores de eventos para las opciones
    triviaButton1.onclick = () => handleAnswer(currentQuestion.opciones[0]);
    triviaButton2.onclick = () => handleAnswer(currentQuestion.opciones[1]);
    triviaButton3.onclick = () => handleAnswer(currentQuestion.opciones[2]);
    triviaButton4.onclick = () => handleAnswer(currentQuestion.opciones[3]);
}

// Función para manejar la respuesta del usuario
function handleAnswer(selectedOption) {
    const currentQuestion = questions[currentQuestionIndex];
    if (selectedOption === currentQuestion.respuesta) {
        correctAnswers++; // Incrementar contador si la respuesta es correcta
    }

    currentQuestionIndex++; // Pasar a la siguiente pregunta
    showQuestion(); // Mostrar la siguiente pregunta
}

// Función para obtener la cookie por su id_visitante
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
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
    loadQuestions(); // Cargar las preguntas al cargar la página
});

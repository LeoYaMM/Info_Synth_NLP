document.getElementById("loginForm").addEventListener("submit", function(event){
    event.preventDefault();
    const nombre = document.getElementById('first-name').value.trim();
    const edad = document.getElementById('age').value.trim();

    if (nombre && edad && edad > 0) {
        enviarDatos(nombre, edad);
    } else {
        alert("Por favor, completa todos los campos.");
    }
});

function enviarDatos(nombre, edad) {
    fetch("http://127.0.0.1:8000/registrar_visitante", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, edad })
    })
    .then(response => response.json())
    .then(data => {
        document.cookie = `id_visitante=${data.id_visitante}; path=/; SameSite=Lax`;
        window.location.href = "index.html"; // Redirige a index.html
    })
    .catch(error => console.error("Error al enviar datos:", error));
}
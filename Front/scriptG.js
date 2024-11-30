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
      const name = document.getElementById("name").value;
      const age = document.getElementById("age").value;
      alert(`¡Hola, ${name}! Has ingresado que tienes ${age} años.`);
  
      // Ocultar el modal
      modal.style.display = "none";
  
      // Scroll automático hacia el final de la página
      window.scrollTo({
        top: document.body.scrollHeight, // Posición final de la página
        behavior: "smooth", // Desplazamiento suave
      });
    });
  });
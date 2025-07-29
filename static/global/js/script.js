 // Toggle para mostrar/ocultar contraseña
 function togglePassword() {
    const passwordField = document.getElementById('id_password');
    const toggleIcon = document.getElementById('password-toggle');

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Validación en tiempo real
 document.addEventListener('DOMContentLoaded', function() {
     const form = document.querySelector('form');
     const usernameField = document.getElementById('id_username');
     const passwordField = document.getElementById('id_password');
     const submitButton = form.querySelector('button[type="submit"]');

     function validateForm() {
         const isValid = usernameField.value.trim() !== '' && passwordField.value.trim() !== '';

         if (isValid) {
             submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
             submitButton.disabled = false;
         } else {
             submitButton.classList.add('opacity-50', 'cursor-not-allowed');
             submitButton.disabled = true;
         }
     }

     usernameField.addEventListener('input', validateForm);
     passwordField.addEventListener('input', validateForm);

     // Validación inicial
     validateForm();

     // Efecto de loading en el botón al enviar
     form.addEventListener('submit', function() {
         submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Iniciando sesión...';
         submitButton.disabled = true;
     });
 });

// Animación de entrada
 window.addEventListener('load', function() {
     const elements = document.querySelectorAll('.fade-in, .slide-up');
     elements.forEach((el, index) => {
         setTimeout(() => {
             el.style.opacity = '1';
             el.style.transform = 'translateY(0)';
         }, index * 200);
     });
 });

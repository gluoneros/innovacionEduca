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

 // dashboard
 src="https://cdn.jsdelivr.net/npm/@tailwindplus/elements@1"//@tailwindplus/elements"
  // Variables globales
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const closeMobileMenu = document.getElementById('closeMobileMenu');
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
    const sidebar = document.getElementById('sidebar');
    const userRoleSelect = document.getElementById('userRole');
    const menuSections = document.querySelectorAll('.menu-section');

    // Función para abrir menú móvil
    function openMobileMenu() {
        sidebar.classList.remove('-translate-x-full');
        sidebar.classList.add('translate-x-0');
        mobileMenuOverlay.classList.remove('hidden');
        document.body.classList.add('overflow-hidden', 'lg:overflow-auto');
    }

    // Función para cerrar menú móvil
    function closeMobileMenuFunc() {
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('translate-x-0');
        mobileMenuOverlay.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
    }

    // Event listeners para menú móvil
    mobileMenuBtn.addEventListener('click', openMobileMenu);
    closeMobileMenu.addEventListener('click', closeMobileMenuFunc);
    mobileMenuOverlay.addEventListener('click', closeMobileMenuFunc);

    // Cerrar menú móvil cuando se hace clic en un enlace (solo en móvil)
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            if (window.innerWidth < 1024) {
                closeMobileMenuFunc();
            }
        });
    });

    // Cambio de rol de usuario
    userRoleSelect.addEventListener('change', function() {
        const selectedRole = this.value;

        // Ocultar todos los menús
        menuSections.forEach(section => {
            section.classList.add('hidden');
        });

        // Mostrar el menú correspondiente
        const targetMenu = document.getElementById(`menu-${selectedRole}`);
        if (targetMenu) {
            targetMenu.classList.remove('hidden');
        }

        // Cambiar el título del dashboard según el rol
        const dashboardTitle = document.querySelector('main h1');
        const dashboardSubtitle = document.querySelector('main p');

        switch(selectedRole) {
            case 'administrativo':
                dashboardTitle.textContent = 'Dashboard Administrativo';
                dashboardSubtitle.textContent = 'Bienvenido al panel de administración del colegio';
                break;
            case 'profesor':
                dashboardTitle.textContent = 'Dashboard Profesor';
                dashboardSubtitle.textContent = 'Gestiona tus cursos y estudiantes';
                break;
            case 'estudiante':
                dashboardTitle.textContent = 'Dashboard Estudiante';
                dashboardSubtitle.textContent = 'Consulta tus notas y horarios';
                break;
        }
    });

    // Animaciones y efectos interactivos
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            if (window.innerWidth >= 1024) {
                this.style.transform = 'translateX(5px)';
                this.style.transition = 'transform 0.3s ease';
            }
        });

        item.addEventListener('mouseleave', function() {
            if (window.innerWidth >= 1024) {
                this.style.transform = 'translateX(0)';
            }
        });
    });

    // Efecto de hover en las tarjetas de estadísticas
    document.querySelectorAll('[class*="stats-card"]').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
            this.style.transition = 'transform 0.3s ease';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Manejo del redimensionamiento de ventana
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 1024) {
            // En desktop, asegurar que el sidebar esté visible
            sidebar.classList.remove('-translate-x-full');
            sidebar.classList.add('translate-x-0');
            mobileMenuOverlay.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        } else {
            // En móvil, asegurar que el sidebar esté oculto inicialmente
            if (!mobileMenuOverlay.classList.contains('hidden')) {
                // Solo ocultar si no está abierto intencionalmente
                return;
            }
            sidebar.classList.add('-translate-x-full');
            sidebar.classList.remove('translate-x-0');
        }
    });

    // Mejorar accesibilidad - navegación por teclado
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeMobileMenuFunc();
        }
    });

    // Touch/swipe gestures para cerrar menú en móvil
    let touchStartX = 0;
    let touchEndX = 0;

    sidebar.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    });

    sidebar.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        if (touchEndX < touchStartX - 50) {
            // Swipe left to close
            if (window.innerWidth < 1024) {
                closeMobileMenuFunc();
            }
        }
    }

    // Inicialización
    document.addEventListener('DOMContentLoaded', function() {
        // Configurar estado inicial basado en el tamaño de pantalla
        if (window.innerWidth < 1024) {
            sidebar.classList.add('-translate-x-full');
            sidebar.classList.remove('translate-x-0');
        }
    });
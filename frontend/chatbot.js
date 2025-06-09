/**
 * Chatbot Frontend - Despacho Jurídico Virtual
 * Manejo de la interfaz de chat y comunicación con la API
 */

const API_BASE_URL = 'http://localhost:8000';

// Estado del chat
let chatState = {
    awaitingCita: false,
    currentSuggestions: []
};

/**
 * Enviar mensaje al chatbot
 */
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Mostrar mensaje del usuario
    addMessage(message, 'user');
    messageInput.value = '';
    
    // Mostrar indicador de escritura
    showTypingIndicator();
    
    try {
        // Enviar mensaje a la API
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mensaje: message,
                usuario_id: getUserId()
            })
        });
        
        if (!response.ok) {
            throw new Error('Error en la comunicación con el servidor');
        }
        
        const data = await response.json();
        
        // Ocultar indicador de escritura
        hideTypingIndicator();
        
        // Mostrar respuesta del bot
        addMessage(data.respuesta, 'bot');
        
        // Mostrar sugerencias
        if (data.sugerencias && data.sugerencias.length > 0) {
            showSuggestions(data.sugerencias);
        }
        
        // Si requiere cita, activar modo cita
        if (data.requiere_cita) {
            chatState.awaitingCita = true;
            setTimeout(() => {
                document.getElementById('citas').scrollIntoView({ behavior: 'smooth' });
            }, 1000);
        }
        
    } catch (error) {
        hideTypingIndicator();
        addMessage('Lo siento, ha ocurrido un error. Por favor, intenta nuevamente.', 'bot');
        console.error('Error:', error);
    }
}

/**
 * Agregar mensaje al chat
 */
function addMessage(message, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (sender === 'bot') {
        // Procesar markdown básico para el bot
        const processedMessage = processMarkdown(message);
        messageContent.innerHTML = `<strong>🤖 Asistente Legal</strong><br>${processedMessage}`;
    } else {
        messageContent.innerHTML = `<strong>👤 Tú</strong><br>${escapeHtml(message)}`;
    }
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // Scroll automático
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Procesar markdown básico
 */
function processMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

/**
 * Escapar HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Mostrar sugerencias
 */
function showSuggestions(suggestions) {
    const suggestionsContainer = document.getElementById('suggestions');
    if (!suggestionsContainer) return;
    
    suggestionsContainer.innerHTML = '';
    
    suggestions.forEach(suggestion => {
        const chip = document.createElement('span');
        chip.className = 'suggestion-chip';
        chip.textContent = suggestion;
        chip.onclick = () => {
            document.getElementById('messageInput').value = suggestion;
            sendMessage();
        };
        suggestionsContainer.appendChild(chip);
    });
}

/**
 * Mostrar/ocultar indicador de escritura
 */
function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.add('show');
    }
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.remove('show');
    }
}

/**
 * Obtener ID único del usuario
 */
function getUserId() {
    let userId = localStorage.getItem('user_id');
    if (!userId) {
        userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('user_id', userId);
    }
    return userId;
}

/**
 * Inicializar chat
 */
function initializeChat() {
    // Configurar fecha mínima para citas (mañana)
    const fechaInput = document.getElementById('fecha');
    if (fechaInput) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        fechaInput.min = tomorrow.toISOString().split('T')[0];
        
        // Fecha máxima: 3 meses después
        const maxDate = new Date();
        maxDate.setMonth(maxDate.getMonth() + 3);
        fechaInput.max = maxDate.toISOString().split('T')[0];
    }
}

// Funciones auxiliares para mensajes rápidos
function askAboutServices() {
    document.getElementById('messageInput').value = "¿Qué servicios legales ofrecen?";
    sendMessage();
}

function askAboutCosts() {
    document.getElementById('messageInput').value = "¿Cuáles son sus costos?";
    sendMessage();
}

function askAboutContact() {
    document.getElementById('messageInput').value = "¿Cuál es su información de contacto?";
    sendMessage();
}

function requestAppointment() {
    document.getElementById('messageInput').value = "Quiero agendar una cita";
    sendMessage();
}

/**
 * Scroll suave a secciones
 */
function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
    
    // Agregar smooth scrolling a los enlaces del navbar
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Función para manejar el evento de tecla Enter en el input del chat
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
}

// Función para mostrar el indicador de escritura
function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.add('show');
    }
}

// Función para ocultar el indicador de escritura
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.remove('show');
    }
}

// Función para mostrar sugerencias
function showSuggestions(suggestions) {
    const suggestionsContainer = document.getElementById('suggestions');
    if (!suggestionsContainer) return;
    
    suggestionsContainer.innerHTML = '';
    
    suggestions.forEach(suggestion => {
        const chip = document.createElement('span');
        chip.className = 'suggestion-chip';
        chip.textContent = suggestion;
        chip.onclick = () => {
            document.getElementById('messageInput').value = suggestion;
            sendMessage();
        };
        suggestionsContainer.appendChild(chip);
    });
}

// Función para procesar markdown básico
function processMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

// Función para escapar HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Función para obtener ID único del usuario
function getUserId() {
    let userId = localStorage.getItem('user_id');
    if (!userId) {
        userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('user_id', userId);
    }
    return userId;
}

// Función para inicializar el chat
function initializeChat() {
    // Establecer fecha mínima para citas (mañana)
    const fechaInput = document.getElementById('fecha');
    if (fechaInput) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        fechaInput.min = tomorrow.toISOString().split('T')[0];
        
        // Fecha máxima: 3 meses después
        const maxDate = new Date();
        maxDate.setMonth(maxDate.getMonth() + 3);
        fechaInput.max = maxDate.toISOString().split('T')[0];
    }
}

// Función para validar el formulario de cita
function validateCitaForm() {
    const form = document.getElementById('citaForm');
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Exponer funciones globalmente para uso en HTML
window.sendMessage = sendMessage;
window.handleKeyPress = handleKeyPress;
window.askAboutServices = askAboutServices;
window.askAboutCosts = askAboutCosts;
window.askAboutContact = askAboutContact;
window.requestAppointment = requestAppointment;
window.scrollToSection = scrollToSection;

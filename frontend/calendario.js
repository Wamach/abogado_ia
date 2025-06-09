/**
 * Sistema de Gestión de Citas - Despacho Jurídico Virtual
 * Manejo del formulario de citas y disponibilidad de horarios
 */

const CITAS_API_URL = 'http://localhost:8000';

/**
 * Inicializar sistema de citas
 */
function initializeCitas() {
    const citaForm = document.getElementById('citaForm');
    const fechaInput = document.getElementById('fecha');
    const horaSelect = document.getElementById('hora');
    
    if (citaForm) {
        citaForm.addEventListener('submit', handleCitaSubmit);
    }
    
    if (fechaInput) {
        fechaInput.addEventListener('change', loadAvailableHours);
        
        // Configurar fecha mínima (mañana)
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        fechaInput.min = tomorrow.toISOString().split('T')[0];
        
        // Configurar fecha máxima (3 meses adelante)
        const maxDate = new Date();
        maxDate.setMonth(maxDate.getMonth() + 3);
        fechaInput.max = maxDate.toISOString().split('T')[0];
    }
}

/**
 * Cargar horarios disponibles para una fecha
 */
async function loadAvailableHours() {
    const fechaInput = document.getElementById('fecha');
    const horaSelect = document.getElementById('hora');
    const fecha = fechaInput.value;
    
    if (!fecha) return;
    
    // Limpiar opciones actuales
    horaSelect.innerHTML = '<option value="">Cargando horarios...</option>';
    horaSelect.disabled = true;
    
    try {
        const response = await fetch(`${CITAS_API_URL}/horarios_disponibles/${fecha}`);
        
        if (!response.ok) {
            throw new Error('Error obteniendo horarios disponibles');
        }
        
        const data = await response.json();
        
        // Limpiar y llenar opciones
        horaSelect.innerHTML = '<option value="">Seleccione una hora</option>';
        
        if (data.horarios_disponibles.length === 0) {
            horaSelect.innerHTML = '<option value="">No hay horarios disponibles</option>';
            showAlert('No hay horarios disponibles para esta fecha. Por favor seleccione otra fecha.', 'warning');
        } else {
            data.horarios_disponibles.forEach(hora => {
                const option = document.createElement('option');
                option.value = hora;
                option.textContent = formatTime(hora);
                horaSelect.appendChild(option);
            });
        }
        
        horaSelect.disabled = false;
        
    } catch (error) {
        console.error('Error cargando horarios:', error);
        horaSelect.innerHTML = '<option value="">Error cargando horarios</option>';
        showAlert('Error cargando horarios disponibles. Por favor intente nuevamente.', 'error');
    }
}

/**
 * Manejar envío del formulario de cita
 */
async function handleCitaSubmit(event) {
    event.preventDefault();
    
    const loadingBtn = document.getElementById('loadingCita');
    const submitBtn = event.target.querySelector('button[type="submit"]');
    
    // Mostrar loading
    loadingBtn.classList.add('show');
    submitBtn.disabled = true;
    
    try {
        // Recopilar datos del formulario
        const formData = {
            nombre: document.getElementById('nombre').value.trim(),
            email: document.getElementById('email').value.trim(),
            telefono: document.getElementById('telefono').value.trim(),
            fecha: `${document.getElementById('fecha').value} ${document.getElementById('hora').value}`,
            tipo_servicio: document.getElementById('tipoServicio').value,
            descripcion: document.getElementById('descripcion').value.trim()
        };
        
        // Validar datos
        if (!validateCitaData(formData)) {
            return;
        }
        
        // Enviar solicitud
        const response = await fetch(`${CITAS_API_URL}/agendar_cita`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || 'Error agendando la cita');
        }
        
        // Éxito
        showAlert(
            `¡Cita agendada exitosamente! 
            ID de cita: ${result.cita_id}
            Fecha: ${formatDateTime(result.detalles.fecha)}
            Servicio: ${getServiceName(result.detalles.servicio)}
            
            Recibirá un email de confirmación en breve.`,
            'success'
        );
        
        // Limpiar formulario
        event.target.reset();
        document.getElementById('hora').innerHTML = '<option value="">Seleccione una hora</option>';
        
        // Enviar mensaje al chat confirmando la cita
        if (window.addMessage) {
            addMessage(
                `Perfecto! Tu cita ha sido agendada para el ${formatDateTime(result.detalles.fecha)} para ${getServiceName(result.detalles.servicio)}. ID de cita: ${result.cita_id}`,
                'bot'
            );
        }
        
    } catch (error) {
        console.error('Error agendando cita:', error);
        showAlert(error.message || 'Error agendando la cita. Por favor intente nuevamente.', 'error');
    } finally {
        // Ocultar loading
        loadingBtn.classList.remove('show');
        submitBtn.disabled = false;
    }
}

/**
 * Función para formatear tiempo en formato 12 horas
 */
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const period = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
    return `${displayHour}:${minutes} ${period}`;
}

/**
 * Función para mostrar alertas
 */
function showAlert(message, type = 'info') {
    // Remover alertas existentes
    const existingAlerts = document.querySelectorAll('.dynamic-alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Crear nueva alerta
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} dynamic-alert`;
    alertDiv.innerHTML = `
        <i class="fas fa-${getAlertIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" aria-label="Close" onclick="this.parentElement.remove()"></button>
    `;
    
    // Insertar después del título de la sección de citas
    const citasSection = document.getElementById('citas');
    const sectionTitle = citasSection.querySelector('.section-title');
    if (sectionTitle) {
        sectionTitle.insertAdjacentElement('afterend', alertDiv);
    }
    
    // Auto-remover después de 10 segundos
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.remove();
        }
    }, 10000);
    
    // Scroll a la alerta
    alertDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Obtener icono para alerta según el tipo
 */
function getAlertIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'error':
        case 'danger': return 'exclamation-triangle';
        case 'warning': return 'exclamation-circle';
        case 'info':
        default: return 'info-circle';
    }
}

/**
 * Validar datos del formulario de cita
 */
function validateCitaData(data) {
    const errors = [];
    
    if (!data.nombre || data.nombre.length < 2) {
        errors.push('El nombre debe tener al menos 2 caracteres');
    }
    
    if (!data.email || !isValidEmail(data.email)) {
        errors.push('Debe proporcionar un email válido');
    }
    
    if (!data.telefono || data.telefono.length < 10) {
        errors.push('Debe proporcionar un teléfono válido');
    }
    
    if (!data.fecha) {
        errors.push('Debe seleccionar una fecha y hora');
    }
    
    if (!data.tipo_servicio) {
        errors.push('Debe seleccionar un tipo de servicio');
    }
    
    if (errors.length > 0) {
        showAlert('Por favor corrija los siguientes errores:\n• ' + errors.join('\n• '), 'error');
        return false;
    }
    
    return true;
}

/**
 * Validar formato de email
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Formatear fecha y hora para mostrar
 */
function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit',
        timeZone: 'America/Mexico_City'
    };
    return date.toLocaleDateString('es-MX', options);
}

/**
 * Obtener nombre del servicio por valor
 */
function getServiceName(serviceValue) {
    const serviceNames = {
        'civil': 'Derecho Civil',
        'penal': 'Derecho Penal',
        'laboral': 'Derecho Laboral',
        'familiar': 'Derecho Familiar',
        'mercantil': 'Derecho Mercantil',
        'inmobiliario': 'Derecho Inmobiliario',
        'accidentes': 'Accidentes Viales',
        'urgente': 'Caso Urgente (24h)'
    };
    return serviceNames[serviceValue] || serviceValue;
}

/**
 * Función para manejar errores de red
 */
function handleNetworkError(error) {
    console.error('Error de red:', error);
    
    if (error.message.includes('Failed to fetch')) {
        showAlert(
            'No se puede conectar con el servidor. Por favor verifique su conexión a internet y que el servidor esté ejecutándose.',
            'error'
        );
    } else {
        showAlert('Ha ocurrido un error inesperado. Por favor intente nuevamente.', 'error');
    }
}

/**
 * Función para actualizar estado del formulario
 */
function updateFormState(isLoading = false) {
    const form = document.getElementById('citaForm');
    const submitBtn = form.querySelector('button[type="submit"]');
    const loadingIcon = document.getElementById('loadingCita');
    
    if (isLoading) {
        submitBtn.disabled = true;
        loadingIcon.classList.add('show');
        form.style.opacity = '0.7';
    } else {
        submitBtn.disabled = false;
        loadingIcon.classList.remove('show');
        form.style.opacity = '1';
    }
}

// Export para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeCitas,
        loadAvailableHours,
        validateCitaData,
        formatDateTime,
        getServiceName
    };
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeCitas();
    
    // Agregar funciones globales para uso desde el chat
    window.preSelectServiceFromChat = preSelectServiceFromChat;
    window.populateFormFromChat = populateFormFromChat;
    window.loadAvailableHours = loadAvailableHours;
});

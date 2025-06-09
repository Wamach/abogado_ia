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
 * Validar datos de la cita
 */
function validateCitaData(data) {
    const errors = [];
    
    if (!data.nombre || data.nombre.length < 2) {
        errors.push('El nombre debe tener al menos 2 caracteres');
    }
    
    if (!data.email || !isValidEmail(data.email)) {
        errors.push('Debe proporcionar un email válido');
    }
    
    if (!data.telefono || data.telefono.length < 7) {
        errors.push('Debe proporcionar un teléfono válido');
    }
    
    if (!data.fecha || !data.fecha.includes(' ')) {
        errors.push('Debe seleccionar fecha y hora');
    }
    
    if (!data.tipo_servicio) {
        errors.push('Debe seleccionar el tipo de servicio');
    }
    
    // Validar que la fecha sea futura
    const citaDate = new Date(data.fecha);
    const now = new Date();
    if (citaDate <= now) {
        errors.push('La fecha de la cita debe ser futura');
    }
    
    if (errors.length > 0) {
        showAlert('Por favor corrija los siguientes errores:\n• ' + errors.join('\n• '), 'error');
        return false;
    }
    
    return true;
}

/**
 * Validar email
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Formatear hora para mostrar
 */
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour24 = parseInt(hours);
    const ampm = hour24 >= 12 ? 'PM' : 'AM';
    const hour12 = hour24 % 12 || 12;
    return `${hour12}:${minutes} ${ampm}`;
}

/**
 * Formatear fecha y hora completa
 */
function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    };
    return date.toLocaleDateString('es-ES', options);
}

/**
 * Obtener nombre del servicio
 */
function getServiceName(serviceCode) {
    const services = {
        'civil': 'Derecho Civil',
        'penal': 'Derecho Penal',
        'laboral': 'Derecho Laboral',
        'familia': 'Derecho de Familia'
    };
    return services[serviceCode] || serviceCode;
}

/**
 * Mostrar alertas/notificaciones
 */
function showAlert(message, type = 'info') {
    // Crear elemento de alerta
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'warning'} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 1050; max-width: 400px;';
    
    // Icono según tipo
    const iconClass = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle';
    
    alertDiv.innerHTML = `
        <i class="fas fa-${iconClass} me-2"></i>
        <span>${message.replace(/\n/g, '<br>')}</span>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remover después de 5 segundos
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

/**
 * Cargar citas existentes (para admin)
 */
async function loadCitas() {
    try {
        const response = await fetch(`${CITAS_API_URL}/citas`);
        
        if (!response.ok) {
            throw new Error('Error cargando citas');
        }
        
        const data = await response.json();
        return data.citas;
        
    } catch (error) {
        console.error('Error cargando citas:', error);
        return [];
    }
}

/**
 * Funciones de utilidad para integración con chat
 */
function preSelectServiceFromChat(serviceType) {
    const serviceSelect = document.getElementById('tipoServicio');
    if (serviceSelect) {
        serviceSelect.value = serviceType;
    }
    
    // Scroll a la sección de citas
    document.getElementById('citas').scrollIntoView({ behavior: 'smooth' });
}

function populateFormFromChat(data) {
    if (data.nombre) document.getElementById('nombre').value = data.nombre;
    if (data.email) document.getElementById('email').value = data.email;
    if (data.telefono) document.getElementById('telefono').value = data.telefono;
    if (data.tipo_servicio) document.getElementById('tipoServicio').value = data.tipo_servicio;
    if (data.descripcion) document.getElementById('descripcion').value = data.descripcion;
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeCitas();
    
    // Agregar funciones globales para uso desde el chat
    window.preSelectServiceFromChat = preSelectServiceFromChat;
    window.populateFormFromChat = populateFormFromChat;
    window.loadAvailableHours = loadAvailableHours;
});

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

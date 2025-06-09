/**
 * Sistema de Predicción de Sentencias - JavaScript
 * Maneja la interfaz y comunicación con la API de predicción
 */

class PredictionSystem {
    constructor() {
        this.apiUrl = 'http://localhost:8003';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadCaseTypes();
    }

    setupEventListeners() {
        const form = document.getElementById('predictionForm');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.analyzeCaseDebounced();
        });

        // Actualizar jurisdicción automáticamente
        document.getElementById('tipoCaso').addEventListener('change', (e) => {
            document.getElementById('jurisdiccion').value = e.target.value;
        });
    }

    // Debounce para evitar múltiples requests
    analyzeCaseDebounced = this.debounce(() => {
        this.analyzeCase();
    }, 500);

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    async loadCaseTypes() {
        try {
            const response = await fetch(`${this.apiUrl}/case_types`);
            if (response.ok) {
                const data = await response.json();
                console.log('Tipos de casos cargados:', data);
            }
        } catch (error) {
            console.error('Error cargando tipos de casos:', error);
        }
    }

    getSelectedEvidences() {
        const evidences = [];
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        
        checkboxes.forEach(checkbox => {
            evidences.push(checkbox.value);
        });
        
        return evidences;
    }

    async analyzeCase() {
        try {
            this.showLoading(true);
            
            // Recopilar datos del formulario
            const caseData = {
                tipo_caso: document.getElementById('tipoCaso').value,
                descripcion: document.getElementById('descripcion').value,
                monto_disputa: parseFloat(document.getElementById('montoDisputa').value) || 0,
                complejidad: document.getElementById('complejidad').value,
                evidencias: this.getSelectedEvidences(),
                antecedentes: document.getElementById('antecedentes').value,
                jurisdiccion: document.getElementById('jurisdiccion').value
            };

            // Validar datos
            if (!this.validateCaseData(caseData)) {
                this.showError('Por favor, completa todos los campos requeridos.');
                return;
            }

            // Enviar a la API
            const response = await fetch(`${this.apiUrl}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(caseData)
            });

            if (!response.ok) {
                throw new Error(`Error en la predicción: ${response.statusText}`);
            }

            const prediction = await response.json();
            this.displayResults(prediction);

        } catch (error) {
            console.error('Error en predicción:', error);
            this.showError('Error al analizar el caso. Por favor, intenta nuevamente.');
        } finally {
            this.showLoading(false);
        }
    }

    validateCaseData(caseData) {
        if (!caseData.tipo_caso || !caseData.descripcion) {
            return false;
        }
        if (caseData.descripcion.length < 10) {
            this.showError('La descripción debe tener al menos 10 caracteres.');
            return false;
        }
        return true;
    }

    displayResults(prediction) {
        // Mostrar sección de resultados
        const resultSection = document.getElementById('resultSection');
        resultSection.style.display = 'block';

        // Actualizar probabilidad
        const probabilityValue = Math.round(prediction.probabilidad_exito * 100);
        document.getElementById('probabilityValue').textContent = `${probabilityValue}%`;
        
        // Colorear círculo según probabilidad
        const circle = document.getElementById('probabilityCircle');
        circle.className = 'probability-circle';
        
        if (probabilityValue >= 70) {
            circle.classList.add('probability-high');
        } else if (probabilityValue >= 40) {
            circle.classList.add('probability-medium');
        } else {
            circle.classList.add('probability-low');
        }

        // Tipo de sentencia
        document.getElementById('sentenceType').textContent = prediction.tipo_sentencia_probable;

        // Tiempo estimado
        document.getElementById('estimatedTime').textContent = prediction.tiempo_estimado_meses;

        // Confianza
        const confidence = Math.round(prediction.confianza_prediccion * 100);
        document.getElementById('confidenceLevel').textContent = `${confidence}%`;

        // Factores de riesgo
        this.displayList('riskFactors', prediction.factores_riesgo, 'risk-factor');

        // Recomendaciones
        this.displayList('recommendations', prediction.recomendaciones, 'recommendation');

        // Scroll hacia resultados
        resultSection.scrollIntoView({ behavior: 'smooth' });

        // Animación de entrada
        this.animateResults();
    }

    displayList(containerId, items, className) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';

        if (items.length === 0) {
            container.innerHTML = '<p class="text-muted">No hay elementos para mostrar.</p>';
            return;
        }

        items.forEach(item => {
            const div = document.createElement('div');
            div.className = className;
            div.innerHTML = `<i class="fas fa-info-circle"></i> ${item}`;
            container.appendChild(div);
        });
    }

    animateResults() {
        const resultSection = document.getElementById('resultSection');
        resultSection.style.opacity = '0';
        resultSection.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            resultSection.style.transition = 'all 0.5s ease';
            resultSection.style.opacity = '1';
            resultSection.style.transform = 'translateY(0)';
        }, 100);
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        const form = document.getElementById('predictionForm');
        const resultSection = document.getElementById('resultSection');
        
        if (show) {
            spinner.style.display = 'block';
            form.style.opacity = '0.5';
            resultSection.style.display = 'none';
        } else {
            spinner.style.display = 'none';
            form.style.opacity = '1';
        }
    }

    showError(message) {
        // Crear toast de error
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-danger border-0';
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-exclamation-circle"></i> ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        // Contenedor de toasts
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }

        toastContainer.appendChild(toast);

        // Mostrar toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        // Remover del DOM después de ocultarse
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    // Métodos utilitarios para estadísticas
    async loadStats() {
        try {
            const response = await fetch(`${this.apiUrl}/predictions/stats`);
            if (response.ok) {
                const stats = await response.json();
                console.log('Estadísticas de predicciones:', stats);
                return stats;
            }
        } catch (error) {
            console.error('Error cargando estadísticas:', error);
        }
        return null;
    }

    async loadHistory() {
        try {
            const response = await fetch(`${this.apiUrl}/predictions/history?limit=10`);
            if (response.ok) {
                const history = await response.json();
                console.log('Historial de predicciones:', history);
                return history;
            }
        } catch (error) {
            console.error('Error cargando historial:', error);
        }
        return null;
    }
}

// Inicializar sistema cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    window.predictionSystem = new PredictionSystem();
    
    // Verificar conectividad con la API
    checkApiConnection();
});

async function checkApiConnection() {
    try {
        const response = await fetch('http://localhost:8003/health');
        if (response.ok) {
            console.log('✅ Conexión con API de predicción establecida');
        } else {
            console.warn('⚠️ API de predicción no responde correctamente');
        }
    } catch (error) {
        console.error('❌ Error conectando con API de predicción:', error);
        window.predictionSystem.showError(
            'No se puede conectar con el servidor de predicción. Asegúrate de que esté ejecutándose en el puerto 8003.'
        );
    }
}

// Función para exportar resultados (bonus)
function exportResults() {
    const resultSection = document.getElementById('resultSection');
    if (resultSection.style.display === 'none') {
        window.predictionSystem.showError('No hay resultados para exportar');
        return;
    }

    // Crear contenido para exportar
    const exportData = {
        fecha: new Date().toLocaleString('es-ES'),
        probabilidad_exito: document.getElementById('probabilityValue').textContent,
        tipo_sentencia: document.getElementById('sentenceType').textContent,
        tiempo_estimado: document.getElementById('estimatedTime').textContent + ' meses',
        confianza: document.getElementById('confidenceLevel').textContent
    };

    // Descargar como JSON
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `prediccion_${Date.now()}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
}

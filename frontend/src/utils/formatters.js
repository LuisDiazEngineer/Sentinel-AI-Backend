// src/utils/formatters.js

// 1. Formatear fechas de ISO a algo humano
export const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
};

// 2. Dar color/clase según la severidad
export const getSeverityStyle = (level) => {
    switch (level?.toLowerCase()) {
        case 'critical': return 'bg-red-600 text-white font-bold';
        case 'high': return 'bg-orange-500 text-white';
        case 'medium': return 'bg-yellow-400 text-black';
        default: return 'bg-blue-500 text-white';
    }
};
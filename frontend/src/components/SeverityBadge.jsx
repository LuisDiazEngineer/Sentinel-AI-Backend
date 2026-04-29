// src/components/SeverityBadge.jsx
import React from 'react';

/**
 * COMPONENTE SeverityBadge
 * Propósito: Categorizar visualmente la gravedad de una amenaza mediante análisis de texto.
 * Relación: Es el puente visual entre el lenguaje natural de la IA y la interfaz de usuario (UI).
 */
const SeverityBadge = ({ analysis }) => {

    // 1. Lógica de Categorización (Parsing)
    // Relación: Analiza el campo 'ai_analysis' que viene de tu base de datos de FastAPI.
    const getSeverity = () => {
        // Normalizamos el texto a minúsculas para que la búsqueda sea robusta
        const text = analysis?.toLowerCase() || "";

        // Búsqueda de palabras clave (Keywords)
        // Relación: Si la IA de Google usó palabras de alta alerta, el badge reacciona.
        if (text.includes("alto") || text.includes("high") || text.includes("crítico")) {
            return { label: "ALTO", color: "bg-red-900 text-red-200 border-red-500" };
        }

        if (text.includes("medio") || text.includes("medium")) {
            return { label: "MEDIO", color: "bg-yellow-900 text-yellow-200 border-yellow-500" };
        }

        // Caso por defecto: Si no detecta peligro inminente, lo marca como Bajo.
        return { label: "BAJO", color: "bg-blue-900 text-blue-200 border-blue-500" };
    };

    const { label, color } = getSeverity();

    return (
        // 2. Renderizado con Tailwind CSS
        // Relación: Usa clases dinámicas `${color}` para cambiar el estilo sin duplicar código.
        <span className={`px-2 py-1 rounded text-xs font-bold border ${color}`}>
            {label}
        </span>
    );
};

export default SeverityBadge;
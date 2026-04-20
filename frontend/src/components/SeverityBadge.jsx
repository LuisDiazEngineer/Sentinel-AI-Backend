// src/components/SeverityBadge.jsx
import React from 'react';

const SeverityBadge = ({ analysis }) => {
    // Lógica para determinar el color basado en lo que diga la IA
    const getSeverity = () => {
        const text = analysis?.toLowerCase() || "";
        if (text.includes("alto") || text.includes("high") || text.includes("crítico")) {
            return { label: "ALTO", color: "bg-red-900 text-red-200 border-red-500" };
        }
        if (text.includes("medio") || text.includes("medium")) {
            return { label: "MEDIO", color: "bg-yellow-900 text-yellow-200 border-yellow-500" };
        }
        return { label: "BAJO", color: "bg-blue-900 text-blue-200 border-blue-500" };
    };

    const { label, color } = getSeverity();

    return (
        <span className={`px-2 py-1 rounded text-xs font-bold border ${color}`}>
            {label}
        </span>
    );
};

export default SeverityBadge;
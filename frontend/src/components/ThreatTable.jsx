// src/components/ThreatTable.jsx
import React from 'react';
import SeverityBadge from './SeverityBadge';

/**
 * COMPONENTE ThreatTable
 * Propósito: Listar de forma tabular y cronológica los incidentes de seguridad.
 * Relación: Consume el array 'threats' que FastAPI envía tras consultar PostgreSQL.
 */
const ThreatTable = ({ threats }) => {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
            {/* Cabecera de la tabla */}
            <div className="p-4 border-b border-slate-800 bg-slate-900/50">
                <h2 className="text-lg font-bold text-white">Últimas Amenazas Detectadas</h2>
            </div>

            {/* Contenedor con scroll horizontal para dispositivos móviles */}
            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        {/* 1. Encabezados de Columna */}
                        {/* Relación: Coinciden con los campos definidos en tu modelo ThreatLog de SQLAlchemy. */}
                        <tr className="text-slate-400 text-xs uppercase bg-slate-950">
                            <th className="p-4 font-medium">Timestamp</th>
                            <th className="p-4 font-medium">IP de Origen</th>
                            <th className="p-4 font-medium">Descripción</th>
                            <th className="p-4 font-medium">Nivel</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {/* 2. Mapeo dinámico de datos */}
                        {threats.map((t, i) => (
                            <tr key={i} className="hover:bg-slate-800/30 transition-colors">
                                {/* Formateo de fecha: Convierte el ISO del backend a hora local legible. */}
                                <td className="p-4 text-xs text-slate-500 font-mono">
                                    {new Date(t.timestamp).toLocaleTimeString()}
                                </td>

                                {/* IP Address: Destacada en verde neón para legibilidad rápida. */}
                                <td className="p-4 text-sm font-bold text-green-400 font-mono">
                                    {t.ip_address}
                                </td>

                                <td className="p-4 text-sm text-slate-300">
                                    {t.description}
                                </td>

                                {/* 3. Integración de Componentes */}
                                {/* Relación: Envía el análisis de la IA al SeverityBadge para determinar el color. */}
                                <td className="p-4">
                                    <SeverityBadge analysis={t.ai_analysis} />
                                </td>
                            </tr>
                        ))}

                        {/* 4. Estado Vacío (Empty State) */}
                        {/* Relación: Se muestra mientras el simulador no ha enviado datos o la DB está vacía. */}
                        {threats.length === 0 && (
                            <tr>
                                <td colSpan="4" className="p-10 text-center text-slate-600 italic">
                                    Esperando señales del Sentinel...
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ThreatTable;
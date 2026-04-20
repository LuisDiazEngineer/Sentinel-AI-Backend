// src/components/ThreatTable.jsx
import React from 'react';
import SeverityBadge from './SeverityBadge';

const ThreatTable = ({ threats }) => {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
            <div className="p-4 border-b border-slate-800 bg-slate-900/50">
                <h2 className="text-lg font-bold text-white">Últimas Amenazas Detectadas</h2>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="text-slate-400 text-xs uppercase bg-slate-950">
                            <th className="p-4 font-medium">Timestamp</th>
                            <th className="p-4 font-medium">IP de Origen</th>
                            <th className="p-4 font-medium">Descripción</th>
                            <th className="p-4 font-medium">Nivel</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {threats.map((t, i) => (
                            <tr key={i} className="hover:bg-slate-800/30 transition-colors">
                                <td className="p-4 text-xs text-slate-500 font-mono">
                                    {new Date(t.timestamp).toLocaleTimeString()}
                                </td>
                                <td className="p-4 text-sm font-bold text-green-400 font-mono">
                                    {t.ip_address}
                                </td>
                                <td className="p-4 text-sm text-slate-300">
                                    {t.description}
                                </td>
                                <td className="p-4">
                                    <SeverityBadge analysis={t.analysis} />
                                </td>
                            </tr>
                        ))}
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
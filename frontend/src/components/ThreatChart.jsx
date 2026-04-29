// src/components/ThreatChart.jsx
import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

/**
 * COMPONENTE ThreatChart
 * Propósito: Visualizar la línea de tiempo de los ataques detectados.
 * Relación: Transforma el historial de la base de datos en una serie de tiempo visual.
 */
const ThreatChart = ({ data }) => {
    return (
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl h-80 shadow-lg">
            <h3 className="text-slate-400 text-sm font-medium mb-4">
                Frecuencia de Ataques (Tiempo Real)
            </h3>

            {/* 1. Contenedor Responsivo */}
            {/* Relación: Permite que la gráfica se ajuste automáticamente al tamaño de la pantalla. */}
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data}>
                    {/* 2. Definición de Gradientes */}
                    {/* Relación: Crea ese efecto visual "Cyber" con un degradado verde neón. */}
                    <defs>
                        <linearGradient id="colorThreat" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                        </linearGradient>
                    </defs>

                    {/* 3. Rejilla y Ejes */}
                    {/* Relación: El eje X usa 'time', que viene del 'timestamp' de PostgreSQL procesado por el front. */}
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                    <XAxis
                        dataKey="time"
                        stroke="#64748b"
                        fontSize={10}
                        tickLine={false}
                        axisLine={false}
                    />
                    <YAxis
                        stroke="#64748b"
                        fontSize={10}
                        tickLine={false}
                        axisLine={false}
                    />

                    {/* 4. Tooltip Personalizado */}
                    {/* Relación: Muestra el valor exacto cuando el usuario pasa el mouse sobre un pico de actividad. */}
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#0f172a',
                            border: '1px solid #1e293b',
                            borderRadius: '8px'
                        }}
                        itemStyle={{ color: '#10b981' }}
                    />

                    {/* 5. La Línea de Datos (Área) */}
                    {/* Relación: 'amount' representa el número de incidentes en ese bloque de tiempo. */}
                    <Area
                        type="monotone"
                        dataKey="amount"
                        stroke="#10b981"
                        fillOpacity={1}
                        fill="url(#colorThreat)"
                        strokeWidth={3}
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ThreatChart;
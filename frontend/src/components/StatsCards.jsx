// src/components/StatsCards.jsx
import React from 'react';
import { ShieldAlert, Globe, Activity } from 'lucide-react';

const StatsCards = ({ totalThreats }) => {
    const stats = [
        { title: "Total Amenazas", value: totalThreats, icon: <ShieldAlert className="text-red-500" />, label: "Detectadas" },
        { title: "Sistemas Activos", value: "OK", icon: <Activity className="text-green-500" />, label: "Sentinel Core" },
        { title: "Región", value: "Austin, TX", icon: <Globe className="text-blue-500" />, label: "Target DC" },
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            {stats.map((s, i) => (
                <div key={i} className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-lg">
                    <div className="flex justify-between items-start mb-2">
                        <span className="text-slate-400 text-sm font-medium">{s.title}</span>
                        {s.icon}
                    </div>
                    <div className="text-2xl font-bold text-white">{s.value}</div>
                    <div className="text-xs text-slate-500 mt-1">{s.label}</div>
                </div>
            ))}
        </div>
    );
};

export default StatsCards;
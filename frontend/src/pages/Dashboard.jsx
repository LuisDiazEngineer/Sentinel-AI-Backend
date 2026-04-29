import React, { useState, useEffect } from 'react';
import { Activity, Server, ShieldAlert, Globe } from "lucide-react";
import AttackMap from '../components/AttackMap';
import LoginScreen from './LoginScreen';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

function Dashboard() {
  const { token, isAuthenticated, logout } = useAuth();

  // ESTADOS
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const [threats, setThreats] = useState([]);
  const [stats, setStats] = useState({ total: 0, critical: 0, avgRisk: 0 });
  const [isLockdown, setIsLockdown] = useState(false);


  // HELPERS
  const getLevel = (text) => {
    if (!text) return 'Low';
    const lowText = text.toLowerCase();
    if (lowText.includes('critical') || lowText.includes('sql') || lowText.includes('ddos')) return 'Critical';
    if (lowText.includes('high') || lowText.includes('brute force')) return 'High';
    return 'Low';
  };

  const getStatusStyles = (status) => {
    switch (status) {
      case 'TERMINATED': return 'bg-red-900/30 text-red-400 border border-red-500/50 px-2 py-1 rounded-full text-[9px] font-black animate-pulse flex items-center gap-1 justify-center';
      case 'QUARANTINED': return 'bg-yellow-900/30 text-yellow-400 border border-yellow-500/50 px-2 py-1 rounded-full text-[9px] flex items-center gap-1 justify-center';
      default: return 'bg-blue-900/20 text-blue-300 border border-blue-500/20 px-2 py-1 rounded-full text-[9px] flex items-center gap-1 justify-center';
    }
  };

  // API FETCH
  const fetchThreats = async () => {
    try {
      const response = await api.get('/threats/');
      const data = response.data || [];
      setThreats(data);

      const criticalCount = data.filter(t => getLevel(t.ai_analysis || t.description) === 'Critical').length;
      setStats({
        total: data.length,
        critical: criticalCount,
        avgRisk: data.length > 0 ? Math.round(data.reduce((acc, curr) => acc + (curr.risk_score || 0), 0) / data.length) : 0
      });
    } catch (error) {
      console.error("Error en Sentinel Node:", error);
      if (error.response?.status === 401) logout();
    }
  };

  const handleLockdown = async () => {
    try {
      const response = await api.post('/system/lockdown');
      setIsLockdown(response.data.lockdown);
    } catch (error) { console.error("Lockdown error:", error); }
  };

  // CICLO DE VIDA
  useEffect(() => {
    if (isAuthenticated !== null && isAuthenticated !== undefined) {
      setIsInitialLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (isAuthenticated && token) {
      fetchThreats();
      const interval = setInterval(fetchThreats, 35000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated, token]);

  // --- LOS GUARDIANES ---
  if (isInitialLoading) {
    return <div className="bg-black min-h-screen flex items-center justify-center text-blue-500 font-mono">INITIALIZING SENTINEL AI...</div>;
  }

  if (!isAuthenticated) {
    return <LoginScreen onLoginSuccess={() => window.location.reload()} />;
  }
  return (
    <div className={`min-h-screen transition-colors duration-1000 ${isLockdown ? 'bg-red-950/20' : 'bg-black'} text-slate-200 p-6 font-sans`}>

      {/* 1. HEADER: Branding & Identidad */}
      <header className="mb-8 flex justify-between items-center border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-2xl font-black tracking-tighter text-blue-500">
            SENTINEL <span className="text-white">AI</span>
          </h1>
          <p className="text-[10px] text-slate-500 font-mono uppercase tracking-widest">
            V1.0.4 - AUSTIN NODE READY // ENGINE: GEMINI-2.5-FLASH
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right hidden md:block">
            <p className="text-[9px] text-slate-500 uppercase tracking-tighter font-mono">System Status</p>
            <p className="text-[10px] font-bold text-emerald-500 font-mono">ENCRYPTED LINK ACTIVE</p>
          </div>
          <button onClick={logout} className="text-[10px] bg-slate-800 hover:bg-red-600/20 px-3 py-1.5 rounded-lg border border-slate-700 font-bold transition-all font-mono">
            LOGOUT
          </button>
        </div>
      </header>

      {/* 2. PANEL SUPERIOR: KPIs y Mapa */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-3xl shadow-xl backdrop-blur-sm">
          <p className="text-[10px] font-bold text-slate-500 uppercase mb-2 tracking-[0.2em] font-mono">Global Threat Level</p>
          <h2 className={`text-6xl font-black font-mono ${stats.avgRisk > 70 ? 'text-red-600' : 'text-blue-500'}`}>
            {stats.avgRisk}%
          </h2>
          <div className="w-full bg-slate-800 h-1.5 mt-6 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-1000 ${stats.avgRisk > 70 ? 'bg-red-600' : 'bg-blue-500'}`}
              style={{ width: `${stats.avgRisk}%` }}
            />
          </div>
        </div>

        <div className="lg:col-span-2 bg-slate-900/50 border border-slate-800 p-6 rounded-3xl min-h-87.5 flex flex-col shadow-xl backdrop-blur-sm">
          <p className="text-[10px] font-bold text-blue-500 uppercase mb-4 flex items-center gap-2 tracking-widest font-mono">
            <Globe size={14} className="animate-spin-slow" /> Live Attack Map
          </p>
          <div className="flex-1 rounded-xl overflow-hidden bg-black/40 relative border border-slate-800/50">
            {threats.length > 0 ? (
              <AttackMap threats={threats} />
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-slate-600 animate-pulse gap-3">
                <Activity size={40} />
                <span className="text-[10px] uppercase tracking-widest font-mono">Waiting for secure neural stream...</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 3. SECCIÓN PRINCIPAL: TABLA ESTILO TERMINAL AUSTIN */}
      <main className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-3 bg-slate-900/30 rounded-3xl border border-slate-800 overflow-hidden shadow-2xl">
          <div className="p-5 border-b border-slate-800 bg-slate-900/50 flex justify-between items-center">
            <h3 className="text-[11px] font-black uppercase tracking-[0.3em] text-slate-400 flex items-center gap-2 font-mono">
              <Activity size={14} className="text-blue-500" /> Neural Incident Log
            </h3>
            <span className="text-[9px] font-mono text-blue-500/50 uppercase">Buffer: Stable</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse font-mono">
              <thead>
                <tr className="border-b border-slate-800/50 bg-slate-900/40">
                  <th className="px-6 py-4 text-[9px] font-black uppercase text-slate-500 tracking-[0.2em]">Time</th>
                  <th className="px-6 py-4 text-[9px] font-black uppercase text-slate-500 tracking-[0.2em]">Origin / City</th>
                  <th className="px-6 py-4 text-[9px] font-black uppercase text-slate-500 tracking-[0.2em]">IP Address</th>
                  <th className="px-6 py-4 text-[9px] font-black uppercase text-slate-500 tracking-[0.2em]">AI Analysis</th>
                  <th className="px-6 py-4 text-[9px] font-black uppercase text-slate-500 tracking-[0.2em] text-center">Status</th>
                  <th className="px-6 py-4 text-[9px] font-black uppercase text-slate-500 tracking-[0.2em] text-center">Risk</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/30">
                {threats.length > 0 ? (
                  threats.map((t, index) => {
                    // --- LÓGICA DE RIESGO Y COLORES (MATRIZ AUSTIN 4 NIVELES) ---
                    const riskValue = t.risk_score || t.risk || 0;
                    let statusText = t.status || "LOGGED";
                    let statusStyle = "";
                    let riskColor = "text-emerald-500";

                    // Asignación de Estilos basada en la Matriz de Decisión
                    if (riskValue >= 90) {
                      statusText = "TERMINATED";
                      statusStyle = "border-red-600 text-red-500 bg-red-500/20 animate-pulse shadow-[0_0_10px_rgba(220,38,38,0.3)]";
                      riskColor = "text-red-500";
                    } else if (riskValue >= 70) {
                      statusText = "QUARANTINED";
                      statusStyle = "border-purple-500 text-purple-400 bg-purple-500/10";
                      riskColor = "text-purple-400";
                    } else if (riskValue >= 40) {
                      statusText = "BLOCKED";
                      statusStyle = "border-orange-500 text-orange-400 bg-orange-500/10";
                      riskColor = "text-orange-400";
                    } else {
                      statusText = "LOGGED";
                      statusStyle = "border-blue-500/50 text-blue-500 bg-blue-500/5";
                      riskColor = "text-blue-400";
                    }

                    return (
                      <tr key={t.id || index} className={`transition-all group border-b border-slate-800/20 ${isLockdown ? 'hover:bg-red-600/5' : 'hover:bg-blue-600/5'}`}>
                        {/* 1. HORA */}
                        <td className="px-6 py-5 text-[10px] text-slate-500 font-mono">
                          {t.timestamp ? new Date(t.timestamp).toLocaleTimeString() : '12:00:00 PM'}
                        </td>

                        {/* 2. LOCALIZACIÓN (CIUDAD Y PAÍS) */}
                        <td className="px-6 py-5">
                          <div className="flex flex-col">
                            <span className="text-[11px] font-bold text-white uppercase font-mono tracking-tighter">
                              {t.city || (t.location && t.location.split(',')[0]) || 'AUSTIN NODE'}
                            </span>
                            <span className="text-[9px] text-blue-500 font-black uppercase font-mono tracking-[0.2em]">
                              {t.country_code || t.pais || (t.location && t.location.split(',')[1]) || 'GLOBAL'}
                            </span>
                          </div>
                        </td>

                        {/* 3. DIRECCIÓN IP REAL */}
                        <td className="px-6 py-5 text-xs font-bold text-blue-500 font-mono">
                          <div className="flex items-center gap-2">
                            {t.source_ip || t.ip || t.ip_address || '127.0.0.1'}
                            {isLockdown && <span className="text-[7px] bg-red-500 text-white px-1 animate-pulse">TRACKING</span>}
                          </div>
                        </td>

                        {/* 4. ANÁLISIS DE IA */}
                        <td className="px-6 py-5">
                          <div className="flex flex-col gap-1 border-l-2 border-blue-500/20 pl-4">
                            <span className="text-[8px] font-black text-blue-500 uppercase font-mono tracking-[0.2em]">AI_REPORT</span>
                            <p className="text-[10px] text-slate-300 leading-tight uppercase font-mono max-w-md">
                              {t.ai_analysis || 'SECURE_DATA_STREAM'}
                            </p>
                          </div>
                        </td>

                        {/* 5. ESTADO DINÁMICO */}
                        <td className="px-6 py-5 text-center">
                          <span className={`px-4 py-1.5 rounded-full text-[9px] font-black border tracking-widest font-mono ${statusStyle}`}>
                            {isLockdown ? `MONITORED // ${statusText}` : statusText}
                          </span>
                        </td>

                        {/* 6. RISK SCORE */}
                        <td className={`px-6 py-5 text-right font-mono font-black text-sm ${riskColor}`}>
                          {riskValue}%
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td colSpan="6" className="px-6 py-32 text-center text-slate-700 uppercase text-[10px] tracking-[0.5em] font-black animate-pulse font-mono">
                      NO_THREATS_DETECTED_IN_DATABASE
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* 4. SIDEBAR */}
        <aside className="space-y-6">
          {/* System Health */}
          <div className="bg-slate-900/80 p-6 rounded-3xl border border-slate-800 shadow-xl">
            <h3 className="text-[10px] font-black mb-6 uppercase flex items-center gap-2 text-slate-400 tracking-widest font-mono">
              <Server size={14} /> System Health
            </h3>
            <div className="space-y-4 font-mono">
              {['Docker', 'PostgreSQL', 'Gemini 2.5 Flash'].map((s) => (
                <div key={s} className="flex justify-between items-center text-[10px]">
                  <span className="text-slate-500 uppercase tracking-widest">{s}</span>
                  <span className="text-emerald-500 font-bold flex items-center gap-2">
                    <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
                    {s === 'Gemini 2.5 Flash' ? 'STABLE' : 'ONLINE'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Botón de Emergencia */}
          <div
            onClick={handleLockdown}
            className={`group relative overflow-hidden border p-8 rounded-3xl text-center cursor-pointer transition-all duration-500 
      ${isLockdown
                ? 'bg-red-600 border-white shadow-[0_0_40px_rgba(255,0,0,0.4)]'
                : 'bg-red-950/20 border-red-900/30 hover:border-red-500/50'
              }`}
          >
            <ShieldAlert size={32} className={`mx-auto mb-3 transition-transform group-hover:scale-110 ${isLockdown ? 'text-white' : 'text-red-900'}`} />
            <h3 className={`text-[10px] font-black uppercase tracking-[0.2em] ${isLockdown ? 'text-white' : 'text-red-900'}`}>
              {isLockdown ? 'SYSTEM SHUTDOWN ACTIVE' : 'Emergency Lockdown'}
            </h3>
            {isLockdown && (
              <div className="absolute inset-0 bg-white/10 animate-pulse pointer-events-none" />
            )}
          </div>
        </aside>
      </main>
    </div>
  );

  // --- RENDERIZADO FINAL: SENTINEL AI INTERFACE ---

}

export default Dashboard;


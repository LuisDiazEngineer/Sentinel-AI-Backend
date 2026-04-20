import { useState, useEffect } from 'react';
import { ShieldCheck, Activity, Server, ShieldAlert } from 'lucide-react';

function App() {
  const [threats, setThreats] = useState([]);
  const [stats, setStats] = useState({ total: 0, critical: 0 });
  const [analyzingId, setAnalyzingId] = useState(null);

  // 🚀 Mejora: Ahora detecta más palabras clave del nuevo tester
  const getLevel = (text) => {
    if (!text) return 'Low';
    const lowText = text.toLowerCase();

    // Prioridad CRITICAL
    if (lowText.includes('critical') || lowText.includes('sql') || lowText.includes('ddos') || lowText.includes('malware')) {
      return 'Critical';
    }
    // Prioridad HIGH
    if (lowText.includes('high') || lowText.includes('brute force') || lowText.includes('unauthorized') || lowText.includes('access')) {
      return 'High';
    }
    // Por defecto LOW
    return 'Low';
  };
  // 1. Cambia la función de obtener datos
  const fetchThreats = async () => {
    try {
      // CAMBIO: Usamos /threats/ que es donde el tester inyecta las IPs
      const response = await fetch('http://127.0.0.1:8000/threats/');
      if (!response.ok) throw new Error("Backend offline");
      const data = await response.json();

      setThreats(data || []);

      const criticalCount = data.filter(t =>
        getLevel(t.ai_analysis || t.description) === 'Critical'
      ).length;

      setStats({ total: data.length, critical: criticalCount });
    } catch (error) {
      console.error("Error al actualizar dashboard:", error);
    }
  };

  // 2. Cambia la función de análisis (si tu endpoint de análisis también cambió)
  const runAIAnalysis = async (threatId, ip) => {
    setAnalyzingId(threatId);
    try {
      // Asegúrate de que esta URL sea la correcta en tu main.py de FastAPI
      const response = await fetch(`http://127.0.0.1:8000/analyze/${threatId}`, {
        method: 'POST'
      });
      if (response.ok) {
        fetchThreats();
      }
    } catch (error) {
      console.error("Error en Gemini Engine:", error);
    } finally {
      setAnalyzingId(null);
    }
  };



  useEffect(() => {
    fetchThreats();
    // ⏱️ Refresco cada 30 segundos como querías
    const interval = setInterval(fetchThreats, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans selection:bg-red-500 selection:text-white">
      {/* Header */}
      <header className="flex justify-between items-center mb-12 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <ShieldCheck className="text-red-600" size={32} />
            <h1 className="text-4xl font-black tracking-tighter text-white">SENTINEL<span className="text-red-600">AI</span></h1>
          </div>
          <p className="text-slate-500 font-mono text-[10px] mt-1 uppercase tracking-[0.2em]">Threat Detection System | Active Node: Austin-TX</p>
        </div>

        <div className="flex gap-4">
          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 shadow-lg min-w-35">
            <p className="text-[10px] text-slate-400 uppercase font-bold mb-1">Total Threats</p>
            <p className="text-3xl font-black text-white">{stats.total}</p>
          </div>
          <div className="bg-slate-900 p-4 rounded-xl border border-red-900/50 shadow-lg min-w-35">
            <p className="text-[10px] text-red-500 uppercase font-bold mb-1">Critical Events</p>
            <p className="text-3xl font-black text-red-500">{stats.critical}</p>
          </div>
        </div>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
          <div className="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
            <h2 className="text-xl font-bold flex items-center gap-2 text-white">
              <Activity className="text-red-500 animate-pulse" /> Live Threat Feed
            </h2>
            <div className="flex items-center gap-2">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
              </span>
              <span className="text-[10px] text-red-500 font-bold uppercase tracking-widest">Live Monitoring</span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="bg-slate-950 text-slate-500 text-[10px] uppercase tracking-widest">
                <tr>
                  <th className="p-4">Timestamp</th>
                  <th className="p-4">Source IP</th>
                  <th className="p-4">AI Analysis</th>
                  <th className="p-4 text-right">Severity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {threats.map((threat) => {
                  // Definimos el nivel usando la descripción o el análisis que viene del BACKEND
                  const content = threat.ai_analysis || threat.description || "";
                  const level = getLevel(content);

                  // Estado de "Escaneando" para esta fila específica
                  const isScanning = analyzingId === threat.id;

                  return (
                    <tr key={threat.id} className="hover:bg-slate-800/40 transition-all border-l-2 border-transparent hover:border-red-500 group">
                      <td className="p-4 text-slate-500 text-xs font-mono">
                        {new Date(threat.timestamp).toLocaleTimeString()}
                      </td>
                      <td className="p-4 font-mono text-blue-400 font-bold">
                        {threat.ip_address}
                      </td>

                      {/* CELDA DE AI ANALYSIS: Aquí es donde ocurre la magia */}
                      <td className="p-4 text-sm text-slate-300">
                        <div className="flex items-center gap-3">
                          {threat.ai_analysis ? (
                            <p className="leading-tight text-emerald-400/90 italic font-medium">
                              <span className="text-emerald-500 mr-1">●</span> {threat.ai_analysis}
                            </p>
                          ) : (
                            <button
                              onClick={() => runAIAnalysis(threat.id, threat.ip_address)}
                              disabled={isScanning}
                              className={`flex items-center gap-2 text-[10px] px-3 py-1 rounded border transition-all 
    ${isScanning
                                  ? 'bg-slate-800 border-slate-700 text-slate-500 cursor-not-allowed'
                                  : 'bg-red-600/10 border-red-500/30 text-red-500 hover:bg-red-600 hover:text-white animate-pulse hover:animate-none hover:shadow-[0_0_15px_rgba(220,38,38,0.6)]'
                                }`}
                            >
                              {isScanning ? (
                                <>
                                  <div className="h-2 w-2 border-2 border-slate-500 border-t-transparent rounded-full animate-spin"></div>
                                  Z-LOGIC SCANNING...
                                </>
                              ) : (
                                <>
                                  <Activity size={12} />
                                  RUN Z-LOGIC AI
                                </>
                              )}
                            </button>
                          )}
                        </div>
                      </td>

                      <td className="p-4 text-right">
                        <span className={`px-3 py-1 rounded-md text-[10px] font-black border shadow-sm ${level === 'Critical' ? 'bg-red-500/10 text-red-500 border-red-500/50' :
                          level === 'High' ? 'bg-orange-500/10 text-orange-500 border-orange-500/50' :
                            'bg-emerald-500/10 text-emerald-500 border-emerald-500/50'
                          }`}>
                          {level.toUpperCase()}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
            <h3 className="text-sm font-bold mb-6 flex items-center gap-2 text-slate-400 uppercase tracking-widest">
              <Server size={16} className="text-blue-500" /> Infrastructure
            </h3>
            <div className="space-y-5">
              {[
                { label: "Docker Containers", status: "Active", color: "text-emerald-500" },
                { label: "PostgreSQL DB", status: "Connected", color: "text-emerald-500" },
                { label: "Gemini AI Engine", status: "Online", color: "text-emerald-500" }
              ].map((item, idx) => (
                <div key={idx} className="flex justify-between items-center border-b border-slate-800/30 pb-2">
                  <span className="text-xs text-slate-400">{item.label}</span>
                  <div className="flex items-center gap-2">
                    <div className={`h-1.5 w-1.5 rounded-full ${item.color.replace('text', 'bg')} animate-pulse`}></div>
                    <span className={`text-[10px] font-black ${item.color}`}>{item.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-linear-to-br from-red-600/20 to-slate-900 p-6 rounded-2xl border border-red-500/20 shadow-inner relative overflow-hidden group">
            <div className="absolute -right-4 -top-4 opacity-10 group-hover:opacity-20 transition-opacity rotate-12">
              <ShieldAlert size={120} />
            </div>
            <ShieldAlert className="text-red-500 mb-4" size={32} />
            <h3 className="font-black text-white uppercase italic tracking-tighter text-xl">Protocol ZL1</h3>
            <p className="text-[11px] text-slate-400 mt-2 leading-relaxed">
              Tráfico enrutado vía Gemini 1.5 Flash. Mitigación en tiempo real activa para nodos Austin-TX.
            </p>
            <button className="mt-4 w-full bg-red-600 hover:bg-red-700 text-white text-[10px] font-bold py-2.5 rounded-lg transition-all uppercase tracking-widest active:scale-95">
              System Lockdown
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
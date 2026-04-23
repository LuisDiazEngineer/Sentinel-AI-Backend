import { useState, useEffect } from 'react';
import { Activity, Server, ShieldAlert, Globe } from 'lucide-react';
import AttackMap from './AttackMap';
import LoginScreen from './LoginScreen'; // Asegúrate de que el nombre coincida con tu archivo

function App() {
  const [threats, setThreats] = useState([]);
  const [stats, setStats] = useState({ total: 0, critical: 0, avgRisk: 0 });
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // 1. Lógica de nivel (Helper)
  const getLevel = (text) => {
    if (!text) return 'Low';
    const lowText = text.toLowerCase();
    if (lowText.includes('critical') || lowText.includes('sql') || lowText.includes('ddos')) return 'Critical';
    if (lowText.includes('high') || lowText.includes('brute force')) return 'High';
    return 'Low';
  };

  // 2. Fetch de datos
  const fetchThreats = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/threats/');
      if (!response.ok) throw new Error("Backend offline");

      const data = await response.json();
      setThreats(data || []);

      const criticalCount = data.filter(
        t => getLevel(t.ai_analysis || t.description) === 'Critical'
      ).length;

      const totalRisk = data.reduce((acc, curr) => acc + (curr.risk_score || 0), 0);
      const average = data.length > 0 ? Math.round(totalRisk / data.length) : 0;

      setStats({
        total: data.length,
        critical: criticalCount,
        avgRisk: average
      });

    } catch (error) {
      console.error("Error al actualizar dashboard:", error);
    }
  };

  // 3. Efecto de carga
  useEffect(() => {
    if (isAuthenticated) {
      fetchThreats();
      const interval = setInterval(fetchThreats, 30000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated]);

  // 🛡️ CONTROL DE ACCESO
  if (!isAuthenticated) {
    return <LoginScreen onLoginSuccess={() => setIsAuthenticated(true)} />;
  }

  // 🏎️ RENDER DEL DASHBOARD (Solo si está autenticado)
  return (
    <div className="min-h-screen bg-black text-slate-200 p-6 font-sans">

      {/* HEADER */}
      <header className="mb-8 flex justify-between items-center border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-2xl font-black tracking-tighter text-blue-500">
            SENTINEL <span className="text-white">AI</span>
          </h1>
          <p className="text-[10px] text-slate-500 font-mono uppercase">
            V1.0.4 - AUSTIN NODE READY
          </p>
        </div>
      </header>

      {/* DASHBOARD TOP PANEL */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

        {/* RISK PANEL */}
        <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-3xl">
          <p className="text-[10px] font-bold text-slate-500 uppercase mb-2">
            Global Threat Level
          </p>
          <h2 className={`text-6xl font-black ${stats.avgRisk > 70 ? 'text-red-600' : 'text-blue-500'}`}>
            {stats.avgRisk}%
          </h2>
          <div className="w-full bg-slate-800 h-1.5 mt-6 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-1000 ${stats.avgRisk > 70 ? 'bg-red-600' : 'bg-blue-500'}`}
              style={{ width: `${stats.avgRisk}%` }}
            />
          </div>
        </div>

        {/* MAP */}
        <div className="lg:col-span-2 bg-slate-900/50 border border-slate-800 p-6 rounded-3xl min-h-[350px] flex flex-col">
          <p className="text-[10px] font-bold text-blue-500 uppercase mb-4 flex items-center gap-2">
            <Globe size={14} /> Live Attack Map
          </p>
          <div className="flex-1 rounded-xl overflow-hidden bg-black/20 relative">
            {threats.length > 0 ? (
              <AttackMap threats={threats} />
            ) : (
              <div className="h-full flex items-center justify-center text-slate-600 animate-pulse">
                Waiting for secure stream...
              </div>
            )}
          </div>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <main className="grid grid-cols-1 lg:grid-cols-4 gap-8">

        {/* TABLE SECTION */}
        <div className="lg:col-span-3 bg-slate-900/30 rounded-3xl border border-slate-800 overflow-hidden">
          <div className="p-6 border-b border-slate-800 flex justify-between items-center">
            <h2 className="text-sm font-bold flex items-center gap-2 uppercase">
              <Activity className="text-red-500" size={16} />
              Incident Feed
            </h2>
            <span className="text-[10px] text-slate-500 font-mono">LIVE_LOG_RECORDS: {threats.length}</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="bg-slate-950 text-[10px] uppercase text-slate-500">
                <tr>
                  <th className="p-4">Time</th>
                  <th className="p-4">Location</th>
                  <th className="p-4">IP Address</th>
                  <th className="p-4">AI Analysis</th>
                  <th className="p-4 text-right">Risk Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {threats.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="p-4 text-[10px] text-slate-500 font-mono">
                      {t.timestamp ? new Date(t.timestamp).toLocaleTimeString() : '--:--:--'}
                    </td>
                    <td className="p-4 text-xs">
                      {t.city || t.country_code ? (
                        <span className="text-slate-200">
                          {t.city || 'Unknown'}, <span className="text-blue-400">{t.country_code || 'Global'}</span>
                        </span>
                      ) : (
                        <span className="text-slate-500 animate-pulse italic">Analyzing...</span>
                      )}
                    </td>
                    <td className="p-4 text-blue-400 font-mono text-xs">
                      {t.ip_address}
                    </td>
                    <td className="p-4 text-xs italic text-slate-400 max-w-xs truncate">
                      {t.ai_analysis || "Awaiting AI Report..."}
                    </td>
                    <td className={`p-4 text-right text-xs font-bold ${t.risk_score > 75 ? 'text-red-500' : t.risk_score > 40 ? 'text-yellow-500' : 'text-green-500'
                      }`}>
                      {t.risk_score || 0}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* SIDEBAR */}
        <aside className="space-y-6">
          <div className="bg-slate-900 p-6 rounded-3xl border border-slate-800">
            <h3 className="text-[10px] font-bold mb-4 uppercase flex items-center gap-2 text-slate-400">
              <Server size={14} /> System Health
            </h3>
            {['Docker', 'PostgreSQL', 'AI Engine'].map((s) => (
              <div key={s} className="flex justify-between text-xs mb-3">
                <span className="text-slate-500">{s}</span>
                <span className="text-emerald-500 font-bold flex items-center gap-1">
                  <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
                  ONLINE
                </span>
              </div>
            ))}
          </div>

          <div className="bg-red-600/10 border border-red-600/20 p-6 rounded-3xl text-center group cursor-pointer hover:bg-red-600 transition-all duration-300">
            <ShieldAlert className="mx-auto mb-2 text-red-600 group-hover:text-white" />
            <h3 className="text-xs font-black uppercase text-red-600 group-hover:text-white">
              Emergency Lockdown
            </h3>
          </div>
        </aside>

      </main>
    </div>
  );
}

export default App;
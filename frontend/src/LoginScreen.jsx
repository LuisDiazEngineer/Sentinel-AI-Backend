import React, { useState } from 'react';
import { ShieldCheck, Lock, User } from 'lucide-react';

const Login = ({ onLoginSuccess }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        // Preparamos los datos como Form Data (que es lo que pide OAuth2 en FastAPI)
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch('http://localhost:8000/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                onLoginSuccess(); // Esto desbloquea el Dashboard
            } else {
                setError('Credenciales inválidas. Acceso denegado.');
            }
        } catch (err) {
            setError('Error de conexión con Sentinel Backend');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-slate-950 font-sans">
            <div className="w-full max-w-md p-8 space-y-6 bg-slate-900/50 border border-slate-800 rounded-2xl backdrop-blur-xl shadow-2xl shadow-blue-500/10">

                {/* Header con Icono */}
                <div className="flex flex-col items-center">
                    <div className="p-3 bg-blue-500/10 rounded-full mb-4">
                        <ShieldCheck className="w-12 h-12 text-blue-500" />
                    </div>
                    <h1 className="text-3xl font-bold tracking-tighter text-white">SENTINEL AI</h1>
                    <p className="text-slate-400 text-sm mt-1">Sistemas de Defensa & Monitoreo</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Campo Usuario */}
                    <div className="relative">
                        <User className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                        <input
                            type="text"
                            placeholder="Usuario del Sistema"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full pl-10 pr-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                            required
                        />
                    </div>

                    {/* Campo Password */}
                    <div className="relative">
                        <Lock className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                        <input
                            type="password"
                            placeholder="Código de Acceso"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full pl-10 pr-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                            required
                        />
                    </div>

                    {error && <p className="text-red-500 text-xs italic text-center animate-shake">{error}</p>}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg transition-all transform active:scale-95 shadow-lg shadow-blue-900/20"
                    >
                        {loading ? 'Verificando...' : 'INICIAR SESIÓN'}
                    </button>
                </form>

                <div className="text-center">
                    <p className="text-[10px] text-slate-600 uppercase tracking-widest">
                        Acceso restringido a personal autorizado
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;
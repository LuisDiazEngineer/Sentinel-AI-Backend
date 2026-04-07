import React, { useState, useEffect } from 'react';
import './App.css';

function App() {

  const [logs, setLogs] = useState([
    { ip: 'Cargando...', accion: 'Esperando' }
  ]);
  const [status, setStatus] = useState('Conectando...');


  useEffect(() => {
    const obtenerDatos = async () => {
      try {

        const respuesta = await fetch('http://localhost:8000/ataques');
        if (respuesta.ok) {
          const datos = await respuesta.json();
          setLogs(datos);
          setStatus('En línea');
        }
      } catch (error) {
        console.error("Python no responde aún, usando datos de prueba...");
        setStatus('Error de conexión');

        setLogs([
          { ip: '192.168.1.50', accion: 'Intento de Intrusión' },
          { ip: '10.0.0.12', accion: 'Escaneo de Puertos' }
        ]);
      }
    };

    obtenerDatos();

    const intervalo = setInterval(obtenerDatos, 5000);
    return () => clearInterval(intervalo);
  }, []);


  return (
    <div className="dashboard-container">
      <header>
        <h1>Sentinel-AI Monitor</h1>
        <p>Estado: <span className={status === 'En línea' ? 'status-online' : 'status-offline'}>
          {status}
        </span></p>
      </header>

      <main className="main-content">
        <div className="card map-card">
          <h2>Mapa de Amenazas</h2>
          <div className="map-placeholder">
            <div className="radar-circle"></div>
            <p>Escaneando red en tiempo real...</p>
          </div>
        </div>

        <div className="card log-card">
          <h2>Logs de Ataques Real-Time</h2>
          <table className="log-table">
            <thead>
              <tr>
                <th>IP de Origen</th>
                <th>Acción Detectada</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((item, index) => (
                <tr key={index}>
                  <td className="ip-text">{item.ip}</td>
                  <td><span className="badge">{item.accion}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

export default App;
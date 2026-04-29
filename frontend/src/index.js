import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css'; // Importación de estilos globales y Tailwind v4
import App from './App.jsx'; // Componente raíz que orquestará el Dashboard y el Login

/**
 * 1. SELECCIÓN DEL NODO MONTAJE
 * Relación: Busca en tu archivo /index.html el <div id="root">.
 * Es el único punto de contacto real entre el HTML estático y el JavaScript dinámico.
 */
const rootElement = document.getElementById('root');

/**
 * 2. CREACIÓN DE LA RAÍZ (Concurrent Mode)
 * Relación: Usa la nueva API de React 18+ para inicializar la aplicación.
 * Esto permite que React gestione mejor las actualizaciones de la UI sin bloquear el navegador.
 */
const root = createRoot(rootElement);

/**
 * 3. RENDERIZADO INICIAL
 * Relación: 'StrictMode' es una herramienta de desarrollo que ayuda a encontrar
 * errores comunes, haciendo que los componentes se rendericen dos veces (solo en dev)
 * para asegurar que no tengan efectos secundarios no deseados.
 */
root.render(
    <StrictMode>
        {/* El componente App contiene los Providers (AuthContext) y las Rutas */}
        <App />
    </StrictMode>
);
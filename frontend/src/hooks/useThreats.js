import { useState, useEffect } from 'react';
import api from '../services/api'; // Importamos la instancia de Axios con el interceptor de seguridad

/**
 * HOOK PERSONALIZADO: useThreats
 * Relación: Centraliza la lógica de comunicación con el endpoint de amenazas.
 * Permite que cualquier componente obtenga los datos sin repetir la lógica de fetch.
 */
export const useThreats = () => {
    // 1. ESTADOS LOCALES DEL HOOK
    const [threats, setThreats] = useState([]); // Almacena la lista de incidentes (PostgreSQL)
    const [loading, setLoading] = useState(true); // Controla el estado de carga (Skeleton/Spinners)

    /**
     * 2. FUNCIÓN DE PETICIÓN (ASYNC/AWAIT)
     * Relación: Conecta con el controlador de FastAPI.
     * Al usar la instancia 'api', el token JWT se adjunta automáticamente.
     */
    const fetchThreats = async () => {
        try {
            // Realizamos la petición GET a la ruta protegida
            const response = await api.get('/threats/all');

            // Actualizamos el estado con los datos recibidos del backend
            setThreats(response.data);
        } catch (err) {
            // Gestión de errores: Log en consola para depuración técnica
            console.error("Error cargando amenazas", err);
        } finally {
            // Finalizamos el estado de carga independientemente del resultado
            setLoading(false);
        }
    };

    /**
     * 3. EFECTO DE MONTAJE
     * Relación: Dispara la primera carga de datos en cuanto el componente se carga.
     */
    useEffect(() => {
        fetchThreats();
    }, []);

    /**
     * 4. EXPOSICIÓN DE LA API DEL HOOK
     * Relación: Retornamos los datos y la función 'refresh' por si el usuario
     * quiere actualizar la lista manualmente (ej: un botón de "Recargar").
     */
    return { threats, loading, refresh: fetchThreats };
};
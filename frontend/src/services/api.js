import axios from 'axios';

/**
 * 1. CONFIGURACIÓN DE URL BASE
 * Relación: Centraliza la dirección del backend de FastAPI. 
 * Si mañana despliegas el backend en la nube (ej. AWS o Google Cloud), 
 * solo cambias esta línea y toda la app se actualiza.
 */
const API_URL = "http://localhost:8000";

/**
 * 2. INSTANCIA PERSONALIZADA DE AXIOS
 * Relación: Crea un cliente HTTP pre-configurado. 
 * Esto evita tener que escribir la URL completa en cada componente.
 */
const api = axios.create({
    baseURL: API_URL,
});

/**
 * 3. INTERCEPTOR DE PETICIONES (The Security Layer)
 * Relación: Este es el "peaje" por donde pasan todas las llamadas al backend.
 * Antes de que la petición salga hacia FastAPI, el interceptor inyecta el JWT.
 */
api.interceptors.request.use((config) => {
    // Extraemos el token del almacenamiento persistente
    const token = localStorage.getItem('token');

    if (token) {
        /**
         * 4. INYECCIÓN DEL HEADER DE AUTORIZACIÓN
         * Relación: Implementa el estándar OAuth2. 
         * FastAPI recibirá el header 'Authorization: Bearer <token>' 
         * y permitirá el acceso a las rutas protegidas automáticamente.
         */
        config.headers.Authorization = `Bearer ${token}`;
    }


    return config;
}, (error) => {
    // Manejo de errores en la salida de la petición
    return Promise.reject(error);
});

export default api;
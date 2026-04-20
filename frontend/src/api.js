import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000', // La dirección de tu FastAPI en Docker
});

export default api;
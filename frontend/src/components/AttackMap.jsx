import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';

/**
 * COMPONENTE AttackMap
 * Propósito: Visualización geoespacial de las amenazas detectadas.
 * Relación: Recibe los datos procesados por el Backend y los proyecta sobre un mapa global.
 */
const AttackMap = ({ threats }) => {
    // Posición inicial: Coordenadas [lat, lng] para centrar el mapa al cargar.
    const center = [20, 0];

    return (
        <MapContainer
            center={center}
            zoom={2}
            style={{
                height: '100%',
                width: '100%',
                borderRadius: '12px',
                background: '#020617' // Color oscuro para hacer match con el estilo "Cyber"
            }}
        >
            {/* 1. Capa de diseño del mapa (Dark Mode) */}
            {/* Relación: Usa el set de CARTO para darle ese aspecto de centro de comando. */}
            <TileLayer
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                attribution='&copy; OpenStreetMap contributors &copy; CARTO'
            />

            {/* 2. Renderizado dinámico de marcadores */}
            {/* Relación: Itera sobre el array de amenazas que viene de la base de datos de FastAPI. */}
            {threats.map((threat) => (
                // Verificación de integridad: Solo dibuja si el backend envió coordenadas válidas.
                threat.latitude && threat.longitude && (
                    <CircleMarker
                        key={threat.id}
                        center={[threat.latitude, threat.longitude]}
                        pathOptions={{
                            // SEMÁFORO DE RIESGO: 
                            // Si el risk_score > 70 es rojo (Crítico), de lo contrario es azul (Informativo).
                            color: threat.risk_score > 70 ? '#ef4444' : '#3b82f6',
                            fillColor: threat.risk_score > 70 ? '#ef4444' : '#3b82f6',
                            fillOpacity: 0.6
                        }}
                        // ESCALADO VISUAL: El tamaño del punto depende de la gravedad del ataque.
                        radius={Math.max(5, threat.risk_score / 10)}
                    >
                        {/* 3. Ventana informativa (Popup) */}
                        {/* Relación: Muestra el análisis generado por Gemini AI al hacer clic. */}
                        <Popup>
                            <div className="text-xs font-sans">
                                <p className="font-bold text-red-600 mb-1">
                                    {threat.ip_address}
                                </p>
                                <p className="text-slate-800 font-semibold">
                                    {threat.city}, {threat.country_code}
                                </p>
                                {/* Muestra el reporte técnico de la IA */}
                                <p className="italic text-slate-600 mt-1">
                                    {threat.ai_analysis || "No AI analysis available"}
                                </p>
                                <p className="mt-1 font-bold text-blue-700">
                                    Risk: {threat.risk_score}%
                                </p>
                            </div>
                        </Popup>
                    </CircleMarker>
                )
            ))}
        </MapContainer>
    );
};

export default AttackMap;
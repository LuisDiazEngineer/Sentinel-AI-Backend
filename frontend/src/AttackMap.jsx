import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';

const AttackMap = ({ threats }) => {
    // Posición inicial: Un punto medio global
    const center = [20, 0];

    return (
        <MapContainer
            center={center}
            zoom={2}
            style={{
                height: '100%',
                width: '100%',
                borderRadius: '12px',
                background: '#020617'
            }}
        >
            <TileLayer
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                attribution='&copy; OpenStreetMap contributors &copy; CARTO'
            />

            {threats.map((threat) => (
                // Solo renderiza el punto si tiene coordenadas válidas
                threat.latitude && threat.longitude && (
                    <CircleMarker
                        key={threat.id}
                        center={[threat.latitude, threat.longitude]}
                        pathOptions={{
                            color: threat.risk_score > 70 ? '#ef4444' : '#3b82f6',
                            fillColor: threat.risk_score > 70 ? '#ef4444' : '#3b82f6',
                            fillOpacity: 0.6
                        }}
                        // El radio mínimo es 5 para que siempre se vea un puntito
                        radius={Math.max(5, threat.risk_score / 10)}
                    >
                        <Popup>
                            <div className="text-xs font-sans">
                                <p className="font-bold text-red-600 mb-1">
                                    {threat.ip_address}
                                </p>
                                <p className="text-slate-800 font-semibold">
                                    {threat.city}, {threat.country_code}
                                </p>
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
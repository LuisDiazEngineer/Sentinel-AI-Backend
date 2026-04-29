import React from "react";
import ReactDOM from "react-dom/client";
import Dashboard from "./pages/Dashboard";
import { AuthProvider } from "./context/AuthContext"; // <--- IMPORTANTE
import "./index.css";
import "leaflet/dist/leaflet.css";

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <AuthProvider> {/* <--- DEBE ENVOLVER AL COMPONENTE */}
            <Dashboard />
        </AuthProvider>
    </React.StrictMode>
);
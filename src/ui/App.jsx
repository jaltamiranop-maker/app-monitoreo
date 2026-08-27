import { useState, useEffect, useRef } from "react";
// ─── COMPONENTS ───────────────────────────────────────────────────────────────
import Field from "./components/Field";
import Input from "./components/Input";
import Select from "./components/Select";
import SectionHeader from "./components/SectionHeader";
import Toast from "./components/Toast";
import PanelBar from "./cards/PanelBar";
// ─── SIDEBAR FORM ─────────────────────────────────────────────────────────────
import SidebarForm from "./cards/SideBarForm/SideBarForm";
// ─── OPTIMIZER TAB ────────────────────────────────────────────────────────────
import OptimizerTab from "./cards//OptimizerTab/OptimizerTab";
// ─── HISTORY TAB ────────────────────────────────────────────────────────────
import HistoryTab from "./cards/HistoryTab/HistoryTab";
// ─── CONSTANTS ───────────────────────────────────────────────────────────────
const API_BASE = "http://127.0.0.1:8000";

// ─── STYLES ───────────────────────────────────────────────────────────────
import "./styles/variables.css"
import "./styles/globals.css"
import "./styles/animations.css"
import "./styles/aplication/App.css"



const today = () => new Date().toISOString().split("T")[0];

// ─── HELPERS ─────────────────────────────────────────────────────────────────
const fmt = (n) => new Intl.NumberFormat("es-CO").format(n);

// ─── ICONS (inline SVG) ───────────────────────────────────────────────────────
const IconCut = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/>
    <line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/>
    <line x1="8.12" y1="8.12" x2="12" y2="12"/>
  </svg>
);
const IconHistory = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-4.95"/>
  </svg>
);


// ─── APP ROOT ─────────────────────────────────────────────────────────────────
export default function App() {
  const [tab, setTab] = useState("optimizer");
  const [nextOrden, setNextOrden] = useState(1);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [form, setForm] = useState({
    f_despiece: today(), comercial: "", orden_compra: "",
    cliente: "", nit: "", contacto: "", telefono: "", correo: "",
    sector: "", mercado: "", canal: "", tipo_destino: "",
    transporte: "", servicio_logistico: "", ciudad: "",
    direccion: "", f_entrega: today(), producto: "", kit: "", cantidad_kit: 0,
  });

  useEffect(() => {
    fetch(`${API_BASE}/siguiente_orden`).then(r => r.ok ? r.json() : null).then(d => { if (d) setNextOrden(d.siguiente); }).catch(() => {});
  }, []);

  const handleOrdenSaved = () => setNextOrden(n => n + 1);

  return (
    <>
      
      {/* TOP NAV */}
      <header className="top-nav">
        <div className="top-nav-section-left">
          <button onClick={() => setSidebarOpen(o => !o)} className="top-nav-button-form">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
          </button>
          <div>
            <div  className="top-nav-name-company">KINGSPAN</div>
            <div className="top-nav-text-optmizer">Optimizador de Cortes</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 4 }}>
          {[["optimizer","🚀 Optimizador", <IconCut />],["history","📜 Historial", <IconHistory />]].map(([id, label, icon]) => (
            <button key={id} onClick={() => setTab(id)} className={`top-nav-button-optimizer-historial ${ tab === id ? "active" : ""}`}>
              {icon} {label.split(" ").slice(1).join(" ")}
            </button>
          ))}
        </div>
        <div className="top-nav-text-copyright">
          © 2026 Kingspan Optimization Tools
        </div>
      </header>

      <div className="sidebar">
        {/* SIDEBAR */}
        <aside className={`sidebar-aside ${ sidebarOpen ? "open" : ""}`}
        >
          <div className="sidebar-container-box">
            <div className="sidebar-info-production">
              <span className="sidebar-info-production-text">Datos de Producción</span>
              <span className="sidebar-info-production-num">
                #{String(nextOrden).padStart(4, "0")}
              </span>
            </div>
            <SidebarForm form={form} setForm={setForm} nextOrden={nextOrden} />
          </div>
        </aside>

        {/* MAIN */}
        <main className="main">
          {tab === "optimizer" && <OptimizerTab form={form} nextOrden={nextOrden} onOrdenSaved={handleOrdenSaved} />}
          {tab === "history" && <HistoryTab />}
        </main>
      </div>
    </>
  );
}

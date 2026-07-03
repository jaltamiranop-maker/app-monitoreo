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
// ─── CONSTANTS ───────────────────────────────────────────────────────────────
const API_BASE = "http://127.0.0.1:8000";


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
const IconDownload = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
  </svg>
);





// ─── HISTORY TAB ──────────────────────────────────────────────────────────────
function HistoryTab() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [regenId, setRegenId] = useState("");
  const [toast, setToast] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/historial`);
      if (res.ok) setHistory(await res.json());
    } catch {}
    setLoading(false);
  };

  useEffect(() => { fetchHistory(); }, []);

  const handleRegen = async () => {
    if (!regenId) return;
    try {
      const res = await fetch(`${API_BASE}/regenerar_pdf/${regenId}`, { method: "POST" });
      if (!res.ok) throw new Error("No encontrado");
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a"); a.href = url; a.download = `Orden_${regenId}.pdf`; a.click();
      URL.revokeObjectURL(url);
      setToast({ message: `PDF de la orden #${regenId} descargado.`, type: "-success" });
    } catch (e) {
      setToast({ message: `Error: ${e.message}`, type: "-error" });
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      <div style={{ background: "var(--card)", border: "1px solid var(--border)", borderRadius: 12, padding: 20 }}>
        <SectionHeader>Historial de Órdenes</SectionHeader>
        {loading ? (
          <div style={{ textAlign: "center", padding: 32, color: "var(--text-muted)" }}>Cargando historial...</div>
        ) : history.length === 0 ? (
          <div style={{ textAlign: "center", padding: 32, color: "var(--text-muted)" }}>
            <div style={{ fontSize: 32, marginBottom: 8 }}>📋</div>
            No hay órdenes registradas.
          </div>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
              <thead>
                <tr style={{ background: "var(--blue)" }}>
                  {["N° Orden","Fecha Registro","Cliente","Producto"].map(h => (
                    <th key={h} style={{ padding: "8px 14px", color: "#fff", fontWeight: 700, textAlign: "left", fontSize: 11, letterSpacing: "0.05em" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {history.map((row, i) => (
                  <tr key={i} style={{ borderBottom: "1px solid var(--border)", background: i % 2 === 0 ? "transparent" : "var(--input-bg)" }}>
                    <td style={{ padding: "9px 14px", fontWeight: 800, color: "var(--blue)" }}>#{String(row["N° Orden"]).padStart(4,"0")}</td>
                    <td style={{ padding: "9px 14px", color: "var(--text-muted)" }}>{row["Fecha Registro"]}</td>
                    <td style={{ padding: "9px 14px", fontWeight: 600 }}>{row["Cliente"]}</td>
                    <td style={{ padding: "9px 14px", fontSize: 11, color: "var(--text-muted)" }}>{row["Producto"]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div style={{ background: "var(--card)", border: "1px solid var(--border)", borderRadius: 12, padding: 20 }}>
        <SectionHeader>Re-descargar Orden</SectionHeader>
        <div style={{ display: "flex", gap: 10, alignItems: "flex-end" }}>
          <Field label="N° de Orden a recuperar">
            <Select value={regenId} onChange={e => setRegenId(e.target.value)} style={{ minWidth: 160 }}>
              <option value="">— Selecciona —</option>
              {history.map(r => (
                <option key={r["N° Orden"]} value={r["N° Orden"]}>#{String(r["N° Orden"]).padStart(4,"0")} — {r["Cliente"]}</option>
              ))}
            </Select>
          </Field>
          <button onClick={handleRegen} disabled={!regenId} style={{
            background: regenId ? "var(--blue)" : "var(--border)", color: regenId ? "#fff" : "var(--text-muted)",
            border: "none", borderRadius: 8, padding: "9px 18px", fontSize: 12, fontWeight: 700,
            cursor: regenId ? "pointer" : "not-allowed", display: "flex", alignItems: "center", gap: 8,
            marginBottom: 1
          }}>
            <IconDownload /> Generar PDF
          </button>
        </div>
      </div>
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  );
}

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
      <style>{`
        :root {
          --blue: #003B8E;
          --gold: #C5A028;
          --bg: #F4F6FA;
          --card: #FFFFFF;
          --border: #E2E8F0;
          --text: #1A202C;
          --text-muted: #718096;
          --input-bg: #F7F9FC;
          --sidebar-w: 280px;
          --accent: #C5A028;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); }
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes slideUp { from { transform: translateY(16px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        input::-webkit-outer-spin-button, input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
        input[type=number] { -moz-appearance: textfield; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
      `}</style>

      {/* TOP NAV */}
      <header style={{
        background: "var(--blue)", color: "#fff", padding: "0 24px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        height: 56, position: "sticky", top: 0, zIndex: 100,
        boxShadow: "0 2px 16px rgba(0,59,142,0.25)"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <button onClick={() => setSidebarOpen(o => !o)} style={{
            background: "rgba(255,255,255,0.12)", border: "none", borderRadius: 6,
            color: "#fff", cursor: "pointer", padding: "6px 8px", lineHeight: 0
          }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
          </button>
          <div>
            <div style={{ fontWeight: 800, fontSize: 15, letterSpacing: "0.03em" }}>KINGSPAN</div>
            <div style={{ fontSize: 10, color: "rgba(255,255,255,0.65)", fontWeight: 500, letterSpacing: "0.08em", textTransform: "uppercase" }}>Optimizador de Cortes</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 4 }}>
          {[["optimizer","🚀 Optimizador", <IconCut />],["history","📜 Historial", <IconHistory />]].map(([id, label, icon]) => (
            <button key={id} onClick={() => setTab(id)} style={{
              background: tab === id ? "rgba(255,255,255,0.18)" : "transparent",
              color: "#fff", border: tab === id ? "1px solid rgba(255,255,255,0.35)" : "1px solid transparent",
              borderRadius: 7, padding: "6px 16px", cursor: "pointer", fontSize: 12, fontWeight: 700,
              letterSpacing: "0.03em", transition: "all 0.15s", display: "flex", alignItems: "center", gap: 7
            }}>
              {icon} {label.split(" ").slice(1).join(" ")}
            </button>
          ))}
        </div>
        <div style={{ fontSize: 11, color: "rgba(255,255,255,0.5)", letterSpacing: "0.05em" }}>
          © 2026 Kingspan Optimization Tools
        </div>
      </header>

      <div style={{ display: "flex", minHeight: "calc(100vh - 56px)" }}>
        {/* SIDEBAR */}
        <aside style={{
          width: sidebarOpen ? "var(--sidebar-w)" : 0, minWidth: sidebarOpen ? "var(--sidebar-w)" : 0,
          background: "var(--card)", borderRight: "1px solid var(--border)",
          overflowY: "auto", overflowX: "hidden",
          transition: "width 0.25s ease, min-width 0.25s ease",
          flexShrink: 0
        }}>
          <div style={{ width: "var(--sidebar-w)", padding: "20px 16px 0" }}>
            <div style={{
              background: "var(--blue)", borderRadius: 8, padding: "10px 14px",
              marginBottom: 18, display: "flex", alignItems: "center", justifyContent: "space-between"
            }}>
              <span style={{ color: "rgba(255,255,255,0.8)", fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase" }}>Datos de Producción</span>
              <span style={{ background: "var(--gold)", color: "#fff", borderRadius: 4, padding: "2px 8px", fontSize: 10, fontWeight: 800 }}>
                #{String(nextOrden).padStart(4, "0")}
              </span>
            </div>
            <SidebarForm form={form} setForm={setForm} nextOrden={nextOrden} />
          </div>
        </aside>

        {/* MAIN */}
        <main style={{ flex: 1, padding: 24, overflowX: "hidden" }}>
          {tab === "optimizer" && <OptimizerTab form={form} nextOrden={nextOrden} onOrdenSaved={handleOrdenSaved} />}
          {tab === "history" && <HistoryTab />}
        </main>
      </div>
    </>
  );
}

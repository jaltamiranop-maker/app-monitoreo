import { useState, useEffect, useRef } from "react";

import CortesInput from "./sections/CortesInput";

import SectionHeader from "../../components/SectionHeader";
import Toast from "../../components/Toast";
import Field from "../../components/Field";
import Input from "../../components/Input";
import PanelBar from "../PanelBar";


const API_BASE = "http://127.0.0.1:8000";
const PANEL_SIZES = [12000, 9000, 6000, 3000];


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
const IconDownload = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
  </svg>
);
const IconPlus = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
);
const IconTrash = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
  </svg>
);
const IconCheck = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><polyline points="20 6 9 17 4 12"/></svg>
);

export default function OptimizerTab({ form, nextOrden, onOrdenSaved }) {
  const [rows, setRows] = useState([{ longitud: "", cantidad: "" }]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const [logistica, setLogistica] = useState([
    { Concepto: "SERVICIO LOGÍSTICO", Tipo: form.servicio_logistico || "", Cantidad: 1, Precio_COP: 2800000 },
    { Concepto: "", Tipo: "", Cantidad: 0, Precio_COP: 0 },
  ]);
  const [saved, setSaved] = useState(false);

  const addRow = () => setRows(r => [...r, { longitud: "", cantidad: "" }]);
  const removeRow = (i) => setRows(r => r.filter((_, idx) => idx !== i));
  const setRow = (i, k, v) => setRows(r => r.map((row, idx) => idx === i ? { ...row, [k]: v } : row));

  const validCortes = rows.filter(r => r.longitud > 0 && r.cantidad > 0)
    .map(r => ({ longitud: parseInt(r.longitud), cantidad: parseInt(r.cantidad) }));

  const handleOptimize = async () => {
    if (!validCortes.length) { setToast({ message: "Ingresa al menos un corte válido.", type: "-warning" }); return; }
    setLoading(true); setResult(null); setSaved(false);
    try {
      const res = await fetch(`${API_BASE}/optimizar`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cortes: validCortes }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setResult(await res.json());
      setToast({ message: "Optimización completada con éxito.", type: "-success" });
    } catch (e) {
      setToast({ message: `Error: ${e.message}. ¿Está corriendo el backend en ${API_BASE}?`, type: "-error" });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveAndDownload = async () => {
    if (!form.cliente || !form.nit) { setToast({ message: "Completa el nombre del cliente y NIT.", type: "-warning" }); return; }
    if (form.transporte === "Kingspan" && !form.servicio_logistico) { setToast({ message: "Selecciona el servicio logístico.", type: "-warning" }); return; }
    try {
      const payload = { ...form, n_orden: nextOrden, servicio_logistico_tabla: logistica };
      const res = await fetch(`${API_BASE}/guardar_pedido`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ datos_pdf: payload, resultado: result }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setSaved(true);
      onOrdenSaved();
      setToast({ message: `Orden #${String(nextOrden).padStart(4,"0")} guardada.`, type: "-success" });
      // Download PDF
      const pdfRes = await fetch(`${API_BASE}/generar_pdf`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ datos_pdf: payload, resultado: result }),
      });
      if (pdfRes.ok) {
        const blob = await pdfRes.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url; a.download = `Orden_${String(nextOrden).padStart(4,"0")}_${form.cliente}.pdf`; a.click();
        URL.revokeObjectURL(url);
      }
    } catch (e) {
      setToast({ message: `Error al guardar: ${e.message}`, type: "-error" });
    }
  };

  // Summary
  const summary = result ? PANEL_SIZES.map(s => ({ size: s, qty: result.filter(r => r.Tamaño === s).length })) : [];
  const totalArea = result ? result.reduce((acc, row) => {
    return acc + row.Cortes.split(",").reduce((s, c) => s + parseInt(c.trim()), 0);
  }, 0) / 1000 : 0;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "320px 1fr", gap: 24, alignItems: "start" }}>
      {/* LEFT: cortes input */}
      <div>
        <CortesInput
            rows={rows}
            setRow={setRow}
            addRow={addRow}
            removeRow={removeRow}
            handleOptimize={handleOptimize}
            loading={loading}
        />
      </div>

      {/* RIGHT: results */}
      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        {!result && (
          <div style={{
            background: "var(--card)", border: "1.5px dashed var(--border)", borderRadius: 12,
            padding: 48, textAlign: "center", color: "var(--text-muted)"
          }}>
            <div style={{ fontSize: 40, marginBottom: 12 }}>📐</div>
            <div style={{ fontSize: 14, fontWeight: 600 }}>Configura los cortes y presiona <strong>Calcular Optimización</strong></div>
            <div style={{ fontSize: 12, marginTop: 6 }}>Los resultados aparecerán aquí.</div>
          </div>
        )}

        {result && (
          <>
            {/* Summary metrics */}
            <div style={{
              background: "var(--card)", border: "1px solid var(--border)", borderRadius: 12, padding: 20
            }}>
              <SectionHeader>Resumen de Inventario</SectionHeader>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 16 }}>
                {summary.map(s => (
                  <div key={s.size} style={{
                    background: s.qty > 0 ? "var(--blue)" : "var(--input-bg)",
                    borderRadius: 10, padding: "14px 10px", textAlign: "center",
                    border: `1px solid ${s.qty > 0 ? "var(--blue)" : "var(--border)"}`
                  }}>
                    <div style={{ fontSize: 22, fontWeight: 800, color: s.qty > 0 ? "#fff" : "var(--text-muted)" }}>{s.qty}</div>
                    <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: "0.06em", color: s.qty > 0 ? "rgba(255,255,255,0.8)" : "var(--text-muted)", marginTop: 2 }}>{fmt(s.size)} mm</div>
                  </div>
                ))}
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
                {[
                  ["Paneles Totales", result.length],
                  ["Área Total", `${totalArea.toFixed(2)} m²`],
                  ["Desperdicio Total", `${result.reduce((a, r) => a + r.Desperdicio, 0)} mm`],
                ].map(([label, value]) => (
                  <div key={label} style={{
                    background: "var(--input-bg)", borderRadius: 8, padding: "10px 12px",
                    border: "1px solid var(--border)"
                  }}>
                    <div style={{ fontSize: 11, color: "var(--text-muted)", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.07em" }}>{label}</div>
                    <div style={{ fontSize: 18, fontWeight: 800, color: "var(--blue)", marginTop: 2 }}>{value}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Detail table */}
            <div style={{
              background: "var(--card)", border: "1px solid var(--border)", borderRadius: 12, padding: 20
            }}>
              <SectionHeader>Detalle por Panel</SectionHeader>
              <div style={{ overflowX: "auto" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
                  <thead>
                    <tr style={{ background: "var(--blue)" }}>
                      {["Panel","Tamaño (mm)","Cortes","Desperdicio (mm)","Distribución Visual"].map(h => (
                        <th key={h} style={{ padding: "8px 12px", color: "#fff", fontWeight: 700, textAlign: "left", fontSize: 11, letterSpacing: "0.05em" }}>{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {result.map((row, i) => (
                      <tr key={i} style={{ borderBottom: "1px solid var(--border)", background: i % 2 === 0 ? "transparent" : "var(--input-bg)" }}>
                        <td style={{ padding: "8px 12px", fontWeight: 700, color: "var(--blue)" }}>{row.Panel}</td>
                        <td style={{ padding: "8px 12px", fontWeight: 600 }}>{fmt(row.Tamaño)}</td>
                        <td style={{ padding: "8px 12px", fontFamily: "monospace", fontSize: 11, color: "var(--text-muted)" }}>{row.Cortes}</td>
                        <td style={{ padding: "8px 12px", color: row.Desperdicio > 1000 ? "#dc2626" : row.Desperdicio > 200 ? "#d97706" : "#16a34a", fontWeight: 600 }}>
                          {fmt(row.Desperdicio)}
                        </td>
                        <td style={{ padding: "8px 12px", minWidth: 160 }}><PanelBar panel={row} /></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Logística */}
            <div style={{
              background: "var(--card)", border: "1px solid var(--border)", borderRadius: 12, padding: 20
            }}>
              <SectionHeader>Servicio Logístico</SectionHeader>
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
                <thead>
                  <tr style={{ background: "var(--blue)" }}>
                    {["Concepto","Tipo","Cantidad","COP $"].map(h => (
                      <th key={h} style={{ padding: "8px 12px", color: "#fff", fontWeight: 700, textAlign: "left", fontSize: 11 }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {logistica.map((item, i) => (
                    <tr key={i} style={{ borderBottom: "1px solid var(--border)" }}>
                      <td style={{ padding: "6px 12px", fontWeight: 600, fontSize: 12 }}>{item.Concepto}</td>
                      <td style={{ padding: "6px 8px" }}>
                        <Input value={item.Tipo} onChange={e => setLogistica(l => l.map((x, idx) => idx === i ? { ...x, Tipo: e.target.value } : x))}
                          style={{ padding: "5px 8px", fontSize: 12 }} />
                      </td>
                      <td style={{ padding: "6px 8px" }}>
                        <Input type="number" min="0" step="0.01" value={item.Cantidad}
                          onChange={e => setLogistica(l => l.map((x, idx) => idx === i ? { ...x, Cantidad: parseFloat(e.target.value) || 0 } : x))}
                          style={{ padding: "5px 8px", fontSize: 12, width: 80 }} />
                      </td>
                      <td style={{ padding: "6px 8px" }}>
                        <Input type="number" min="0" step="50000" value={item.Precio_COP}
                          onChange={e => setLogistica(l => l.map((x, idx) => idx === i ? { ...x, Precio_COP: parseInt(e.target.value) || 0 } : x))}
                          style={{ padding: "5px 8px", fontSize: 12, width: 120 }} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Save & Download */}
            <div style={{ display: "flex", gap: 12 }}>
              <button onClick={handleSaveAndDownload} disabled={saved} style={{
                flex: 1, background: saved ? "#16a34a" : "var(--gold)",
                color: "#fff", border: "none", borderRadius: 8, padding: "12px 20px",
                fontSize: 13, fontWeight: 800, cursor: saved ? "default" : "pointer",
                display: "flex", alignItems: "center", justifyContent: "center", gap: 8,
                transition: "background 0.2s"
              }}>
                {saved ? <><IconCheck /> Orden Guardada</> : <><IconDownload /> Guardar y Descargar PDF</>}
              </button>
            </div>
          </>
        )}
      </div>

      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  );
}
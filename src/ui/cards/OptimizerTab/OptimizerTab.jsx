import { useState, useEffect, useRef } from "react";
//CARDS LEFT---------------------------------------------------------------
import PanelTable from "./sections/PanelTable";
import CortesInput from "./sections/CortesInput";
//CARDS RIGHT---------------------------------------------------------------
import Logistica from "./sections/Logistica";
import SectionHeader from "../../components/SectionHeader";
import InventorySummary from "./sections/InventorySummary";

//COMPONENST---------------------------------------------------------------------
import Toast from "../../components/Toast";
import Field from "../../components/Field";
import Input from "../../components/Input";
import PanelBar from "../PanelBar";

import "../../styles/cards/OptimizerTab/OptimizerTab.css"

const API_BASE = "http://127.0.0.1:8000";
const PANEL_SIZES = [12000, 9000, 6000, 3000];


// ─── HELPERS ─────────────────────────────────────────────────────────────────
const fmt = (n) => new Intl.NumberFormat("es-CO").format(n);

// ─── ICONS (inline SVG) ───────────────────────────────────────────────────────

const IconDownload = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
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
    <div className="optimizer-tab">
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
      <div className="optimizer-result">
        {!result && (
          <div className="optimizer-card-result">
            <div className="optimizer-icon">📐</div>
            <div className="optimizer-title">Configura los cortes y presiona <strong>Calcular Optimización</strong></div>
            <div className="optimizer-text">Los resultados aparecerán aquí.</div>
          </div>
        )}

        {result && (
          <>
            {/* Summary metrics */}
            <InventorySummary
                summary={summary}
                result={result}
                totalArea={totalArea}
                fmt={fmt}
            />

            {/* Detail table */}
            <PanelTable result={result} />

            {/* Logística */}
            <Logistica
                logistica={logistica}
                setLogistica={setLogistica}
            />

            {/* Save & Download */}
            <div className="button">
              <button 
              className={`save-button ${saved ? "saved" : ""}`}
              onClick={handleSaveAndDownload} 
              disabled={saved} 
              >
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
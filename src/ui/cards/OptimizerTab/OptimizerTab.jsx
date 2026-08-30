import { useOptimizer } from "../../../application/hooks/useOptimizer";
//CARDS LEFT---------------------------------------------------------------
import PanelTable from "./sections/PanelTable";
import CortesInput from "./sections/CortesInput";
//CARDS RIGHT---------------------------------------------------------------
import Logistica from "./sections/Logistica";
import SectionHeader from "../../components/SectionHeader";
import InventorySummary from "./sections/InventorySummary";

//COMPONENST---------------------------------------------------------------------
import Toast from "../../components/Toast";

//STILOS---------------------------------------------------------------------
import "../../styles/cards/OptimizerTab/OptimizerTab.css"



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
  
  const {
    rows,
    setRow,
    addRow,
    removeRow,
    handleOptimize,
    loading,
    result,
    summary,
    totalArea,
    logistica,
    setLogistica,
    handleSaveAndDownload,
    saved,
    toast,


  } = useOptimizer(form, nextOrden, onOrdenSaved);

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
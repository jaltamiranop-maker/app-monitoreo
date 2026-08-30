import { useHistory } from "../../../application/hooks/useHistory";
//COMPONENST---------------------------------------------------------------------
import SectionHeader from "../../components/SectionHeader";
import Toast from "../../components/Toast";
import Field from "../../components/Field";
import Select from "../../components/Select";


import "../../styles/cards/HistoryTab/HistoryTab.css";



const IconDownload = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
  </svg>
);


export default function HistoryTab() {

  const {
    history,
    loading,
    regenId,
    setRegenId,
    toast,
    setToast,
    handleRegen,
  } = useHistory();

  return (
    <div className="history-tab">
      <div className="history-tab-panel">
        <SectionHeader>Historial de Órdenes</SectionHeader>
        {loading ? (
          <div className="history-tab-loading">Cargando historial...</div>
        ) : history.length === 0 ? (
          <div className="history-tab-loading">
            <div className="history-tab-loading-noresults">📋</div>
            No hay órdenes registradas.
          </div>
        ) : (
          <div className="history-tab-info">
            <table>
              <thead>
                <tr className="history-tab-info-banner">
                  {["N° Orden","Fecha Registro","Cliente","Producto"].map(h => (
                    <th key={h} className="history-tab-info-th">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {history.map((row, i) => (
                  <tr key={i} className={`history-tab-info-tr ${ i % 2 == 0 ? "index" : ""}`}>
                    <td className="history-tab-info-order">#{String(row["N° Orden"]).padStart(4,"0")}</td>
                    <td className="history-tab-info-date">{row["Fecha Registro"]}</td>
                    <td className="history-tab-info-client">{row["Cliente"]}</td>
                    <td className="history-tab-info-product">{row["Producto"]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="history-tab-panel">
        <SectionHeader>Re-descargar Orden</SectionHeader>
        <div className="history-tab-download">
          <Field label="N° de Orden a recuperar">
            <Select value={regenId} onChange={e => setRegenId(e.target.value)} className="history-tab-select-order">
              <option value="">— Selecciona —</option>
              {history.map(r => (
                <option key={r["N° Orden"]} value={r["N° Orden"]}>#{String(r["N° Orden"]).padStart(4,"0")} — {r["Cliente"]}</option>
              ))}
            </Select>
          </Field>
          <button onClick={handleRegen} disabled={!regenId} className={`history-tab-download-button ${ regenId ? "regenId" : ""}`}>
            <IconDownload /> Generar PDF
          </button>
        </div>
      </div>
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  );
}
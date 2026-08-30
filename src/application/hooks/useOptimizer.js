import { useState } from "react";
import { API_BASE, PANEL_SIZES } from "../config/api";
import { 
    optimizeCuts, 
    saveOrder, 
    generatePdf 
} from "../services/optimizeService";

export function useOptimizer(form, nextOrden, onOrdenSaved){

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

    // Summary
    const summary = result ? PANEL_SIZES.map(s => ({ size: s, qty: result.filter(r => r.Tamaño === s).length })) : [];
    const totalArea = result ? result.reduce((acc, row) => {
        return acc + row.Cortes.split(",").reduce((s, c) => s + parseInt(c.trim()), 0);
    }, 0) / 1000 : 0;

    const handleOptimize = async () => {
    if (!validCortes.length) { 
        setToast({ message: "Ingresa al menos un corte válido.", type: "-warning" });
        return; 
        }

    setLoading(true); 
    setResult(null); 
    setSaved(false);

    try {
      const data = await optimizeCuts(validCortes);
      setResult(data);
      setToast({ message: "Optimización completada con éxito.", type: "-success" });

    } catch (error) {
      setToast({ message: `Error: ${error.message}. ¿Está corriendo el backend en ${API_BASE}?`, type: "-error" });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveAndDownload = async () => {
    if (!form.cliente || !form.nit) { setToast({ message: "Completa el nombre del cliente y NIT.", type: "-warning" }); return; }
    if (form.transporte === "Kingspan" && !form.servicio_logistico) { setToast({ message: "Selecciona el servicio logístico.", type: "-warning" }); return; }
    try {
      const payload = { ...form, n_orden: nextOrden, servicio_logistico_tabla: logistica };
      await saveOrder( payload , result);
      setSaved(true);
      onOrdenSaved();
      setToast({ message: `Orden #${String(nextOrden).padStart(4,"0")} guardada.`, type: "-success" });

      // Download PDF
      
      const blob = await generatePdf(payload, result);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url; 
      a.download = `Orden_${String(nextOrden).padStart(4,"0")}_${form.cliente}.pdf`; 
      a.click();
      URL.revokeObjectURL(url);

    } catch (error) {
      setToast({ message: `Error al guardar: ${error.message}`, type: "-error" });
    }

    


  };

  return {
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
    toast
}


}
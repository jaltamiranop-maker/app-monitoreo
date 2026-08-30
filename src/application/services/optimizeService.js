import { API_BASE } from "../config/api";

export async function optimizeCuts(cortesValidos) {

    const res = await fetch(`${API_BASE}/optimizar`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cortes: cortesValidos }),
      });
    
      if (!res.ok){
        throw new Error(`HTTP ${res.status}`)
      }

      return await res.json();
}

export async function saveOrder(payload, result) {

    const res = await fetch(`${API_BASE}/guardar_pedido`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ datos_pdf: payload, resultado: result }),
    });

    if(!res.ok){
        throw new Error(`HTTP ${res.status}`);
    }

    return await res.json();
    
}

export async function generatePdf(payload, result) {

    const pdfRes = await fetch(`${API_BASE}/generar_pdf`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ datos_pdf: payload, resultado: result }),
    });

    if(!pdfRes.ok){
        throw new Error(`HTTP ${pdfRes.status}`);
    }

    return await pdfRes.blob();
}
import { API_BASE } from "../config/api";

export async function getHistory() {
    const res = await fetch(`${API_BASE}/historial`);

    if (!res.ok){
        throw new Error("No se udo obtener el historial");
    }

    return await res.json();
}

export async function regeneratePDF(orderId){
    const res = await fetch(`${API_BASE}/regenerar_pdf/${orderId}`, { method: "POST" });

    if (!res.ok){
        throw new Error("Orden no encontrada");
    }

    return await res.blob();
}
import { API_BASE } from "../config/api";

export async function getNextOrder() {

    const res = await fetch(`${API_BASE}/siguiente_orden`);

    return res.json();
}
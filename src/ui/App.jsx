import { useState, useEffect, useRef } from "react";
import Field from "./components/Field";
import Input from "./components/Input";
import Select from "./components/Select";
// ─── CONSTANTS ───────────────────────────────────────────────────────────────
const API_BASE = "http://127.0.0.1:8000";
const PANEL_SIZES = [12000, 9000, 6000, 3000];

const COMERCIALES = [
  "ALTAMIRANO PUENTES YAZMIN","ARENAS GUZMAN DIEGO FERNANDO","ARIAS GIRALDO ANA ISABEL",
  "BENAVIDES MARQUEZ JULIO ALBERTO","CALDERON DIEGO","CANDELA YOLANDA",
  "GARCIA RUIZ MONICA ALEXANDRA","GIRALDO ALZATE LINA MARCELA","GUERRERO JULIO",
  "LOZANO TENORIO MARIA CAROLINA","MOJICA MONTALVO JESUS DAVID","NARANJO ALEXIS",
  "PEREZ JOHANA","QUINTANA BARRIOS JAIRO ALONSO","SALAZAR EDWAR","VALENZUELA RONALD",
];

const PRODUCTOS = [
  "KINGFRIGO PIR100 CAL28-9002/CAL28-9002","KINGFRIGO PIR80 CAL28-9002/CAL28-9002",
  "KINGFRIGO PIR40 CAL28-9002/CAL28-9002","KINGROOF PIR30 CAL28-9002/CAL28-9002",
  "KINGROOF PIR18 CAL28-9002/CAL28-9002","KINGROOF PIR15 CAL28-9002/CAL28-9002",
];

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

// ─── COMPONENTS ───────────────────────────────────────────────────────────────


function SectionHeader({ children }) {
  return (
    <div style={{
      fontSize: 10, fontWeight: 800, letterSpacing: "0.12em", textTransform: "uppercase",
      color: "var(--blue)", borderBottom: "2px solid var(--blue)", paddingBottom: 6, marginBottom: 12
    }}>
      {children}
    </div>
  );
}

function Toast({ message, type, onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 3500);
    return () => clearTimeout(t);
  }, []);
  const bg = type === "success" ? "#16a34a" : type === "error" ? "#dc2626" : "#d97706";
  return (
    <div style={{
      position: "fixed", bottom: 24, right: 24, zIndex: 9999,
      background: bg, color: "#fff", borderRadius: 8, padding: "12px 20px",
      fontSize: 13, fontWeight: 600, boxShadow: "0 8px 32px rgba(0,0,0,0.25)",
      display: "flex", alignItems: "center", gap: 10,
      animation: "slideUp 0.3s ease"
    }}>
      {type === "success" && <IconCheck />}
      {message}
    </div>
  );
}

// Panel visualizer bar
function PanelBar({ panel }) {
  const cuts = panel.Cortes.split(",").map(s => parseInt(s.trim()));
  const total = panel.Tamaño;
  const colors = ["#003B8E","#1a56b0","#2e6fd4","#4a85e0","#6699e8"];
  return (
    <div style={{ display: "flex", height: 28, borderRadius: 6, overflow: "hidden", border: "1px solid var(--border)", marginTop: 4 }}>
      {cuts.map((c, i) => (
        <div key={i} title={`${c} mm`} style={{
          width: `${(c / total) * 100}%`, background: colors[i % colors.length],
          borderRight: i < cuts.length - 1 ? "1px solid rgba(255,255,255,0.3)" : "none",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 9, color: "#fff", fontWeight: 700, overflow: "hidden", whiteSpace: "nowrap"
        }}>
          {c >= 800 ? `${c}` : ""}
        </div>
      ))}
      {panel.Desperdicio > 0 && (
        <div title={`Desperdicio: ${panel.Desperdicio} mm`} style={{
          flexGrow: 1, background: "repeating-linear-gradient(45deg, #f3f4f6, #f3f4f6 4px, #e5e7eb 4px, #e5e7eb 8px)",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 9, color: "#9ca3af", fontWeight: 600
        }}>
          {panel.Desperdicio > 500 ? `~${panel.Desperdicio}mm` : ""}
        </div>
      )}
    </div>
  );
}

// ─── SIDEBAR FORM ─────────────────────────────────────────────────────────────
function SidebarForm({ form, setForm, nextOrden }) {
  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20, padding: "0 0 24px" }}>
      {/* Orden info */}
      <div>
        <SectionHeader>Información de la Orden</SectionHeader>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <Field label="Fecha de Despiece">
            <Input type="date" value={form.f_despiece} onChange={set("f_despiece")} />
          </Field>
          <Field label="N° de Orden">
            <div style={{
              background: "var(--blue)", color: "#fff", borderRadius: 6, padding: "8px 11px",
              fontSize: 13, fontWeight: 700, letterSpacing: "0.05em"
            }}>
              #{String(nextOrden).padStart(4, "0")}
            </div>
          </Field>
          <Field label="Comercial Asignado">
            <Select value={form.comercial} onChange={set("comercial")}>
              <option value="">— Escoge Asesor —</option>
              {COMERCIALES.map(c => <option key={c} value={c}>{c}</option>)}
            </Select>
          </Field>
          <Field label="Orden de Compra">
            <Input placeholder="OC-00000" value={form.orden_compra} onChange={set("orden_compra")} />
          </Field>
        </div>
      </div>

      {/* Cliente */}
      <div>
        <SectionHeader>Datos del Cliente</SectionHeader>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {[["cliente","Nombre del Cliente","Empresa S.A.S",true],
            ["nit","NIT","900.000.000-0",true],
            ["contacto","Contacto de Obra","Nombre Apellido"],
            ["telefono","Teléfono","310 000 0000"],
            ["correo","Correo Electrónico","correo@empresa.com"],
          ].map(([k, label, ph, req]) => (
            <Field key={k} label={label} required={req}>
              <Input placeholder={ph} value={form[k]} onChange={set(k)} />
            </Field>
          ))}
        </div>
      </div>

      {/* Logística */}
      <div>
        <SectionHeader>Logística y Entrega</SectionHeader>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <Field label="Sector">
            <Input placeholder="Sector industrial..." value={form.sector} onChange={set("sector")} />
          </Field>
          <Field label="Mercado Final">
            <Select value={form.mercado} onChange={set("mercado")}>
              <option value="">— Escoge mercado —</option>
              <option>Nuevo</option><option>Remodelación</option>
            </Select>
          </Field>
          <Field label="Canal de Venta">
            <Select value={form.canal} onChange={set("canal")}>
              <option value="">— Escoge canal —</option>
              <option>Cliente final</option><option>Distribuidor</option>
            </Select>
          </Field>
          <Field label="Tipo Destino">
            <Select value={form.tipo_destino} onChange={set("tipo_destino")}>
              <option value="">— Escoge una opción —</option>
              <option>Venta con IVA</option><option>Exportación</option>
            </Select>
          </Field>
          <Field label="Transporte">
            <Select value={form.transporte} onChange={set("transporte")}>
              <option value="">— Escoge una opción —</option>
              <option>Kingspan</option><option>Cliente</option>
            </Select>
          </Field>
          {form.transporte === "Kingspan" && (
            <>
              <Field label="Servicio Logístico">
                <Select value={form.servicio_logistico} onChange={set("servicio_logistico")}>
                  <option value="">— Escoge una opción —</option>
                  <option>MINIMULA</option><option>SENCILLO</option><option>TURBO</option>
                </Select>
              </Field>
              <Field label="Ciudad de Entrega">
                <Input placeholder="Ciudad..." value={form.ciudad} onChange={set("ciudad")} />
              </Field>
            </>
          )}
          <Field label="Dirección de Entrega">
            <Input placeholder="Calle / Carrera..." value={form.direccion} onChange={set("direccion")} />
          </Field>
          <Field label="Fecha de Entrega">
            <Input type="date" value={form.f_entrega} onChange={set("f_entrega")} />
          </Field>
        </div>
      </div>

      {/* Producto */}
      <div>
        <SectionHeader>Producto y Kit</SectionHeader>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <Field label="Producto">
            <Select value={form.producto} onChange={set("producto")}>
              <option value="">— Escoge un producto —</option>
              {PRODUCTOS.map(p => <option key={p} value={p}>{p}</option>)}
            </Select>
          </Field>
          <Field label="Kit de Anclaje">
            <Select value={form.kit} onChange={set("kit")}>
              <option value="">— Escoge una cubierta —</option>
              <option>Cubierta 30</option><option>Cubierta 18</option>
              <option>Metalroof</option><option>Otro</option>
            </Select>
          </Field>
          <Field label="Cantidad de Kits">
            <Input type="number" min="0" value={form.cantidad_kit} onChange={set("cantidad_kit")} />
          </Field>
        </div>
      </div>
    </div>
  );
}

// ─── OPTIMIZER TAB ────────────────────────────────────────────────────────────
function OptimizerTab({ form, nextOrden, onOrdenSaved }) {
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
    if (!validCortes.length) { setToast({ message: "Ingresa al menos un corte válido.", type: "warning" }); return; }
    setLoading(true); setResult(null); setSaved(false);
    try {
      const res = await fetch(`${API_BASE}/optimizar`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cortes: validCortes }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setResult(await res.json());
      setToast({ message: "Optimización completada con éxito.", type: "success" });
    } catch (e) {
      setToast({ message: `Error: ${e.message}. ¿Está corriendo el backend en ${API_BASE}?`, type: "error" });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveAndDownload = async () => {
    if (!form.cliente || !form.nit) { setToast({ message: "Completa el nombre del cliente y NIT.", type: "warning" }); return; }
    if (form.transporte === "Kingspan" && !form.servicio_logistico) { setToast({ message: "Selecciona el servicio logístico.", type: "warning" }); return; }
    try {
      const payload = { ...form, n_orden: nextOrden, servicio_logistico_tabla: logistica };
      const res = await fetch(`${API_BASE}/guardar_pedido`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ datos_pdf: payload, resultado: result }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setSaved(true);
      onOrdenSaved();
      setToast({ message: `Orden #${String(nextOrden).padStart(4,"0")} guardada.`, type: "success" });
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
      setToast({ message: `Error al guardar: ${e.message}`, type: "error" });
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
        <div style={{
          background: "var(--card)", border: "1px solid var(--border)", borderRadius: 12,
          padding: 20, boxShadow: "0 2px 12px rgba(0,0,0,0.06)"
        }}>
          <SectionHeader>Parámetros de Corte</SectionHeader>
          <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 14 }}>
            {rows.map((row, i) => (
              <div key={i} style={{ display: "grid", gridTemplateColumns: "1fr 80px 36px", gap: 6, alignItems: "end" }}>
                <Field label={i === 0 ? "Longitud (mm)" : ""}>
                  <Input type="number" min="0" placeholder="p.ej. 2400" value={row.longitud}
                    onChange={e => setRow(i, "longitud", e.target.value)} />
                </Field>
                <Field label={i === 0 ? "Cant." : ""}>
                  <Input type="number" min="0" placeholder="1" value={row.cantidad}
                    onChange={e => setRow(i, "cantidad", e.target.value)} />
                </Field>
                <button onClick={() => removeRow(i)} disabled={rows.length === 1}
                  style={{
                    background: "none", border: "1.5px solid var(--border)", borderRadius: 6,
                    color: "var(--text-muted)", cursor: "pointer", padding: "7px 6px",
                    opacity: rows.length === 1 ? 0.3 : 1
                  }}>
                  <IconTrash />
                </button>
              </div>
            ))}
          </div>
          <button onClick={addRow} style={{
            width: "100%", background: "none", border: "1.5px dashed var(--border)",
            borderRadius: 6, color: "var(--text-muted)", cursor: "pointer", padding: "7px",
            fontSize: 12, fontWeight: 600, display: "flex", alignItems: "center", justifyContent: "center", gap: 6,
            marginBottom: 16
          }}>
            <IconPlus /> Agregar tipo de corte
          </button>
          <button onClick={handleOptimize} disabled={loading} style={{
            width: "100%", background: loading ? "#6b8fc7" : "var(--blue)",
            color: "#fff", border: "none", borderRadius: 8, padding: "11px",
            fontSize: 14, fontWeight: 800, cursor: loading ? "not-allowed" : "pointer",
            letterSpacing: "0.04em", transition: "background 0.2s",
            display: "flex", alignItems: "center", justifyContent: "center", gap: 8
          }}>
            {loading ? (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" style={{ animation: "spin 1s linear infinite" }}>
                  <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
                </svg>
                Calculando...
              </>
            ) : (<><IconCut /> Calcular Optimización</>)}
          </button>
        </div>
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
      setToast({ message: `PDF de la orden #${regenId} descargado.`, type: "success" });
    } catch (e) {
      setToast({ message: `Error: ${e.message}`, type: "error" });
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

import FormSection from "./FormSection";
import Field from "../../components/Field";
import Input from "../../components/Input";
import Select from "../../components/Select";


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
export default function SidebarForm({ form, setForm, nextOrden }) {
  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20, padding: "0 0 24px" }}>
      {/* Orden info */}
      <FormSection title={"Información de la Orden"}>
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
      </FormSection>

      

      {/* Cliente */}
      <FormSection title={"Datos del Cliente"}>
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

      </FormSection>
      
      {/* Logística */}
      <FormSection title={"Logística y Entrega"}>
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

      </FormSection>
      

      {/* Producto */}
      <FormSection title={"Producto y Kit"}>
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

      </FormSection>
      
    </div>
  );
}
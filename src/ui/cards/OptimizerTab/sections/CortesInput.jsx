import Field from "../../../components/Field";
import Input from "../../../components/Input";
import SectionHeader from "../../../components/SectionHeader";


import "../../../styles/cards/OptimizerTab/sections/CortesInput.css";

export default function CortesInput({
    rows,
    setRow,
    addRow,
    removeRow,
    handleOptimize,
    loading,
}) {
    const IconPlus = () => (
   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
    );
    const IconTrash = () => (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
    </svg>
    );
    const IconCut = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/>
        <line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/>
        <line x1="8.12" y1="8.12" x2="12" y2="12"/>
    </svg>
    );

    return (

        <div className="card">

            <SectionHeader>
                Parámetros de Corte
            </SectionHeader>

            <div className="cut-list">

                {rows.map((row, i) => (

                    <div
                        key={i}
                        className="cut-row"
                    >

                        <Field label={i === 0 ? "Longitud (mm)" : ""}>

                            <Input
                                type="number"
                                min="0"
                                placeholder="p.ej. 2400"
                                value={row.longitud}
                                onChange={(e) =>
                                    setRow(i, "longitud", e.target.value)
                                }
                            />

                        </Field>

                        <Field label={i === 0 ? "Cant." : ""}>

                            <Input
                                type="number"
                                min="0"
                                placeholder="1"
                                value={row.cantidad}
                                onChange={(e) =>
                                    setRow(i, "cantidad", e.target.value)
                                }
                            />

                        </Field>

                        <button
                            className="card remove-button"
                            onClick={() => removeRow(i)}
                            disabled={rows.length === 1}
                        >

                            <IconTrash />

                        </button>

                    </div>

                ))}

            </div>

            <button
                className="add-button"
                onClick={addRow}
            >

                <IconPlus />

                Agregar tipo de corte

            </button>

            <button
                className={`optimize-button ${loading ? "loading" : ""}`}
                onClick={handleOptimize}
                disabled={loading}
            >

                {loading ? (
                    <>
                        <svg
                            className="spinner"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2.5"
                        >
                            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                        </svg>

                        Calculando...

                    </>
                ) : (
                    <>
                        <IconCut />

                        Calcular Optimización
                    </>
                )}

            </button>

        </div>

    );

}
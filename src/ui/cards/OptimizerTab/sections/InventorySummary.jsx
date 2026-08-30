import SectionHeader from "../../../components/SectionHeader";
import "../../../styles/cards/OptimizerTab/sections/InventorySummary.css"
export default function InventorySummary({ summary, result, totalArea, fmt }) {
    return (
        <div className="inventory-card">
            <SectionHeader>Resumen de Inventario</SectionHeader>

            <div className="inventory-panels">
                {summary.map((item) => (
                    <div
                        key={item.size}
                        className={`inventory-panel ${
                            item.qty > 0 ? "active" : ""
                        }`}
                    >
                        <div className="inventory-qty">
                            {item.qty}
                        </div>

                        <div className="inventory-size">
                            {fmt(item.size)} mm
                        </div>
                    </div>
                ))}
            </div>

            <div className="inventory-metrics">
                {[
                    ["Paneles Totales", result.length],
                    ["Área Total", `${totalArea.toFixed(2)} m²`],
                    [
                        "Desperdicio Total",
                        `${result.reduce(
                            (acc, row) => acc + row.Desperdicio,
                            0
                        )} mm`,
                    ],
                ].map(([label, value]) => (
                    <div key={label} className="inventory-metric">
                        <div className="inventory-label">
                            {label}
                        </div>

                        <div className="inventory-value">
                            {value}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
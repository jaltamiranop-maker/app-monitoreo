import PanelBar from "../../PanelBar";
import SectionHeader from "../../../components/SectionHeader";
import "../../../styles/cards/OptimizerTab/sections/PanelTable.css"

const fmt = (n) => new Intl.NumberFormat("es-CO").format(n);

export default function PanelTable({ result }) {
    return (
        <div className="panel-table-card">
            <SectionHeader>Detalle por Panel</SectionHeader>

            <div className="table-container">
                <table className="panel-table">
                    <thead>
                        <tr>
                            {[
                                "Panel",
                                "Tamaño (mm)",
                                "Cortes",
                                "Desperdicio (mm)",
                                "Distribución Visual",
                            ].map((h) => (
                                <th key={h}>{h}</th>
                            ))}
                        </tr>
                    </thead>

                    <tbody>
                        {result.map((row, i) => (
                            <tr
                                key={i}
                                className={i % 2 === 0 ? "" : "alternate-row"}
                            >
                                <td className="panel-id">
                                    {row.Panel}
                                </td>

                                <td className="panel-size">
                                    {fmt(row.Tamaño)}
                                </td>

                                <td className="panel-cuts">
                                    {row.Cortes}
                                </td>

                                <td
                                    className={`waste ${
                                        row.Desperdicio > 1000
                                            ? "high"
                                            : row.Desperdicio > 200
                                            ? "medium"
                                            : "low"
                                    }`}
                                >
                                    {fmt(row.Desperdicio)}
                                </td>

                                <td className="panelTable-bar">
                                    <PanelBar panel={row} />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
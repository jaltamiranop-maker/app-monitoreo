import "../../../styles/cards/OptimizerTab/sections/Logistica.css"
import SectionHeader from "../../../components/SectionHeader";
import Input from "../../../components/Input";

export default function Logistica({ logistica, setLogistica }) {
    return (
        <div className="logistica-card">
            <SectionHeader>Servicio Logístico</SectionHeader>

            <table className="logistica-table">
                <thead>
                    <tr>
                        {["Concepto", "Tipo", "Cantidad", "COP $"].map((h) => (
                            <th key={h}>{h}</th>
                        ))}
                    </tr>
                </thead>

                <tbody>
                    {logistica.map((item, i) => (
                        <tr key={i}>
                            <td className="concepto">
                                {item.Concepto}
                            </td>

                            <td>
                                <Input
                                    value={item.Tipo}
                                    onChange={(e) =>
                                        setLogistica((l) =>
                                            l.map((x, idx) =>
                                                idx === i
                                                    ? { ...x, Tipo: e.target.value }
                                                    : x
                                            )
                                        )
                                    }
                                    style={{ padding: "5px 8px", fontSize: 12 }}
                                />
                            </td>

                            <td>
                                <Input
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    value={item.Cantidad}
                                    onChange={(e) =>
                                        setLogistica((l) =>
                                            l.map((x, idx) =>
                                                idx === i
                                                    ? {
                                                          ...x,
                                                          Cantidad:
                                                              parseFloat(e.target.value) || 0,
                                                      }
                                                    : x
                                            )
                                        )
                                    }
                                    style={{
                                        padding: "5px 8px",
                                        fontSize: 12,
                                        width: 80,
                                    }}
                                />
                            </td>

                            <td>
                                <Input
                                    type="number"
                                    min="0"
                                    step="50000"
                                    value={item.Precio_COP}
                                    onChange={(e) =>
                                        setLogistica((l) =>
                                            l.map((x, idx) =>
                                                idx === i
                                                    ? {
                                                          ...x,
                                                          Precio_COP:
                                                              parseInt(e.target.value) || 0,
                                                      }
                                                    : x
                                            )
                                        )
                                    }
                                    style={{
                                        padding: "5px 8px",
                                        fontSize: 12,
                                        width: 120,
                                    }}
                                />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
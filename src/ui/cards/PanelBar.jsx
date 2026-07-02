import "../styles/cards/PanelBar.css";

const colors = [
    "#003B8E",
    "#1a56b0",
    "#2e6fd4",
    "#4a85e0",
    "#6699e8"
];

function PanelBar({ panel }) {

    const cuts = panel.Cortes
        .split(",")
        .map(c => parseInt(c.trim()));

    const total = panel.Tamaño;

    return (

        <div className="panel-bar">

            {cuts.map((cut, index) => (

                <div
                    key={index}
                    className="panel-piece"
                    title={`${cut} mm`}
                    style={{
                        width: `${(cut / total) * 100}%`,
                        background: colors[index % colors.length],
                        borderRight:
                            index < cuts.length - 1
                                ? "1px solid rgba(255,255,255,.3)"
                                : "none"
                    }}
                >

                    {cut >= 800 && cut}

                </div>

            ))}

            {panel.Desperdicio > 0 && (

                <div
                    className="panel-waste"
                    title={`Desperdicio: ${panel.Desperdicio} mm`}
                >

                    {panel.Desperdicio > 500 &&
                        `~${panel.Desperdicio} mm`}

                </div>

            )}

        </div>

    );

}

export default PanelBar;
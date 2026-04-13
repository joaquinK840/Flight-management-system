import Btn from "../components/Btn";
import Card from "../components/Card";
import { C, gCardTitle } from "../theme";

export default function MetricsSection({ metrics, refreshMetrics }) {
  if (!metrics) return <div style={{ color: C.textMuted, textAlign: "center", padding: "60px" }}>Carga un árbol para ver las métricas</div>;

  const cards = [
    { l: "Altura AVL", v: metrics.height ?? 0, s: "niveles", c: C.accentLt, b: C.accentDim, bdr: C.accentBdr },
    { l: "Total nodos", v: metrics.total_nodes ?? 0, s: "vuelos", c: C.green, b: C.greenDim, bdr: C.greenBdr },
    { l: "Hojas", v: metrics.leaves ?? 0, s: "terminales", c: C.violet, b: C.violetDim, bdr: C.violetBdr },
    { l: "Rot. LL", v: metrics.rotations?.ll ?? 0, s: "izq-izq", c: C.amber, b: C.amberDim, bdr: C.amberBdr },
    { l: "Rot. LR", v: metrics.rotations?.lr ?? 0, s: "izq-der", c: C.teal, b: C.tealDim, bdr: C.tealBdr },
    { l: "Rot. RR", v: metrics.rotations?.rr ?? 0, s: "der-der", c: C.red, b: C.redDim, bdr: C.redBdr }
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(6,minmax(0,1fr))", gap: "10px" }}>
        {cards.map((c) => (
          <div key={c.l} style={{ background: c.b, border: `1px solid ${c.bdr}`, borderRadius: "11px", padding: "14px 12px" }}>
            <div style={{ fontSize: "9px", color: C.textMuted, fontWeight: 700, letterSpacing: ".8px", marginBottom: "8px", textTransform: "uppercase" }}>{c.l}</div>
            <div style={{ fontSize: "26px", fontWeight: 700, color: c.c, lineHeight: 1 }}>{c.v}</div>
            <div style={{ fontSize: "10px", color: C.textMuted, marginTop: "5px" }}>{c.s}</div>
          </div>
        ))}
      </div>
      <Card
        header={
          <>
            <h3 style={gCardTitle}>Recorridos del sistema</h3>
            <Btn color={C.textSub} bg={C.surface3} border={C.border2} onClick={refreshMetrics}>Actualizar</Btn>
          </>
        }
      >
        {metrics.traversals ? (
          <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
            {Object.entries(metrics.traversals).map(([k, v]) => (
              <div key={k}>
                <div style={{ fontSize: "10px", color: C.textMuted, fontWeight: 700, letterSpacing: ".8px", marginBottom: "6px", textTransform: "uppercase" }}>{k}</div>
                <div
                  style={{
                    fontFamily: "monospace",
                    fontSize: "11px",
                    background: C.surface2,
                    border: `1px solid ${C.border}`,
                    padding: "10px",
                    borderRadius: "8px",
                    overflowX: "auto",
                    whiteSpace: "nowrap",
                    color: C.accentLt
                  }}
                >
                  {Array.isArray(v) ? v.join(" → ") : v}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ color: C.textMuted, fontSize: "12px" }}>Sin datos de recorrido disponibles</div>
        )}
      </Card>
    </div>
  );
}

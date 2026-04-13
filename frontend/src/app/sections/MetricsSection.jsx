import Btn from "../components/Btn";
import Card from "../components/Card";
import { C, gCardTitle } from "../theme";

export default function MetricsSection({ metrics, refreshMetrics }) {
  if (!metrics) return <div style={{ color: C.textMuted, textAlign: "center", padding: "60px" }}>Carga un árbol para ver las métricas</div>;

  const cards = [
    { l: "Altura AVL", v: metrics.height ?? 0, s: "niveles", c: C.accentLt, b: C.accentDim, bdr: C.accentBdr },
    { l: "Total nodos", v: metrics.total_nodes ?? 0, s: "vuelos", c: C.green, b: C.greenDim, bdr: C.greenBdr },
    { l: "Hojas", v: metrics.leaves ?? 0, s: "terminales", c: C.violet, b: C.violetDim, bdr: C.violetBdr },
    { l: "Rot. LL", v: metrics.rotation_counts?.LL ?? 0, s: "izq-izq", c: C.amber, b: C.amberDim, bdr: C.amberBdr },
    { l: "Rot. LR", v: metrics.rotation_counts?.LR ?? 0, s: "izq-der", c: C.teal, b: C.tealDim, bdr: C.tealBdr },
    { l: "Rot. RR", v: metrics.rotation_counts?.RR ?? 0, s: "der-der", c: C.red, b: C.redDim, bdr: C.redBdr },
    { l: "Rot. RL", v: metrics.rotation_counts?.RL ?? 0, s: "der-izq", c: C.violet, b: C.violetDim, bdr: C.violetBdr },
    { l: "Canc. masivas", v: metrics.mass_cancellations ?? 0, s: "eventos", c: C.accentLt, b: C.accentDim, bdr: C.accentBdr }
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))", gap: "14px" }}>
        {cards.map((c) => (
            <div key={c.l} style={{ background: c.b, border: `1px solid ${c.bdr}`, borderRadius: "12px", padding: "18px 16px" }}>
            <div style={{ fontSize: "9px", color: C.textMuted, fontWeight: 700, letterSpacing: ".8px", marginBottom: "8px", textTransform: "uppercase" }}>{c.l}</div>
            <div style={{ fontSize: "26px", fontWeight: 700, color: c.c, lineHeight: 1 }}>{c.v}</div>
            <div style={{ fontSize: "10px", color: C.textMuted, marginTop: "5px" }}>{c.s}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

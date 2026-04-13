import Card from "../components/Card";
import { C, gCardTitle } from "../theme";

export default function TraversalSection({ onTraversal }) {
  const opts = [
    { k: "pre", label: "Preorden", desc: "Raíz → Izquierda → Derecha", c: C.green, b: C.greenDim, bdr: C.greenBdr },
    { k: "in", label: "Inorden", desc: "Izquierda → Raíz → Derecha", c: C.accentLt, b: C.accentDim, bdr: C.accentBdr },
    { k: "post", label: "Postorden", desc: "Izquierda → Derecha → Raíz", c: C.amber, b: C.amberDim, bdr: C.amberBdr },
    { k: "level", label: "Por niveles", desc: "BFS nivel por nivel", c: C.violet, b: C.violetDim, bdr: C.violetBdr }
  ];

  return (
    <Card header={<h3 style={gCardTitle}>Recorridos del árbol</h3>}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,minmax(0,1fr))", gap: "12px" }}>
        {opts.map((o) => (
          <button
            key={o.k}
            onClick={() => onTraversal(o.k)}
            style={{
              padding: "18px 14px",
              background: o.b,
              border: `1px solid ${o.bdr}`,
              borderRadius: "10px",
              textAlign: "left",
              cursor: "pointer",
              fontFamily: "inherit"
            }}
          >
            <div style={{ fontWeight: 700, fontSize: "13px", color: o.c, marginBottom: "5px" }}>{o.label}</div>
            <div style={{ fontSize: "11px", color: C.textMuted, lineHeight: "1.5" }}>{o.desc}</div>
          </button>
        ))}
      </div>
    </Card>
  );
}

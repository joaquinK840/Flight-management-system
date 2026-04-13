import Card from "../components/Card";
import Pill from "../components/Pill";
import { C, gCardTitle } from "../theme";

export default function TraversalSection({ onTraversal, traversalResult, traversalMode }) {
  const opts = [
    { k: "pre", label: "Preorden", desc: "Raíz → Izquierda → Derecha", c: C.green, b: C.greenDim, bdr: C.greenBdr },
    { k: "in", label: "Inorden", desc: "Izquierda → Raíz → Derecha", c: C.accentLt, b: C.accentDim, bdr: C.accentBdr },
    { k: "post", label: "Postorden", desc: "Izquierda → Derecha → Raíz", c: C.amber, b: C.amberDim, bdr: C.amberBdr },
    { k: "bfs", label: "Anchura", desc: "Recorrido en anchura (BFS)", c: C.accentLt, b: C.accentDim, bdr: C.accentBdr },
    { k: "depth", label: "Profundidad", desc: "Recorrido en profundidad (DFS)", c: C.green, b: C.greenDim, bdr: C.greenBdr }
  ];

  const tl = { pre: "Preorden", in: "Inorden", post: "Postorden", bfs: "Anchura", depth: "Profundidad" };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
      <Card header={<h3 style={gCardTitle}>Recorridos del árbol</h3>}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))", gap: "12px" }}>
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
      {traversalResult && (
        <Card
          header={
            <>
              <h3 style={gCardTitle}>Recorrido {tl[traversalMode] || traversalMode}</h3>
              <Pill text={`${Array.isArray(traversalResult) ? traversalResult.length : 0} nodos`} color={C.textSub} bg={C.surface3} border={C.border2} />
            </>
          }
        >
          <div
            style={{
              fontFamily: "monospace",
              fontSize: "11px",
              background: C.surface2,
              border: `1px solid ${C.border}`,
              padding: "12px",
              borderRadius: "8px",
              overflowX: "auto",
              whiteSpace: "nowrap",
              color: C.accentLt,
              letterSpacing: ".3px"
            }}
          >
            {Array.isArray(traversalResult)
              ? traversalResult.join(" → ")
              : (typeof traversalResult === "string" || typeof traversalResult === "number")
                ? traversalResult
                : (traversalResult?.detail || "Sin datos")}
          </div>
        </Card>
      )}
    </div>
  );
}

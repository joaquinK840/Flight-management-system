import { useMemo } from "react";
import Card from "./Card";
import Pill from "./Pill";
import { C, gCardTitle } from "../theme";

function AVLNode({ node, isRoot }) {
  if (!node) return null;
  const crit = node.nodoCritico;
  const bg = crit ? C.redDim : isRoot ? C.accentDim : C.surface3;
  const bd = crit ? C.red : isRoot ? C.accentBdr : C.border2;
  const cc = crit ? C.red : isRoot ? C.accentLt : "#c5d5ee";
  const bal = node.balance_factor ?? node.balance ?? 0;

  return (
    <div
      title={`Código: ${node.codigo}\nRuta: ${node.origen ?? ""}→${node.destino ?? ""}\nPasajeros: ${node.pasajeros ?? 0}\nPrecio: $${node.precioFinal ?? 0}\nBalance: ${bal}`}
      style={{
        display: "inline-flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "10px 14px",
        background: bg,
        border: `1px solid ${bd}`,
        borderRadius: "10px",
        minWidth: "96px",
        cursor: "default",
        transition: "transform .12s"
      }}
      onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.05)")}
      onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
    >
      <div style={{ fontSize: "12px", fontWeight: 700, color: cc, letterSpacing: ".4px" }}>
        {crit && <span style={{ color: C.red }}>⚠ </span>}
        {node.codigo}
      </div>
      {node.origen && node.destino && (
        <div style={{ fontSize: "10px", color: C.textMuted, marginTop: "3px" }}>
          {node.origen} → {node.destino}
        </div>
      )}
      <div style={{ fontSize: "9px", color: C.textMuted, marginTop: "4px", fontFamily: "monospace" }}>
        bal:{bal}
      </div>
    </div>
  );
}

export default function TreeView({ tree, title, showBst }) {
  const countNodes = (n) => (!n ? 0 : 1 + countNodes(n.left) + countNodes(n.right));
  const getLevels = (root, maxD) => {
    if (!root) return [];
    const lvls = [];
    const q = [{ n: root, d: 0 }];
    while (q.length) {
      const { n, d } = q.shift();
      if (d > maxD) continue;
      if (!lvls[d]) lvls[d] = [];
      lvls[d].push(n);
      if (n.left) q.push({ n: n.left, d: d + 1 });
      if (n.right) q.push({ n: n.right, d: d + 1 });
    }
    return lvls;
  };

  const { total, levels } = useMemo(() => {
    const t = countNodes(tree);
    return { total: t, levels: getLevels(tree, t > 15 ? 4 : Infinity) };
  }, [tree]);

  return (
    <Card
      header={
        <>
          <h3 style={gCardTitle}>{title}</h3>
          <div style={{ display: "flex", gap: "8px" }}>
            {showBst && (
              <Pill text="Sin balanceo" color={C.amber} bg={C.amberDim} border={C.amberBdr} />
            )}
            <Pill text={`${total} nodos`} color={C.textSub} bg={C.surface3} border={C.border2} />
          </div>
        </>
      }
    >
      {!tree ? (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "60px 20px", color: C.textMuted }}>
          <div style={{ fontSize: "13px", fontWeight: 600, color: C.textSub, marginBottom: "8px" }}>Árbol vacío</div>
          <div style={{ fontSize: "12px", textAlign: "center", maxWidth: "240px" }}>
            Carga un archivo JSON o inserta vuelos manualmente para comenzar
          </div>
        </div>
      ) : (
        <div style={{ overflowX: "auto", maxHeight: "520px", overflowY: "auto", paddingBottom: "4px" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: "18px", alignItems: "center", minWidth: total > 10 ? "780px" : "auto" }}>
            {levels.map((lvl, li) => (
              <div key={li} style={{ display: "flex", flexDirection: "column", alignItems: "center", width: "100%" }}>
                <div style={{ fontSize: "9px", color: C.textMuted, marginBottom: "6px", fontWeight: 600, letterSpacing: "1px" }}>
                  NIVEL {li}
                </div>
                <div style={{ display: "flex", gap: "10px", justifyContent: "center", flexWrap: "wrap" }}>
                  {lvl.map((n, i) => (
                    <AVLNode key={`${n.codigo ?? n.value}-${i}`} node={n} isRoot={li === 0} />
                  ))}
                </div>
                {li < levels.length - 1 && <div style={{ marginTop: "8px", color: C.border2, fontSize: "18px" }}>↓</div>}
              </div>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}

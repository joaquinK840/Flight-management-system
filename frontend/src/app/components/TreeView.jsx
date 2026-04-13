import { useLayoutEffect, useMemo, useRef, useState } from "react";
import Card from "./Card";
import Pill from "./Pill";
import { C, gCardTitle } from "../theme";

function AVLNode({ node, isRoot, onHover, onMount }) {
  if (!node) return null;
  const crit = node.nodoCritico;
  const bg = crit ? C.redDim : isRoot ? C.accentDim : C.surface3;
  const bd = crit ? C.red : isRoot ? C.accentBdr : C.border2;
  const cc = crit ? C.red : isRoot ? C.accentLt : "#c5d5ee";
  const codigo = node.codigo ?? node.value ?? "-";

  return (
    <div
      ref={(el) => onMount?.(node, el)}
      style={{
        display: "inline-flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "6px 8px",
        background: bg,
        border: `1px solid ${bd}`,
        borderRadius: "10px",
        minWidth: "44px",
        cursor: "default",
        transition: "transform .12s",
        position: "relative"
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "scale(1.05)";
        onHover?.(node);
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "scale(1)";
        onHover?.(null);
      }}
    >
      <div style={{ fontSize: "11px", fontWeight: 700, color: cc, letterSpacing: ".3px" }}>
        {crit && <span style={{ color: C.red }}>⚠ </span>}
        {codigo}
      </div>
    </div>
  );
}

export default function TreeView({ tree, title, showBst }) {
  const [hoveredNode, setHoveredNode] = useState(null);
  const [lines, setLines] = useState([]);
  const containerRef = useRef(null);
  const nodeRefs = useRef(new Map());
  const NODE_WIDTH = 52;
  const NODE_GAP = 16;
  const LEVEL_GAP_STEP = 10;
  const countNodes = (n) => (!n ? 0 : 1 + countNodes(n.left) + countNodes(n.right));
  const getLevels = (root, maxD) => {
    if (!root) return [];
    const lvls = [];
    const q = [{ n: root, d: 0, i: 0 }];
    while (q.length) {
      const { n, d, i } = q.shift();
      if (d > maxD) continue;
      if (!lvls[d]) lvls[d] = Array(2 ** d).fill(null);
      lvls[d][i] = n;
      if (n.left) q.push({ n: n.left, d: d + 1, i: i * 2 });
      if (n.right) q.push({ n: n.right, d: d + 1, i: i * 2 + 1 });
    }
    return lvls;
  };

  const { total, levels } = useMemo(() => {
    nodeRefs.current = new Map();
    const t = countNodes(tree);
    return { total: t, levels: getLevels(tree, t > 15 ? 4 : Infinity) };
  }, [tree]);

  const edges = useMemo(() => {
    const result = [];
    const walk = (n) => {
      if (!n) return;
      if (n.left) result.push([n, n.left]);
      if (n.right) result.push([n, n.right]);
      walk(n.left);
      walk(n.right);
    };
    walk(tree);
    return result;
  }, [tree]);

  useLayoutEffect(() => {
    const container = containerRef.current;
    if (!container || !tree) {
      setLines([]);
      return;
    }

    const buildLines = () => {
      const containerRect = container.getBoundingClientRect();
      const scrollLeft = container.scrollLeft;
      const scrollTop = container.scrollTop;
      const nextLines = [];

      edges.forEach(([from, to]) => {
        const fromEl = nodeRefs.current.get(from);
        const toEl = nodeRefs.current.get(to);
        if (!fromEl || !toEl) return;
        const fromRect = fromEl.getBoundingClientRect();
        const toRect = toEl.getBoundingClientRect();

        const x1 = fromRect.left - containerRect.left + fromRect.width / 2 + scrollLeft;
        const y1 = fromRect.top - containerRect.top + fromRect.height + scrollTop;
        const x2 = toRect.left - containerRect.left + toRect.width / 2 + scrollLeft;
        const y2 = toRect.top - containerRect.top + scrollTop;
        nextLines.push({ x1, y1, x2, y2 });
      });

      setLines(nextLines);
    };

    buildLines();
    const onScroll = () => buildLines();
    const onResize = () => buildLines();
    container.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onResize);
    let ro;
    if (typeof ResizeObserver !== "undefined") {
      ro = new ResizeObserver(() => buildLines());
      ro.observe(container);
    }

    return () => {
      container.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onResize);
      if (ro) ro.disconnect();
    };
  }, [edges, tree, levels]);

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
        <div style={{ position: "relative" }}>
          <div ref={containerRef} style={{ overflowX: "auto", maxHeight: "520px", overflowY: "auto", paddingBottom: "4px", position: "relative" }}>
            {lines.length > 0 && (
              <svg
                width={containerRef.current?.scrollWidth || 0}
                height={containerRef.current?.scrollHeight || 0}
                style={{ position: "absolute", top: 0, left: 0, pointerEvents: "none" }}
              >
                {lines.map((l, i) => (
                  <line key={i} x1={l.x1} y1={l.y1} x2={l.x2} y2={l.y2} stroke={C.border2} strokeWidth="1" />
                ))}
              </svg>
            )}
            <div style={{ display: "flex", flexDirection: "column", gap: "22px", alignItems: "center", minWidth: total > 10 ? "860px" : "auto" }}>
              {levels.map((lvl, li) => (
                <div key={li} style={{ display: "flex", flexDirection: "column", alignItems: "center", width: "100%" }}>
                  <div style={{ fontSize: "9px", color: C.textMuted, marginBottom: "6px", fontWeight: 600, letterSpacing: "1px" }}>
                    NIVEL {li}
                  </div>
                  {(() => {
                    const boost = li === 1 ? 70 : li === 2 ? 24 : 0;
                    const levelGap = Math.max(
                      NODE_GAP,
                      NODE_GAP + (levels.length - li - 1) * LEVEL_GAP_STEP + boost
                    );
                    const levelWidth = lvl.length * NODE_WIDTH + (lvl.length - 1) * levelGap;
                    return (
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: `repeat(${lvl.length}, ${NODE_WIDTH}px)`,
                      columnGap: `${levelGap}px`,
                      justifyContent: "center",
                      width: levelWidth
                    }}
                  >
                    {lvl.map((n, i) =>
                      n ? (
                        <AVLNode
                          key={`${n.codigo ?? n.value}-${i}`}
                          node={n}
                          isRoot={li === 0}
                          onHover={setHoveredNode}
                          onMount={(nodeRef, el) => {
                            if (!el) return;
                            nodeRefs.current.set(nodeRef, el);
                          }}
                        />
                      ) : (
                        <div key={`empty-${li}-${i}`} style={{ width: NODE_WIDTH, height: "32px" }} />
                      )
                    )}
                  </div>
                    );
                  })()}
                  {li < levels.length - 1 && <div style={{ marginTop: "8px", color: C.border2, fontSize: "18px" }}>↓</div>}
                </div>
              ))}
            </div>
          </div>
          {hoveredNode && (
            <div
              style={{
                position: "absolute",
                top: 0,
                right: 0,
                width: "260px",
                background: C.surface2,
                border: `1px solid ${C.border}`,
                borderRadius: "10px",
                padding: "12px",
                boxShadow: "0 10px 26px rgba(0,0,0,.35)",
                pointerEvents: "none"
              }}
            >
              <div style={{ fontSize: "11px", fontWeight: 700, color: C.text, marginBottom: "8px" }}>
                Detalle del nodo
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px 10px", fontSize: "10px" }}>
                <div style={{ color: C.textMuted }}>Codigo</div><div style={{ color: C.text }}>{hoveredNode.codigo ?? hoveredNode.value ?? "-"}</div>
                <div style={{ color: C.textMuted }}>Origen</div><div style={{ color: C.text }}>{hoveredNode.origen ?? hoveredNode.datos?.origen ?? "-"}</div>
                <div style={{ color: C.textMuted }}>Destino</div><div style={{ color: C.text }}>{hoveredNode.destino ?? hoveredNode.datos?.destino ?? "-"}</div>
                <div style={{ color: C.textMuted }}>Hora</div><div style={{ color: C.text }}>{hoveredNode.horaSalida ?? hoveredNode.datos?.horaSalida ?? "-"}</div>
                <div style={{ color: C.textMuted }}>Pasajeros</div><div style={{ color: C.text }}>{hoveredNode.pasajeros ?? hoveredNode.datos?.pasajeros ?? 0}</div>
                <div style={{ color: C.textMuted }}>Prioridad</div><div style={{ color: C.text }}>{hoveredNode.prioridad ?? hoveredNode.datos?.prioridad ?? 0}</div>
                <div style={{ color: C.textMuted }}>Precio base</div><div style={{ color: C.text }}>${hoveredNode.precioBase ?? hoveredNode.datos?.precioBase ?? 0}</div>
                <div style={{ color: C.textMuted }}>Precio final</div><div style={{ color: C.text }}>${hoveredNode.precioFinal ?? hoveredNode.datos?.precioFinal ?? (hoveredNode.precioBase ?? hoveredNode.datos?.precioBase ?? 0)}</div>
                <div style={{ color: C.textMuted }}>Promocion</div><div style={{ color: C.text }}>{(hoveredNode.promocion ?? hoveredNode.datos?.promocion) ? "si" : "no"}</div>
                <div style={{ color: C.textMuted }}>Alerta</div><div style={{ color: C.text }}>{(hoveredNode.alerta ?? hoveredNode.datos?.alerta) ? "si" : "no"}</div>
                <div style={{ color: C.textMuted }}>Profundidad</div><div style={{ color: C.text }}>{hoveredNode.profundidad ?? 0}</div>
                <div style={{ color: C.textMuted }}>Balance</div><div style={{ color: C.text }}>{hoveredNode.balance_factor ?? hoveredNode.balance ?? 0}</div>
              </div>
            </div>
          )}
        </div>
      )}
    </Card>
  );
}

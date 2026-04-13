import Btn from "../components/Btn";
import Card from "../components/Card";
import Pill from "../components/Pill";
import { C, gCardHeader, gCardTitle } from "../theme";

export default function StressSection({ stressMode, handlers, auditReport, clearAudit, tree }) {
  const findDepth = (n, code, d = 0) => {
    if (!n) return null;
    const c = n.codigo ?? n.value;
    if (c === code) return d;
    const l = findDepth(n.left, code, d + 1);
    return l !== null ? l : findDepth(n.right, code, d + 1);
  };

  const buildErr = (item) => {
    const h = item.expected_height !== item.actual_height;
    const b = item.expected_balance === false;
    return h && b ? "Altura y balance" : h ? "Altura incorrecta" : "Desbalanceado";
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
      <div
        style={{
          background: stressMode ? C.redDim : C.surface,
          border: `1px solid ${stressMode ? C.red : C.border}`,
          borderRadius: "12px",
          overflow: "hidden"
        }}
      >
        <div style={{ ...gCardHeader, borderBottom: `1px solid ${stressMode ? C.redBdr : C.border}` }}>
          <h3 style={{ ...gCardTitle, color: stressMode ? C.red : C.text }}>Control de modo estrés</h3>
          {stressMode ? (
            <Pill text="ACTIVO — Sin balanceo AVL" color={C.red} bg={C.redDim} border={C.redBdr} />
          ) : (
            <Pill text="Normal — Balanceo automático" color={C.green} bg={C.greenDim} border={C.greenBdr} />
          )}
        </div>
        <div style={{ padding: "18px" }}>
          {stressMode && (
            <div
              style={{
                padding: "12px 16px",
                background: "#1a0a0c",
                border: `1px solid ${C.redBdr}`,
                borderRadius: "8px",
                marginBottom: "16px",
                color: C.red,
                fontSize: "12px",
                fontWeight: 600,
                lineHeight: "1.6"
              }}
            >
              El árbol se comporta como BST sin rotaciones AVL. Los factores de balance pueden superar ±1.
            </div>
          )}
          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
            {stressMode ? (
              <Btn color={C.green} bg={C.greenDim} border={C.greenBdr} onClick={handlers.disableStress}>Volver a modo normal</Btn>
            ) : (
              <Btn color={C.red} bg={C.redDim} border={C.redBdr} onClick={handlers.enableStress}>Activar modo estrés</Btn>
            )}
            <Btn color={stressMode ? C.textMuted : C.accentLt} bg={stressMode ? C.surface3 : C.accentDim} border={stressMode ? C.border : C.accentBdr} onClick={handlers.rebalance} disabled={stressMode}>Rebalancear</Btn>
            {stressMode && <Btn color={C.amber} bg={C.amberDim} border={C.amberBdr} onClick={handlers.audit}>Auditar árbol AVL</Btn>}
          </div>
        </div>
      </div>
      {auditReport && (
        <div style={{ background: auditReport.valid ? C.greenDim : C.redDim, border: `1px solid ${auditReport.valid ? C.greenBdr : C.redBdr}`, borderRadius: "12px", overflow: "hidden" }}>
          <div style={{ ...gCardHeader, borderBottom: `1px solid ${auditReport.valid ? C.greenBdr : C.redBdr}` }}>
            <h3 style={{ ...gCardTitle, color: auditReport.valid ? C.green : C.red }}>
              {auditReport.valid ? `✓ Árbol válido — ${auditReport.nodes_checked} nodos verificados` : `⚠ ${auditReport.inconsistent_nodes?.length || 0} nodos inconsistentes`}
            </h3>
            <Btn color={C.textSub} bg={C.surface3} border={C.border2} onClick={clearAudit}>Cerrar</Btn>
          </div>
          {!auditReport.valid && (
            <div style={{ padding: "18px", overflowX: "auto" }}>
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "12px" }}>
                <thead>
                  <tr>
                    {["Código", "Profundidad", "Factor balance", "Altura real", "Altura esperada", "Error"].map((h) => (
                      <th key={h} style={{ textAlign: "left", padding: "8px 10px", borderBottom: `1px solid ${C.border}`, color: C.textMuted, fontSize: "10px", fontWeight: 700, letterSpacing: ".5px" }}>
                        {h.toUpperCase()}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {auditReport.inconsistent_nodes?.map((item, i) => {
                    const depth = findDepth(tree, item.codigo);
                    return (
                      <tr key={i} style={{ borderBottom: `1px solid ${C.border}` }}>
                        <td style={{ padding: "9px 10px", fontWeight: 700, color: C.text }}>{item.codigo}</td>
                        <td style={{ padding: "9px 10px", color: C.textSub }}>{depth ?? "—"}</td>
                        <td style={{ padding: "9px 10px", color: C.textSub }}>{item.balance_factor}</td>
                        <td style={{ padding: "9px 10px", color: C.textSub }}>{item.actual_height}</td>
                        <td style={{ padding: "9px 10px", color: C.textSub }}>{item.expected_height}</td>
                        <td style={{ padding: "9px 10px" }}>
                          <Pill text={buildErr(item)} color={C.red} bg={C.redDim} border={C.redBdr} />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

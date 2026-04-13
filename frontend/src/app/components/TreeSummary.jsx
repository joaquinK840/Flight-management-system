import Card from "./Card";
import { C } from "../theme";

const calcHeight = (node) => {
  if (!node) return 0;
  return 1 + Math.max(calcHeight(node.left), calcHeight(node.right));
};

const calcLeaves = (node) => {
  if (!node) return 0;
  if (!node.left && !node.right) return 1;
  return calcLeaves(node.left) + calcLeaves(node.right);
};

export default function TreeSummary({ title, tree, metrics }) {
  const rootValue = tree?.codigo ?? tree?.value ?? "—";
  const height = metrics?.height ?? calcHeight(tree);
  const leaves = metrics?.leaves ?? calcLeaves(tree);
  const depthMax = height > 0 ? height - 1 : 0;

  return (
    <Card
      header={
        <div style={{ fontSize: "12px", fontWeight: 700, color: C.text }}>
          {title}
        </div>
      }
    >
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,minmax(0,1fr))", gap: "10px" }}>
        <div style={{ background: C.surface2, border: `1px solid ${C.border}`, borderRadius: "10px", padding: "10px" }}>
          <div style={{ fontSize: "9px", color: C.textMuted, fontWeight: 700, letterSpacing: ".7px", marginBottom: "6px" }}>RAIZ</div>
          <div style={{ fontSize: "16px", fontWeight: 700, color: C.text }}>{rootValue}</div>
        </div>
        <div style={{ background: C.surface2, border: `1px solid ${C.border}`, borderRadius: "10px", padding: "10px" }}>
          <div style={{ fontSize: "9px", color: C.textMuted, fontWeight: 700, letterSpacing: ".7px", marginBottom: "6px" }}>PROFUNDIDAD MAX</div>
          <div style={{ fontSize: "16px", fontWeight: 700, color: C.text }}>{depthMax}</div>
        </div>
        <div style={{ background: C.surface2, border: `1px solid ${C.border}`, borderRadius: "10px", padding: "10px" }}>
          <div style={{ fontSize: "9px", color: C.textMuted, fontWeight: 700, letterSpacing: ".7px", marginBottom: "6px" }}>ALTURA</div>
          <div style={{ fontSize: "16px", fontWeight: 700, color: C.text }}>{height}</div>
        </div>
        <div style={{ background: C.surface2, border: `1px solid ${C.border}`, borderRadius: "10px", padding: "10px" }}>
          <div style={{ fontSize: "9px", color: C.textMuted, fontWeight: 700, letterSpacing: ".7px", marginBottom: "6px" }}>HOJAS</div>
          <div style={{ fontSize: "16px", fontWeight: 700, color: C.text }}>{leaves}</div>
        </div>
      </div>
    </Card>
  );
}

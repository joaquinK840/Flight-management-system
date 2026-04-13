import Btn from "../components/Btn";
import Card from "../components/Card";
import Pill from "../components/Pill";
import { C, gCardTitle, gInput, gLabel } from "../theme";

export default function OpsSection({ value, setValue, handlers, searchResult, traversalResult, traversalMode }) {
  const tl = { pre: "Preorden", in: "Inorden", post: "Postorden", level: "Por niveles" };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
      <Card header={<h3 style={gCardTitle}>Operaciones del árbol</h3>}>
        <div style={{ marginBottom: "14px" }}>
          <label style={gLabel}>CÓDIGO DE VUELO</label>
          <input
            value={value}
            type="number"
            placeholder="Ingresa el código numérico del vuelo…"
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handlers.search()}
            style={gInput}
          />
        </div>
        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
          <Btn color={C.accentLt} bg={C.accentDim} border={C.accentBdr} onClick={handlers.search}>Buscar</Btn>
          <Btn color={C.red} bg={C.redDim} border={C.redBdr} onClick={handlers.delete}>Eliminar</Btn>
          <Btn color={C.violet} bg={C.violetDim} border={C.violetBdr} onClick={handlers.cancel}>Cancelar vuelo</Btn>
          <Btn color={C.textSub} bg={C.surface3} border={C.border2} onClick={handlers.undo}>Deshacer</Btn>
          <Btn color={C.textSub} bg={C.surface3} border={C.border2} onClick={handlers.redo}>Rehacer</Btn>
          <Btn color={C.amber} bg={C.amberDim} border={C.amberBdr} onClick={handlers.profit}>Menor rentabilidad</Btn>
          <Btn color={C.teal} bg={C.tealDim} border={C.tealBdr} onClick={handlers.compare}>Comparar AVL/BST</Btn>
          <Btn color={C.red} bg={C.redDim} border={C.redBdr} onClick={handlers.reset}>Reiniciar</Btn>
        </div>
      </Card>
      {searchResult && (
        <div
          style={{
            background: searchResult.found ? C.greenDim : C.redDim,
            border: `1px solid ${searchResult.found ? C.greenBdr : C.redBdr}`,
            borderRadius: "10px",
            padding: "14px 18px",
            display: "flex",
            alignItems: "center",
            gap: "14px"
          }}
        >
          <div
            style={{
              width: "36px",
              height: "36px",
              background: searchResult.found ? C.greenBdr : C.redBdr,
              borderRadius: "8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "18px",
              fontWeight: 700,
              color: searchResult.found ? C.green : C.red
            }}
          >
            {searchResult.found ? "✓" : "✕"}
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: "13px", color: searchResult.found ? C.green : C.red }}>
              {searchResult.found ? "Vuelo encontrado" : "Vuelo no encontrado"}
            </div>
            <div style={{ color: C.textMuted, fontSize: "11px", marginTop: "2px" }}>Código: {searchResult.value}</div>
          </div>
        </div>
      )}
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
            {Array.isArray(traversalResult) ? traversalResult.join(" → ") : traversalResult}
          </div>
        </Card>
      )}
    </div>
  );
}

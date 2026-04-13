import Btn from "../components/Btn";
import Card from "../components/Card";
import { C, gCardTitle, gInput, gLabel } from "../theme";

export default function OpsSection({ value, setValue, handlers, searchResult }) {

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
      <Card header={<h3 style={gCardTitle}>Operaciones del árbol</h3>}>
        <div style={{ marginBottom: "14px" }}>
          <label style={gLabel}>CÓDIGO DE VUELO</label>
          <input
            value={value}
            type="text"
            placeholder="Ingresa el código del vuelo…"
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
            alignItems: "flex-start",
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
            {searchResult.found && searchResult.node && (
              <div
                style={{
                  marginTop: "10px",
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "6px 12px",
                  fontSize: "11px",
                  color: C.text
                }}
              >
                <div style={{ color: C.textMuted }}>Origen</div><div>{searchResult.node.origen ?? searchResult.node.datos?.origen ?? "-"}</div>
                <div style={{ color: C.textMuted }}>Destino</div><div>{searchResult.node.destino ?? searchResult.node.datos?.destino ?? "-"}</div>
                <div style={{ color: C.textMuted }}>Hora</div><div>{searchResult.node.horaSalida ?? searchResult.node.datos?.horaSalida ?? "-"}</div>
                <div style={{ color: C.textMuted }}>Pasajeros</div><div>{searchResult.node.pasajeros ?? searchResult.node.datos?.pasajeros ?? 0}</div>
                <div style={{ color: C.textMuted }}>Prioridad</div><div>{searchResult.node.prioridad ?? searchResult.node.datos?.prioridad ?? 0}</div>
                <div style={{ color: C.textMuted }}>Precio base</div><div>${searchResult.node.precioBase ?? searchResult.node.datos?.precioBase ?? 0}</div>
                <div style={{ color: C.textMuted }}>Precio final</div><div>${searchResult.node.precioFinal ?? searchResult.node.datos?.precioFinal ?? (searchResult.node.precioBase ?? searchResult.node.datos?.precioBase ?? 0)}</div>
                <div style={{ color: C.textMuted }}>Promoción</div><div>{(searchResult.node.promocion ?? searchResult.node.datos?.promocion) ? "si" : "no"}</div>
                <div style={{ color: C.textMuted }}>Alerta</div><div>{(searchResult.node.alerta ?? searchResult.node.datos?.alerta) ? "si" : "no"}</div>
                <div style={{ color: C.textMuted }}>Profundidad</div><div>{searchResult.node.profundidad ?? searchResult.depth ?? 0}</div>
                <div style={{ color: C.textMuted }}>Balance</div><div>{searchResult.node.balance_factor ?? searchResult.node.balance ?? 0}</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

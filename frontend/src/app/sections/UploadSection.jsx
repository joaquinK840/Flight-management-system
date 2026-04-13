import { useRef, useState } from "react";
import Btn from "../components/Btn";
import Card from "../components/Card";
import Pill from "../components/Pill";
import { C, gCardTitle, gInput, gLabel } from "../theme";

export default function UploadSection({ onFileLoad, onExport, depthLimit, onDepthLimitChange }) {
  const topRef = useRef();
  const insRef = useRef();
  const [dl, setDl] = useState(depthLimit ?? 3);
  const [applying, setApplying] = useState(false);

  const onFile = async (e, mode) => {
    const f = e.target.files?.[0];
    if (f) await onFileLoad(f, mode);
    e.target.value = "";
  };

  const apply = async () => {
    setApplying(true);
    try {
      await onDepthLimitChange(dl);
    } finally {
      setApplying(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
      <Card
        header={
          <>
            <h3 style={gCardTitle}>Cargar desde JSON</h3>
            <Pill text="Topología / Inserción" color={C.textSub} bg={C.surface3} border={C.border2} />
          </>
        }
      >
        <p style={{ color: C.textMuted, fontSize: "12px", marginBottom: "18px", lineHeight: "1.7" }}>
          <strong style={{ color: C.textSub }}>Topología</strong> carga la estructura completa del árbol. {" "}
          <strong style={{ color: C.textSub }}>Inserción</strong> extrae códigos SB* e inserta uno a uno en el árbol AVL.
        </p>
        <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
          <input ref={topRef} type="file" accept=".json" style={{ display: "none" }} onChange={(e) => onFile(e, "topology")} />
          <Btn color={C.green} bg={C.greenDim} border={C.greenBdr} onClick={() => topRef.current?.click()}>
            Cargar topología
          </Btn>
          <input ref={insRef} type="file" accept=".json" style={{ display: "none" }} onChange={(e) => onFile(e, "insertion")} />
          <Btn color={C.accentLt} bg={C.accentDim} border={C.accentBdr} onClick={() => insRef.current?.click()}>
            Cargar por inserción
          </Btn>
          <Btn color={C.amber} bg={C.amberDim} border={C.amberBdr} onClick={onExport}>
            Exportar JSON
          </Btn>
        </div>
      </Card>
      <Card
        header={
          <>
            <h3 style={gCardTitle}>Profundidad límite crítica</h3>
            <Pill text="Penalización de precio" color={C.amber} bg={C.amberDim} border={C.amberBdr} />
          </>
        }
      >
        <p style={{ color: C.textMuted, fontSize: "12px", marginBottom: "16px", lineHeight: "1.7" }}>
          Nodos más profundos que este límite reciben penalización económica automática en el cálculo de precio final.
        </p>
        <div style={{ display: "flex", gap: "12px", alignItems: "flex-end" }}>
          <div>
            <label style={gLabel}>LÍMITE (NIVELES)</label>
            <input
              type="number"
              min="0"
              max="20"
              value={dl}
              onChange={(e) => setDl(parseInt(e.target.value) || 0)}
              style={{ ...gInput, width: "90px" }}
            />
          </div>
          <Btn color={C.text} bg={C.surface3} border={C.border2} onClick={apply} disabled={applying}>
            {applying ? "Aplicando…" : "Aplicar"}
          </Btn>
          <span style={{ color: C.textMuted, fontSize: "12px", paddingBottom: "2px" }}>
            Actual: <strong style={{ color: C.textSub }}>{dl}</strong>
          </span>
        </div>
      </Card>
    </div>
  );
}

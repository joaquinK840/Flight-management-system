import Pill from "./Pill";
import { C } from "../theme";

const NAV = [
  { id: "upload", label: "Cargar datos", path: "M12 3l8 8h-5v8H9v-8H4l8-8z" },
  { id: "tree", label: "Árbol AVL", path: "M12 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm-8 14a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm16 0a3 3 0 1 0 0 6 3 3 0 0 0 0-6zM12 8v4m0 0-4 4m4-4 4 4" },
  { id: "ops", label: "Operaciones", path: "M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" },
  { id: "traversal", label: "Recorridos", path: "M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" },
  { id: "metrics", label: "Métricas", path: "M3 3v18h18M7 16l4-4 4 4 4-8" },
  { id: "queue", label: "Cola FIFO", path: "M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 1 4 0M9 5a2 2 0 0 0 4 0" },
  { id: "versions", label: "Versiones", path: "M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0z" },
  { id: "stress", label: "Modo estrés", path: "M13 10V3L4 14h7v7l9-11h-7z" }
];

export default function Sidebar({ active, setActive, stressMode, metrics, leastProfitable }) {
  return (
    <nav
      style={{
        width: "210px",
        background: C.surface,
        borderRight: `1px solid ${C.border}`,
        padding: "16px 0",
        flexShrink: 0,
        overflowY: "auto",
        display: "flex",
        flexDirection: "column"
      }}
    >
      <div
        style={{
          padding: "0 16px 8px",
          fontSize: "9px",
          fontWeight: 700,
          color: C.textMuted,
          letterSpacing: "1.5px"
        }}
      >
        NAVEGACIÓN
      </div>
      {NAV.map((n) => {
        const on = active === n.id;
        return (
          <button
            key={n.id}
            onClick={() => setActive(n.id)}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              padding: "9px 16px",
              width: "100%",
              border: "none",
              borderLeft: `2px solid ${on ? C.accentLt : "transparent"}`,
              background: on ? C.surface2 : "transparent",
              color: on ? C.accentLt : C.textMuted,
              fontSize: "13px",
              fontWeight: on ? 600 : 400,
              textAlign: "left",
              cursor: "pointer",
              fontFamily: "inherit"
            }}
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke={on ? C.accentLt : C.textMuted}
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d={n.path} />
            </svg>
            {n.label}
            {n.id === "stress" && stressMode && (
              <Pill text="ON" color={C.red} bg={C.redDim} border={C.redBdr} />
            )}
          </button>
        );
      })}
      <div
        style={{
          margin: "20px 12px 0",
          padding: "14px",
          background: C.surface2,
          border: `1px solid ${C.border}`,
          borderRadius: "10px"
        }}
      >
        <div
          style={{
            fontSize: "9px",
            fontWeight: 700,
            color: C.textMuted,
            letterSpacing: "1px",
            marginBottom: "10px"
          }}
        >
          ESTADO DEL ÁRBOL
        </div>
        {[
          ["Altura", metrics?.height ?? 0, C.accentLt],
          [" Nodos", metrics?.total_nodes ?? 0, C.green],
          ["Hojas", metrics?.leaves ?? 0, C.violet],
          null,
          ["Rot. LL", metrics?.rotations?.ll ?? 0, C.amber],
          ["Rot. RR", metrics?.rotations?.rr ?? 0, C.amber],
          null,
          ["Menor rentab.", leastProfitable?.code ?? "—", C.accentLt],
          ["Rentabilidad", leastProfitable ? `$${leastProfitable.rent}` : "—", C.textSub]
        ].map((r, i) =>
          r === null ? (
            <div key={i} style={{ height: "1px", background: C.border, margin: "6px 0" }} />
          ) : (
            <div
              key={i}
              style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}
            >
              <span style={{ fontSize: "11px", color: C.textMuted }}>{r[0]}</span>
              <span style={{ fontSize: "12px", fontWeight: 700, color: r[2] }}>{r[1]}</span>
            </div>
          )
        )}
      </div>
    </nav>
  );
}

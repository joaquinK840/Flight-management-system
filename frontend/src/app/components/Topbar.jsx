import Pill from "./Pill";
import { C } from "../theme";

export default function Topbar({ stressMode, metrics }) {
  return (
    <header
      style={{
        background: C.surface,
        borderBottom: `1px solid ${C.border}`,
        padding: "0 22px",
        height: "54px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexShrink: 0,
        position: "sticky",
        top: 0,
        zIndex: 100
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
        <div
          style={{
            width: "34px",
            height: "34px",
            background: "#1a3a6e",
            border: "1px solid #2d5aa0",
            borderRadius: "9px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
          }}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path
              d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"
              fill="#5b9ef4"
            />
          </svg>
        </div>
        <div>
          <div style={{ fontSize: "14px", fontWeight: 700, color: C.text, letterSpacing: "-.2px" }}>
            SkyAVL Operations
          </div>
          <div style={{ fontSize: "10px", color: C.textMuted, fontWeight: 500, letterSpacing: ".5px" }}>
            FLIGHT MANAGEMENT SYSTEM
          </div>
        </div>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        {stressMode && (
          <Pill text="STRESS MODE" color={C.red} bg={C.redDim} border={C.redBdr} />
        )}
        {metrics && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              padding: "5px 12px",
              background: C.surface2,
              border: `1px solid ${C.border2}`,
              borderRadius: "8px"
            }}
          >
            <div style={{ width: "6px", height: "6px", background: C.green, borderRadius: "50%" }} />
            <span style={{ color: C.textSub, fontSize: "11px" }}>
              {metrics.total_nodes ?? 0} nodos · altura {metrics.height ?? 0}
            </span>
          </div>
        )}
        <Pill
          text={stressMode ? "BST" : "AVL"}
          color={stressMode ? C.red : C.accentLt}
          bg={stressMode ? C.redDim : C.accentDim}
          border={stressMode ? C.redBdr : C.accentBdr}
        />
      </div>
    </header>
  );
}

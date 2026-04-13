import { useEffect } from "react";
import { C } from "../theme";

export default function Toast({ msg, type, onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 3500);
    return () => clearTimeout(t);
  }, [msg, onClose]);

  if (!msg) return null;

  const map = {
    success: { c: C.green, b: C.greenDim, bdr: C.greenBdr },
    error: { c: C.red, b: C.redDim, bdr: C.redBdr },
    info: { c: C.accentLt, b: C.accentDim, bdr: C.accentBdr },
    warning: { c: C.amber, b: C.amberDim, bdr: C.amberBdr }
  };
  const v = map[type] || map.info;

  return (
    <div
      style={{
        position: "fixed",
        bottom: "24px",
        right: "24px",
        padding: "12px 18px",
        background: v.b,
        border: `1px solid ${v.bdr}`,
        borderRadius: "10px",
        color: v.c,
        fontWeight: 600,
        fontSize: "13px",
        zIndex: 9999,
        display: "flex",
        alignItems: "center",
        gap: "12px",
        maxWidth: "320px",
        boxShadow: "0 8px 32px rgba(0,0,0,.5)"
      }}
    >
      <span style={{ flex: 1 }}>{msg}</span>
      <button
        onClick={onClose}
        style={{
          background: "none",
          border: "none",
          color: "inherit",
          cursor: "pointer",
          fontWeight: 700,
          fontSize: "16px"
        }}
      >
        ×
      </button>
    </div>
  );
}

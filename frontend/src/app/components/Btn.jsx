import { C } from "../theme";

export default function Btn({ children, color, bg, border, onClick, disabled, style = {} }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        padding: "8px 15px",
        background: disabled ? C.surface3 : bg,
        color: disabled ? C.textMuted : color,
        border: `1px solid ${disabled ? C.border : border}`,
        borderRadius: "7px",
        cursor: disabled ? "not-allowed" : "pointer",
        fontWeight: 600,
        fontSize: "12px",
        fontFamily: "inherit",
        display: "inline-flex",
        alignItems: "center",
        gap: "6px",
        whiteSpace: "nowrap",
        ...style
      }}
    >
      {children}
    </button>
  );
}

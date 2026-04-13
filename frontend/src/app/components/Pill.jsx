import { C } from "../theme";

export default function Pill({ text, color, bg, border }) {
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: "3px 9px",
        borderRadius: "999px",
        background: bg,
        border: `1px solid ${border}`,
        color,
        fontSize: "10px",
        fontWeight: 700,
        letterSpacing: ".4px"
      }}
    >
      {text}
    </span>
  );
}

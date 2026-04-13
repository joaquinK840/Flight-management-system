import { C, gCardBody, gCardHeader } from "../theme";

export default function Card({ header, children, redBorder }) {
  return (
    <div
      style={{
        background: C.surface,
        border: `1px solid ${redBorder ? C.red : C.border}`,
        borderRadius: "12px",
        overflow: "hidden"
      }}
    >
      <div style={gCardHeader}>{header}</div>
      <div style={gCardBody}>{children}</div>
    </div>
  );
}

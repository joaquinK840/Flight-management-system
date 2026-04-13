import { useEffect, useState } from "react";
import Btn from "../components/Btn";
import Card from "../components/Card";
import Pill from "../components/Pill";
import { apiGet, apiPost } from "../apiClient";
import { C, gCardTitle } from "../theme";

export default function VersionSection({ onRestored }) {
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const d = await apiGet("/versions");
      setVersions(d.versions || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const restore = async (id) => {
    try {
      await apiPost(`/versions/${id}/restore`, {});
      onRestored?.();
      load();
    } catch {
      return null;
    }
    return null;
  };

  return (
    <Card
      header={
        <>
          <h3 style={gCardTitle}>Historial de versiones</h3>
          <Btn color={C.textSub} bg={C.surface3} border={C.border2} onClick={load}>Actualizar</Btn>
        </>
      }
    >
      {loading && <div style={{ color: C.textMuted, textAlign: "center", padding: "20px" }}>Cargando…</div>}
      {!loading && !versions.length && <div style={{ color: C.textMuted, textAlign: "center", padding: "20px" }}>No hay versiones guardadas</div>}
      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        {versions.map((v, i) => (
          <div key={v.id ?? i} style={{ display: "flex", alignItems: "center", gap: "14px", padding: "12px 14px", background: C.surface2, border: `1px solid ${C.border}`, borderRadius: "10px" }}>
            <div style={{ width: "38px", height: "38px", background: C.accentDim, border: `1px solid ${C.accentBdr}`, borderRadius: "9px", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "12px", fontWeight: 700, color: C.accentLt }}>
              v{i + 1}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 700, color: C.text, fontSize: "13px" }}>Versión {i + 1}</div>
              <div style={{ fontSize: "11px", color: C.textMuted, marginTop: "2px" }}>{v.timestamp ?? v.created_at ?? "—"}</div>
            </div>
            {v.nodes != null && <Pill text={`${v.nodes} nodos`} color={C.textSub} bg={C.surface3} border={C.border2} />}
            <Btn color={C.accentLt} bg={C.accentDim} border={C.accentBdr} onClick={() => restore(v.id ?? i)}>Restaurar</Btn>
          </div>
        ))}
      </div>
    </Card>
  );
}

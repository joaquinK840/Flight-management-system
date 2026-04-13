import { useEffect, useState } from "react";
import Btn from "../components/Btn";
import Card from "../components/Card";
import Pill from "../components/Pill";
import Toast from "../components/Toast";
import { apiGet, apiPost, API_BASE_URL } from "../apiClient";
import { C, gCardTitle } from "../theme";

export default function VersionSection({ onRestored }) {
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [versionName, setVersionName] = useState("");
  const [msg, setMsg] = useState(null);

  const notify = (t, tp = "info") => {
    setMsg({ t, tp });
    setTimeout(() => setMsg(null), 3000);
  };

  const load = async () => {
    setLoading(true);
    try {
      const d = await apiGet("/versions/list");
      setVersions(d.versions || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const restore = async (name) => {
    try {
      await apiPost(`/versions/restore/${name}`, {});
      onRestored?.();
      load();
    } catch {
      return null;
    }
    return null;
  };

  const saveVersion = async () => {
    const rawName = versionName.trim();
    const pad2 = (n) => String(n).padStart(2, "0");
    const now = new Date();
    const ts = `${now.getFullYear()}-${pad2(now.getMonth() + 1)}-${pad2(now.getDate())} ${pad2(now.getHours())}:${pad2(now.getMinutes())}:${pad2(now.getSeconds())}`;
    const existing = new Set(versions.map((v) => v.name).filter(Boolean));
    let name = rawName || `Version ${ts}`;
    if (existing.has(name)) {
      name = `${name} (${ts})`;
    }
    setSaving(true);
    try {
      const res = await fetch(`${API_BASE_URL}/versions/save`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        notify(data.detail || "Error guardando versión", "error");
        return;
      }
      setVersionName("");
      notify("Versión guardada", "success");
      load();
    } finally {
      setSaving(false);
    }
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
      {msg && <Toast msg={msg.t} type={msg.tp} onClose={() => setMsg(null)} />}
      <div style={{ display: "flex", gap: "10px", alignItems: "center", marginBottom: "14px" }}>
        <input
          value={versionName}
          onChange={(e) => setVersionName(e.target.value)}
          placeholder="Nombre de la versión"
          style={{
            flex: 1,
            background: C.surface2,
            border: `1px solid ${C.border2}`,
            color: C.text,
            borderRadius: "8px",
            padding: "8px 10px",
            fontSize: "12px",
            outline: "none",
            fontFamily: "inherit"
          }}
        />
        <Btn color={C.accentLt} bg={C.accentDim} border={C.accentBdr} onClick={saveVersion} disabled={saving || !versionName.trim()}>
          {saving ? "Guardando…" : "Guardar versión"}
        </Btn>
      </div>
      {loading && <div style={{ color: C.textMuted, textAlign: "center", padding: "20px" }}>Cargando…</div>}
      {!loading && !versions.length && <div style={{ color: C.textMuted, textAlign: "center", padding: "20px" }}>No hay versiones guardadas</div>}
      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        {versions.map((v, i) => (
          <div key={v.name ?? v.id ?? i} style={{ display: "flex", alignItems: "center", gap: "14px", padding: "12px 14px", background: C.surface2, border: `1px solid ${C.border}`, borderRadius: "10px" }}>
            <div style={{ width: "38px", height: "38px", background: C.accentDim, border: `1px solid ${C.accentBdr}`, borderRadius: "9px", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "12px", fontWeight: 700, color: C.accentLt }}>
              v{i + 1}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 700, color: C.text, fontSize: "13px" }}>{v.name ?? `Versión ${i + 1}`}</div>
              <div style={{ fontSize: "11px", color: C.textMuted, marginTop: "2px" }}>{v.created_at ?? v.timestamp ?? "—"}</div>
            </div>
            {v.total_nodes != null && <Pill text={`${v.total_nodes} nodos`} color={C.textSub} bg={C.surface3} border={C.border2} />}
            <Btn color={C.accentLt} bg={C.accentDim} border={C.accentBdr} onClick={() => restore(v.name ?? v.id ?? i)}>Restaurar</Btn>
          </div>
        ))}
      </div>
    </Card>
  );
}

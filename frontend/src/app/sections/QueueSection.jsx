import { useEffect, useState } from "react";
import Btn from "../components/Btn";
import Card from "../components/Card";
import Pill from "../components/Pill";
import Toast from "../components/Toast";
import { apiDelete, apiGet, apiPost } from "../apiClient";
import { C, gCardTitle, gInput, gLabel } from "../theme";

export default function QueueSection({ onUpdated }) {
  const [pending, setPending] = useState([]);
  const [results, setResults] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ codigo: "", origen: "", destino: "", horaSalida: "", precioBase: "", pasajeros: "", prioridad: 1 });
  const [msg, setMsg] = useState(null);

  const notify = (t, tp = "info") => {
    setMsg({ t, tp });
    setTimeout(() => setMsg(null), 3000);
  };

  useEffect(() => {
    const fetchQueue = async () => {
      try {
        const d = await apiGet("/queue/pending");
        if (d.status === "success") setPending(d.flights || []);
      } catch {
        return null;
      }
      return null;
    };

    fetchQueue();
    const id = setInterval(fetchQueue, 2000);
    return () => clearInterval(id);
  }, []);

  const addFlight = async () => {
    if (!form.codigo || !form.origen || !form.destino || !form.horaSalida || !form.precioBase || !form.pasajeros) {
      notify("Completa todos los campos", "error");
      return;
    }
    try {
      const d = await apiPost("/queue/add", {
        ...form,
        precioBase: parseFloat(form.precioBase),
        pasajeros: parseInt(form.pasajeros),
        prioridad: parseInt(form.prioridad)
      });
      if (d.status === "success") {
        notify("Vuelo agregado", "success");
        setForm({ codigo: "", origen: "", destino: "", horaSalida: "", precioBase: "", pasajeros: "", prioridad: 1 });
        setShowForm(false);
      } else {
        notify(d.message || "Error", "error");
      }
    } catch {
      notify("Error de conexión", "error");
    }
  };

  const processOne = async () => {
    setProcessing(true);
    try {
      const d = await apiPost("/queue/process_one", {});
      if (d.status === "success") {
        setResults((p) => [d, ...p].slice(0, 10));
        notify("Vuelo procesado", "success");
        onUpdated?.();
      }
    } finally {
      setProcessing(false);
    }
  };

  const processAll = async () => {
    setProcessing(true);
    try {
      const d = await apiPost("/queue/process_all", {});
      if (d.results) {
        setResults((p) => [...d.results, ...p].slice(0, 20));
        notify(`${d.results.length} vuelos procesados`, "success");
        onUpdated?.();
      }
    } finally {
      setProcessing(false);
    }
  };

  const clearQ = async () => {
    try {
      await apiDelete("/queue/clear");
      setPending([]);
      notify("Cola limpiada", "info");
    } catch {
      return null;
    }
    return null;
  };

  const fields = [
    ["Código", "codigo", "number"],
    ["Origen", "origen", "text"],
    ["Destino", "destino", "text"],
    ["Hora salida", "horaSalida", "text"],
    ["Precio base", "precioBase", "number"],
    ["Pasajeros", "pasajeros", "number"],
    ["Prioridad", "prioridad", "number"]
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
      {msg && <Toast msg={msg.t} type={msg.tp} onClose={() => setMsg(null)} />}
      <Card
        header={
          <>
            <h3 style={gCardTitle}>Cola de concurrencia FIFO</h3>
            <Pill text={`${pending.length} en cola`} color={C.accentLt} bg={C.accentDim} border={C.accentBdr} />
          </>
        }
      >
        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "18px" }}>
          <Btn color={C.green} bg={C.greenDim} border={C.greenBdr} onClick={() => setShowForm((f) => !f)}>
            Agregar vuelo
          </Btn>
          <Btn color={C.accentLt} bg={C.accentDim} border={C.accentBdr} onClick={processOne} disabled={processing || !pending.length}>
            Procesar siguiente
          </Btn>
          <Btn color={C.violet} bg={C.violetDim} border={C.violetBdr} onClick={processAll} disabled={processing || !pending.length}>
            Procesar todo
          </Btn>
          <Btn color={C.textSub} bg={C.surface3} border={C.border2} onClick={clearQ} disabled={!pending.length}>
            Limpiar cola
          </Btn>
        </div>
        {showForm && (
          <div style={{ background: C.surface2, border: `1px solid ${C.border}`, borderRadius: "10px", padding: "16px", marginBottom: "16px" }}>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4,minmax(0,1fr))", gap: "10px", marginBottom: "14px" }}>
              {fields.map(([label, key, type]) => (
                <div key={key}>
                  <label style={gLabel}>{label.toUpperCase()}</label>
                  <input type={type} value={form[key]} onChange={(e) => setForm((p) => ({ ...p, [key]: e.target.value }))} style={gInput} />
                </div>
              ))}
            </div>
            <div style={{ display: "flex", gap: "8px" }}>
              <Btn color={C.green} bg={C.greenDim} border={C.greenBdr} onClick={addFlight}>Agregar a cola</Btn>
              <Btn color={C.textSub} bg={C.surface3} border={C.border2} onClick={() => setShowForm(false)}>Cancelar</Btn>
            </div>
          </div>
        )}
        {pending.length > 0 && (
          <div>
            <div style={{ fontSize: "10px", color: C.textMuted, fontWeight: 700, letterSpacing: ".8px", marginBottom: "8px" }}>VUELOS EN COLA</div>
            <div style={{ display: "flex", flexDirection: "column", gap: "6px", maxHeight: "220px", overflowY: "auto" }}>
              {pending.map((f, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "10px 14px", background: C.surface3, border: `1px solid ${C.border}`, borderRadius: "9px" }}>
                  <div style={{ width: "24px", height: "24px", background: C.accentDim, border: `1px solid ${C.accentBdr}`, borderRadius: "6px", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "11px", fontWeight: 700, color: C.accentLt }}>
                    {i + 1}
                  </div>
                  <div style={{ fontWeight: 700, color: C.text, fontSize: "13px" }}>{f.codigo}</div>
                  <div style={{ color: C.textMuted, fontSize: "12px" }}>{f.origen} → {f.destino}</div>
                  <div style={{ marginLeft: "auto" }}>
                    <Pill text={`Prio ${f.prioridad ?? 1}`} color={C.violet} bg={C.violetDim} border={C.violetBdr} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        {results.length > 0 && (
          <div style={{ marginTop: "16px" }}>
            <div style={{ fontSize: "10px", color: C.textMuted, fontWeight: 700, letterSpacing: ".8px", marginBottom: "8px" }}>RESULTADOS RECIENTES</div>
            <div style={{ display: "flex", flexDirection: "column", gap: "4px", maxHeight: "160px", overflowY: "auto" }}>
              {results.map((r, i) => (
                <div key={i} style={{ fontSize: "12px", padding: "7px 10px", background: r.conflict ? C.redDim : C.greenDim, border: `1px solid ${r.conflict ? C.redBdr : C.greenBdr}`, borderRadius: "7px", color: r.conflict ? C.red : C.green }}>
                  {r.conflict ? "⚠ Conflicto" : "✓"} {r.flight?.codigo ?? ""} — {r.message ?? "Procesado"}
                </div>
              ))}
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}

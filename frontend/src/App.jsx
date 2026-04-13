import { useEffect, useState } from "react";
import { apiDelete, apiGet, apiPost, apiPut, apiUpload, API_BASE_URL } from "./app/apiClient";
import { C } from "./app/theme";
import Toast from "./app/components/Toast";
import Btn from "./app/components/Btn";
import Topbar from "./app/components/Topbar";
import Sidebar from "./app/components/Sidebar";
import TreeView from "./app/components/TreeView";
import TreeSummary from "./app/components/TreeSummary";
import UploadSection from "./app/sections/UploadSection";
import OpsSection from "./app/sections/OpsSection";
import TraversalSection from "./app/sections/TraversalSection";
import MetricsSection from "./app/sections/MetricsSection";
import QueueSection from "./app/sections/QueueSection";
import VersionSection from "./app/sections/VersionSection";
import StressSection from "./app/sections/StressSection";

export default function App(){
  const[active,setActive]=useState("tree");
  const[sidebarCollapsed,setSidebarCollapsed]=useState(false);
  const[tree,setTree]=useState(null),[bstTree,setBstTree]=useState(null),[bstNote,setBstNote]=useState(null);
  const[bstMetrics,setBstMetrics]=useState(null);
  const[metrics,setMetrics]=useState(null),[stressMode,setStress]=useState(false);
  const[value,setValue]=useState(""),[searchResult,setSearch]=useState(null);
  const[traversalResult,setTrav]=useState(null),[traversalMode,setTravMode]=useState(null);
  const[showComparison,setComp]=useState(false),[depthLimit,setDepth]=useState(3);
  const[auditReport,setAudit]=useState(null),[rebalanceReport,setRebalance]=useState(null),[toast,setToast]=useState(null);

  const notify=(text,type="info")=>{setToast({text,type});setTimeout(()=>setToast(null),3500);};
  const normalizeCodigo=(input)=>{
    const raw=String(input??"").trim();
    if(!raw)return { ok:false, value:null };
    const digits=raw.replace(/\D+/g, "");
    if(!digits)return { ok:false, value:null };
    return { ok:true, value:parseInt(digits,10) };
  };
  const extractTree=(data)=>{
    if(!data)return null;
    if(data.root!==undefined)return data.root;
    if(data.tree!==undefined)return extractTree(data.tree);
    return data;
  };
  const findNodeByCode=(root, code, depth=0)=>{
    if(!root) return null;
    const nodeCode = root.codigo ?? root.value ?? null;
    if(nodeCode === code) return { node: root, depth };
    return findNodeByCode(root.left, code, depth + 1) || findNodeByCode(root.right, code, depth + 1);
  };
  const getLeastProfitable=(root)=>{
    if(!root) return null;
    let best={ rent: Infinity, depth: -1, code: null, node: null };
    const walk=(n, depth=0)=>{
      if(!n) return;
      const pasajeros = n.pasajeros ?? n.datos?.pasajeros ?? 0;
      const precioFinal = n.precioFinal ?? n.datos?.precioFinal ?? n.precioBase ?? n.datos?.precioBase ?? 0;
      const promocion = n.promocion ?? n.datos?.promocion ?? false;
      const rent = (pasajeros * precioFinal) - (promocion ? 0.1 * precioFinal : 0);
      const code = n.codigo ?? n.value ?? null;
      if(rent < best.rent || (rent === best.rent && depth > best.depth) || (rent === best.rent && depth === best.depth && code > best.code)){
        best = { rent, depth, code, node: n };
      }
      walk(n.left, depth + 1);
      walk(n.right, depth + 1);
    };
    walk(root, 0);
    if(best.code == null) return null;
    return { code: best.code, rent: Math.round(best.rent * 100) / 100, depth: best.depth };
  };
  const loadTree=async()=>{try{const d=await apiGet("/avl/tree");setTree(extractTree(d));}catch{}};
  const loadMetrics=async()=>{try{const d=await apiGet("/avl/metrics");if(d){setMetrics(d);setStress(d.stress_mode??false);}}catch{}};
  useEffect(()=>{loadTree();loadMetrics();},[]);

  const handleFileLoad=async(file,mode)=>{
    const fd=new FormData();
    fd.append("file",file);
    fd.append("load_type",mode);
    try{
      const d=await apiUpload("/avl/load-file",fd);
      setTree(extractTree(d?.avl?.tree ?? d?.avl ?? d));
      setBstTree(extractTree(d?.bst?.tree ?? d?.bst ?? null));
      setBstMetrics(d?.bst?.metrics ?? null);
      if(d?.load_type==="topology"){
        setBstNote("BST construido insertando los mismos vuelos en orden inorden — sin balanceo automático");
      }else{
        setBstNote(null);
      }
      notify(`Archivo cargado — modo ${mode}`,"success");
      await loadMetrics();
    }catch{notify("Error al cargar","error");}
  };
  const handleExport=async()=>{try{const d=await apiGet("/avl/export-json");const b=new Blob([JSON.stringify(d,null,2)],{type:"application/json"});const u=URL.createObjectURL(b);const a=document.createElement("a");a.href=u;a.download="avl_tree.json";a.click();notify("Exportado","success");}catch{notify("Error al exportar","error");}};
  const handleDepth=async(dl)=>{try{const d=await apiPut("/avl/config/depth-limit",{limit:dl});setTree(extractTree(d));setDepth(dl);notify(`Profundidad límite: ${dl}`,"success");await loadMetrics();}catch{notify("Error","error");}};

  const handlers={
    search:   async()=>{
      const parsed=normalizeCodigo(value);
      if(!parsed.ok){notify("Código inválido","warning");return;}
      try{
        const d=await apiGet(`/avl/search/${parsed.value}`);
        const info = d.found ? findNodeByCode(tree, parsed.value) : null;
        setSearch({value: parsed.value, found: d.found, node: info?.node ?? null, depth: info?.depth ?? null});
        setActive("ops");
      }catch{notify("Error","error");}
    },
    delete:   async()=>{
      const parsed=normalizeCodigo(value);
      if(!parsed.ok){notify("Código inválido","warning");return;}
      try{
        let d=await apiDelete(`/flights/delete/${parsed.value}`);
        if(d?.detail){
          d=await apiDelete(`/avl/delete/${parsed.value}`);
          if(d?.detail){
            notify(d.detail,"error");
            return;
          }
        }
        if(d?.tree){
          setTree(extractTree(d.tree));
        }
        notify(`Vuelo ${value} eliminado`,"success");
        setValue("");
        await loadMetrics();
      }catch{notify("Error","error");}
    },
    cancel:   async()=>{
      const parsed=normalizeCodigo(value);
      if(!parsed.ok){notify("Código inválido","warning");return;}
      try{
        let d=await apiDelete(`/flights/cancel/${parsed.value}`);
        if(d?.detail){
          d=await apiDelete(`/avl/cancel/${parsed.value}`);
          if(d?.detail){
            notify(d.detail,"error");
            return;
          }
        }
        if(d?.tree){
          setTree(extractTree(d.tree));
        }
        notify(`Vuelo ${value} cancelado`,"info");
        setValue("");
        await loadMetrics();
      }catch{notify("Error","error");}
    },
    undo:     async()=>{try{const d=await apiPost("/flights/undo");setTree(extractTree(d));notify("Deshecho","info");await loadMetrics();}catch{}},
    redo:     async()=>{try{const d=await apiPost("/flights/redo");setTree(extractTree(d));notify("Rehecho","info");await loadMetrics();}catch{}},
    profit:   async()=>{
      try{
        let res=await fetch(`${API_BASE_URL}/flights/eliminate-least-profitable`,{method:"DELETE"});
        if(res.status===404){
          res=await fetch(`${API_BASE_URL}/avl/least-profitable`,{method:"DELETE"});
        }
        const d=await res.json().catch(()=>({}));
        if(!res.ok){
          notify(d?.detail || d?.message || "Error al eliminar menor rentabilidad","error");
          return;
        }
        if(d?.tree){
          setTree(extractTree(d.tree));
        } else {
          await loadTree();
        }
        const code=d?.eliminated_code ?? "";
        const rent=d?.eliminated_rentability;
        const removed=d?.subtree_size_removed;
        const depth=d?.profundidad;
        const parts=[];
        if(code) parts.push(`Vuelo ${code}`);
        if(typeof rent==="number") parts.push(`rentabilidad $${rent}`);
        if(typeof removed==="number") parts.push(`${removed} nodo(s)`);
        if(typeof depth==="number") parts.push(`prof ${depth}`);
        notify(parts.length?`Eliminado: ${parts.join(" · ")}`:"Nodo eliminado","success");
        await loadMetrics();
      }catch{notify("Error","error");}
    },
    compare:  async()=>{
      if(!bstTree){
        notify("Carga un archivo para comparar AVL/BST","warning");
        return;
      }
      setComp(true);
      setActive("tree");
    },
    reset:    async()=>{try{await apiDelete("/avl/reset");setTree(null);setBstTree(null);setSearch(null);setTrav(null);setComp(false);setMetrics(null);notify("Reiniciado","info");}catch{}},
    enableStress: async()=>{try{await apiPost("/avl/stress-mode/enable");setStress(true);notify("Modo estrés activado","warning");await loadTree();await loadMetrics();}catch{}},
    disableStress:async()=>{try{await apiPost("/avl/stress-mode/disable");const d=await apiPost("/avl/rebalance");setRebalance(d);setStress(false);notify("Rebalanceo global aplicado","success");await loadTree();await loadMetrics();}catch{}},
    rebalance:async()=>{try{const d=await apiPost("/avl/rebalance");setRebalance(d);notify("Rebalanceado","success");await loadTree();await loadMetrics();}catch{}},
    audit:    async()=>{try{const d=await apiGet("/avl/audit");setAudit(d);}catch{notify("Error en auditoría","error");}},
  };

  const handleTraversal=async(mode)=>{
    const apiMode=mode==="level"?"bfs":mode==="depth"?"pre":mode;
    try{
      const d=await apiGet(`/avl/traversal/${apiMode}`);
      setTrav(d.result??d.traversal??d);
      setTravMode(mode);
      setActive("traversal");
    }catch{notify("Error","error");}
  };
  const onUpdated=async()=>{await loadTree();await loadMetrics();};

  const section={
    upload:<UploadSection onFileLoad={handleFileLoad} onExport={handleExport} depthLimit={depthLimit} onDepthLimitChange={handleDepth}/>,
    tree:<div>{showComparison?<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:"16px"}}><div style={{display:"flex",flexDirection:"column",gap:"12px"}}><TreeSummary title="Resumen AVL" tree={tree} metrics={metrics}/><TreeView tree={tree} title="Árbol AVL"/></div><div style={{display:"flex",flexDirection:"column",gap:"12px"}}><TreeSummary title="Resumen BST" tree={bstTree} metrics={bstMetrics}/><TreeView tree={bstTree} title="Árbol BST (comparación)" showBst/>{bstNote&&<div style={{marginTop:"8px",fontSize:"11px",color:C.amber,textAlign:"center"}}>{bstNote}</div>}<div style={{marginTop:"10px",textAlign:"center"}}><Btn color={C.textSub} bg={C.surface3} border={C.border2} onClick={()=>{setComp(false);setBstTree(null);}}>Cerrar comparación</Btn></div></div></div>:<div style={{display:"flex",flexDirection:"column",gap:"12px"}}><TreeSummary title="Resumen AVL" tree={tree} metrics={metrics}/><TreeView tree={tree} title="Árbol AVL — Sistema de vuelos"/></div>}</div>,
    ops:<OpsSection value={value} setValue={setValue} handlers={handlers} searchResult={searchResult}/>,
    traversal:<TraversalSection onTraversal={handleTraversal} traversalResult={traversalResult} traversalMode={traversalMode}/>,
    metrics:<MetricsSection metrics={metrics} refreshMetrics={loadMetrics}/>,
    queue:<QueueSection onUpdated={onUpdated}/>,
    versions:<VersionSection onRestored={onUpdated}/>,
    stress:<StressSection stressMode={stressMode} handlers={handlers} auditReport={auditReport} clearAudit={()=>setAudit(null)} rebalanceReport={rebalanceReport} clearRebalance={()=>setRebalance(null)} tree={tree}/>,
  };

  return<div style={{minHeight:"100vh",background:C.bg,color:C.text,fontFamily:"'Segoe UI',system-ui,sans-serif",fontSize:"13px"}}>
    <style>{`*{box-sizing:border-box;margin:0;padding:0}::-webkit-scrollbar{width:4px;height:4px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:#2a3347;border-radius:4px}button:not([disabled]):hover{opacity:.82}input:focus{border-color:${C.accent}!important;outline:none}`}</style>
    {toast&&<Toast msg={toast.text} type={toast.type} onClose={()=>setToast(null)}/>}
    <Topbar stressMode={stressMode} metrics={metrics}/>
    <div style={{display:"flex",height:"calc(100vh - 54px)"}}>
      <Sidebar
        active={active}
        setActive={setActive}
        stressMode={stressMode}
        metrics={metrics}
        leastProfitable={getLeastProfitable(tree)}
        collapsed={sidebarCollapsed}
        onToggle={()=>setSidebarCollapsed((v)=>!v)}
      />
      <main style={{flex:1,overflowY:"auto",padding:"20px",background:C.bg}}>{section[active]}</main>
    </div>
  </div>;
}

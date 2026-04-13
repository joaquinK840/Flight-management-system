const API_BASE = "http://localhost:8000";

export const apiGet = async (path) => {
  const res = await fetch(`${API_BASE}${path}`);
  return res.json();
};

export const apiPost = async (path, body = {}) => {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return res.json();
};

export const apiDelete = async (path) => {
  const res = await fetch(`${API_BASE}${path}`, { method: "DELETE" });
  return res.json();
};

export const apiPut = async (path, body = {}) => {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return res.json();
};

export const apiUpload = async (path, formData) => {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    body: formData
  });
  return res.json();
};

export const API_BASE_URL = API_BASE;

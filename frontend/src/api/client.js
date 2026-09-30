import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export async function predictSequence(sequence) {
  const { data } = await apiClient.post("/predict", { sequence });
  return data;
}

export async function predictFromCSV(file) {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await apiClient.post("/predict/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}
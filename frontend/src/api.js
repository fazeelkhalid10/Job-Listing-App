// src/api.js
import axios from "axios"

const api = axios.create({
  baseURL: "http://localhost:5000", // Flask runs here
})

export default api

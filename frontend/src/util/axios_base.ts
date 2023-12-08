import axios, { AxiosInstance } from "axios";

const API_URL = import.meta.env.VITE_API_URL;

const instance: AxiosInstance = axios.create({
    baseURL: API_URL,
});

export default instance;
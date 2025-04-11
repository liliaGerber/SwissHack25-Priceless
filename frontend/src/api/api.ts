// api.ts file
import axios from 'axios';
const api = axios.create({
    baseURL: import.meta.env.VITE_API_ENDPOINT,
});
export default api
import axios from 'axios';

const api= axios.create({baseURL: import.meta.env.VITE_API_URL,
    withcredentials: true,
});

export default api
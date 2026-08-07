import axios from 'axios';

const api = axios.create({
  baseURL:'http://127.0.0.1:5000',
  timeout: 10000,
});

export const fetchDevelopers = (query = '', limit = 20) =>
  api.get('/developers', {
    params: { q: query, limit },
  });

export const fetchDashboard = () =>
  api.get('/dashboard');

export const fetchRecommendations = (developerEmail) =>
  api.get(`/recommendations/${encodeURIComponent(developerEmail)}`);

export const fetchSearch = (query) =>
  api.get('/search', {
    params: { q: query },
  });

export default api;

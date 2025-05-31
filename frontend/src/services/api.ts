import axios from 'axios';
import { config } from '../config';

const api = axios.create({
  baseURL: config.apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getStreamlitUrl = () => config.streamlitUrl;

export const apiService = {
  // Add your API endpoints here
  // Example:
  // async getData() {
  //   const response = await api.get('/data');
  //   return response.data;
  // },
  
  // For ML predictions
  async getPrediction(data: any) {
    const response = await api.post('/predict', data);
    return response.data;
  },
};

export default apiService; 
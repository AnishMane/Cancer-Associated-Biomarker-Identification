export const config = {
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  streamlitUrl: import.meta.env.VITE_STREAMLIT_URL || 'http://localhost:8501',
} as const; 
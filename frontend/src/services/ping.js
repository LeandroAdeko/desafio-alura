const API_BASE_URL = import.meta.env.VITE_BACKEND_URL;

async function sendPing(options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  try {
    const response = await fetch(`${API_BASE_URL}/ping`, {
      ...options,
      headers,
      mode: 'cors', // Enable CORS
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return response;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export default {
  sendPing
};

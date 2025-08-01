const API_BASE_URL = import.meta.env.VITE_BACKEND_URL;

async function login(email, password, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  try {
    const response = await fetch(`${API_BASE_URL}/account/login`, {
      method: 'POST',
      body: JSON.stringify({
        email: email,
        password: password
      }),
      ...options,
      headers,
      mode: 'cors',
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

export default login;

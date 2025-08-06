const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

async function create(route, data, options = {}) {
  const url = `${BACKEND_URL}/${route}`;
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
    ...options.headers,
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      body: JSON.stringify(data),
      headers,
      ...options,
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

async function listAll(route, options = {}) {
  const url = `${BACKEND_URL}/${route}`;
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
    ...options.headers,
  };

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers,
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

async function getById(route, id, options = {}) {
  const url = `${BACKEND_URL}/${route}/${id}`;
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
    ...options.headers,
  };

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers,
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

async function update(route, data, options = {}) {
  const url = `${BACKEND_URL}/${route}/${data.id}`;
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
    ...options.headers,
  };

  try {
    const response = await fetch(url, {
      method: 'PUT',
      body: JSON.stringify(data),
      headers,
      ...options,
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

async function remove(route, id, options = {}) {
  const url = `${BACKEND_URL}/${route}/${id}`;
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
    ...options.headers,
  };

  try {
    const response = await fetch(url, {
      method: 'DELETE',
      headers,
      ...options,
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

async function executeQuery(query, options = {}) {
  const url = `${BACKEND_URL}/query`;
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
    ...options.headers,
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      body: JSON.stringify({ query: query }),
      headers,
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export { create, listAll, getById, update, remove, executeQuery };

// API store for handling backend communication

const API_BASE_URL = process.env.API_URL || (import.meta.env.PROD ? '/api' : 'http://localhost:8000/api');

/**
 * Makes an API call to the wizard trainer backend
 * @param {string} endpoint - The API endpoint (without /api/)
 * @param {Object} data - The data to send
 * @returns {Promise<any>} - The response data
 */
export async function apiCall(endpoint, data) {
  try {
    const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API call to ${endpoint} failed:`, error);
    throw error;
  }
}

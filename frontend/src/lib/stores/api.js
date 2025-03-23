// API store for handling backend communication
import { browser } from '$app/environment';

// Get the base URL dynamically
const API_BASE_URL = browser 
  ? (import.meta.env.PROD 
     ? '/api' 
     : 'http://localhost:8000/api')
  : 'http://localhost:8000/api';

/**
 * Makes an API call to the wizard trainer backend
 * @param {string} endpoint - The API endpoint (without /api/)
 * @param {Object} data - The data to send
 * @returns {Promise<any>} - The response data
 */
export async function apiCall(endpoint, data) {
  console.log(`Making API call to ${endpoint} with data:`, data);
  console.log(`Using API base URL: ${API_BASE_URL}`);

  try {
    const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
      credentials: 'include',
      mode: 'cors'
    });

    console.log(`Received response:`, response);

    if (!response.ok) {
      let errorMessage = `HTTP error ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (e) {
        console.error("Failed to parse error response:", e);
      }
      throw new Error(errorMessage);
    }

    const result = await response.json();
    console.log(`Response data:`, result);
    return result;
  } catch (error) {
    console.error(`API call to ${endpoint} failed:`, error);
    throw error;
  }
}

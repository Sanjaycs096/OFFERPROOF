/**
 * OFFERPROOF API Service
 * Manages communication with the FastAPI backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Checks backend health status and measures latency.
 * @returns {Promise<{ isOnline: boolean, data?: object, latencyMs?: number, error?: string }>}
 */
export async function checkBackendHealth() {
  const startTime = performance.now();
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    const latencyMs = Math.round(performance.now() - startTime);

    if (!response.ok) {
      return {
        isOnline: false,
        latencyMs,
        error: `Server responded with status ${response.status}`,
      };
    }

    const data = await response.json();
    return {
      isOnline: true,
      data,
      latencyMs,
    };
  } catch (err) {
    const latencyMs = Math.round(performance.now() - startTime);
    return {
      isOnline: false,
      latencyMs,
      error: err instanceof Error ? err.message : 'Network connection failed',
    };
  }
}

/**
 * Fetches basic API information from root endpoint.
 * @returns {Promise<{ success: boolean, data?: object, error?: string }>}
 */
export async function fetchApiInfo() {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      return {
        success: false,
        error: `Server error: ${response.status}`,
      };
    }

    const data = await response.json();
    return {
      success: true,
      data,
    };
  } catch (err) {
    return {
      success: false,
      error: err instanceof Error ? err.message : 'Failed to reach API info endpoint',
    };
  }
}

export { API_BASE_URL };

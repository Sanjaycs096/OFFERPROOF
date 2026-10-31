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
 * Fetches versioned API v1 health and capability info.
 */
export async function fetchApiV1Health() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/health`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });
    if (!response.ok) {
      return { success: false, error: `Status ${response.status}` };
    }
    const data = await response.json();
    return { success: true, data };
  } catch (err) {
    return {
      success: false,
      error: err instanceof Error ? err.message : 'Connection failed',
    };
  }
}

/**
 * Ingests raw opportunity text.
 * @param {{ text: string, url?: string, category_hint?: string }} payload
 */
export async function ingestText(payload) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/ingest/text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      return {
        success: false,
        error: data.detail || `Server error ${response.status}`,
      };
    }
    return { success: true, data };
  } catch (err) {
    return {
      success: false,
      error: err instanceof Error ? err.message : 'Failed to ingest text',
    };
  }
}

/**
 * Ingests a PDF document via multipart/form-data.
 * @param {File} file
 * @param {string} [url]
 */
export async function ingestPdf(file, url) {
  try {
    const formData = new FormData();
    formData.append('file', file);
    if (url) {
      formData.append('url', url);
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/ingest/pdf`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      return {
        success: false,
        error: data.detail || `Server error ${response.status}`,
      };
    }
    return { success: true, data };
  } catch (err) {
    return {
      success: false,
      error: err instanceof Error ? err.message : 'Failed to upload PDF',
    };
  }
}

/**
 * Extracts entities, claims, and suspicious indicators from ingested text.
 * @param {{ content: string, source_type?: string, application_url?: string, force_mode?: string }} payload
 */
export async function extractClaims(payload) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/extract`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      return {
        success: false,
        error: data.detail || `Extraction failed with status ${response.status}`,
      };
    }
    return { success: true, data };
  } catch (err) {
    return {
      success: false,
      error: err instanceof Error ? err.message : 'Network request failed',
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

import { useState, useEffect, useCallback } from 'react';
import { checkBackendHealth } from '../services/api';

/**
 * Custom hook to monitor FastAPI backend connectivity status.
 */
export function useHealthCheck(pollIntervalMs = 30000) {
  const [status, setStatus] = useState({
    isChecking: true,
    isOnline: false,
    data: null,
    latencyMs: null,
    error: null,
    lastChecked: null,
  });

  const runCheck = useCallback(async () => {
    setStatus((prev) => ({ ...prev, isChecking: true }));
    const result = await checkBackendHealth();
    setStatus({
      isChecking: false,
      isOnline: result.isOnline,
      data: result.data || null,
      latencyMs: result.latencyMs ?? null,
      error: result.error || null,
      lastChecked: new Date(),
    });
  }, []);

  useEffect(() => {
    runCheck();

    if (pollIntervalMs > 0) {
      const interval = setInterval(runCheck, pollIntervalMs);
      return () => clearInterval(interval);
    }
  }, [runCheck, pollIntervalMs]);

  return {
    ...status,
    refresh: runCheck,
  };
}

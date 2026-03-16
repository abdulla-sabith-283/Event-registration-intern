/**
 * script.js — Student Task Manager
 * Utility helper functions used by the React frontend in index.html.
 */

// ── Format a date string for display ─────────────────────────────────────────
/**
 * Converts an ISO date string (e.g. "2026-03-20") to "20 Mar 2026".
 * Returns "No due date" if the value is empty.
 * @param {string} dateStr
 * @returns {string}
 */
function formatDate(dateStr) {
  if (!dateStr) return 'No due date';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

// ── Get a readable status label ───────────────────────────────────────────────
/**
 * Returns "Completed" or "Pending" based on the task status string.
 * @param {string} status - "completed" or "pending"
 * @returns {string}
 */
function getStatusLabel(status) {
  return status === 'completed' ? 'Completed' : 'Pending';
}

// ── Get CSS badge class for a priority level ──────────────────────────────────
/**
 * Maps a priority string to its CSS badge class name.
 * @param {string} priority - "High", "Medium", or "Low"
 * @returns {string} CSS class name
 */
function getPriorityClass(priority) {
  const map = { High: 'badge-high', Medium: 'badge-medium', Low: 'badge-low' };
  return map[priority] || 'badge-medium';
}

// ── Validate task form input ──────────────────────────────────────────────────
/**
 * Checks that a task has at minimum a non-empty title.
 * Returns an error message string, or empty string if valid.
 * @param {object} task - { title, due_date, priority, description }
 * @returns {string} error message or ""
 */
function validateTaskInput(task) {
  if (!task.title || task.title.trim() === '') {
    return 'Task title cannot be empty.';
  }
  if (task.title.trim().length < 3) {
    return 'Task title must be at least 3 characters.';
  }
  return '';
}

// ── Calculate completion progress percentage ──────────────────────────────────
/**
 * Returns the percentage of tasks that are completed, rounded to the nearest integer.
 * Returns 0 if there are no tasks.
 * @param {number} completed - number of completed tasks
 * @param {number} total     - total number of tasks
 * @returns {number} 0–100
 */
function calculateProgress(completed, total) {
  if (!total || total === 0) return 0;
  return Math.round((completed / total) * 100);
}

// ── Generic API request helper ────────────────────────────────────────────────
/**
 * Wrapper around the Fetch API for calling the Flask backend.
 * Handles JSON encoding and throws an error on non-2xx responses.
 * @param {string} url    - API endpoint path
 * @param {string} method - HTTP method (GET, POST, DELETE)
 * @param {object} [body] - Optional request body (will be JSON serialised)
 * @returns {Promise<object>} Parsed JSON response
 */
async function apiRequest(url, method, body) {
  const options = {
    method: method || 'GET',
    headers: { 'Content-Type': 'application/json' }
  };
  if (body) {
    options.body = JSON.stringify(body);
  }
  const response = await fetch(url, options);
  if (!response.ok) {
    const err = await response.json().catch(function() { return { message: 'Request failed' }; });
    throw new Error(err.message || 'HTTP ' + response.status);
  }
  return response.json();
}

// ── Export for Node.js / testing environments ─────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    formatDate,
    getStatusLabel,
    getPriorityClass,
    validateTaskInput,
    calculateProgress,
    apiRequest
  };
}

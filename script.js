/**
 * script.js — College Event Registration Portal
 * Utility helper functions used by the React frontend in index.html.
 */

// ── Format ISO date to readable string ────────────────────────────────────────
/**
 * Converts "2026-04-10" to "10 Apr 2026".
 * @param {string} dateStr
 * @returns {string}
 */
function formatDate(dateStr) {
  if (!dateStr) return '';
  var d = new Date(dateStr);
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

// ── Calculate seat availability percentage ────────────────────────────────────
/**
 * Returns percentage of seats filled, capped at 100.
 * @param {number} registered
 * @param {number} total
 * @returns {number} 0–100
 */
function seatPercent(registered, total) {
  if (!total || total === 0) return 0;
  return Math.min(Math.round((registered / total) * 100), 100);
}

// ── Check if an event is full ─────────────────────────────────────────────────
/**
 * Returns true if no seats are available.
 * @param {object} event - { seats, registered }
 * @returns {boolean}
 */
function isFull(event) {
  return event.registered >= event.seats;
}

// ── Validate registration form ────────────────────────────────────────────────
/**
 * Checks name and email are present and email looks valid.
 * Returns an error string, or empty string if valid.
 * @param {string} name
 * @param {string} email
 * @returns {string}
 */
function validateRegistration(name, email) {
  if (!name || name.trim() === '') return 'Name is required.';
  if (!email || email.trim() === '') return 'Email is required.';
  if (email.indexOf('@') === -1 || email.indexOf('.') === -1) return 'Enter a valid email address.';
  return '';
}

// ── Validate new event form ───────────────────────────────────────────────────
/**
 * Checks all event fields are filled in.
 * Returns an error string, or empty string if valid.
 * @param {object} event - { name, date, venue, seats }
 * @returns {string}
 */
function validateEvent(event) {
  if (!event.name  || event.name.trim() === '')  return 'Event name is required.';
  if (!event.date  || event.date.trim() === '')  return 'Date is required.';
  if (!event.venue || event.venue.trim() === '') return 'Venue is required.';
  if (!event.seats || isNaN(event.seats) || parseInt(event.seats) < 1) return 'Enter a valid seat count.';
  return '';
}

// ── Generic API request wrapper ───────────────────────────────────────────────
/**
 * Sends a fetch request to the Flask backend.
 * Throws an error on non-2xx responses.
 * @param {string} url
 * @param {string} method - GET, POST, DELETE
 * @param {object} [body]
 * @returns {Promise<object>}
 */
function apiRequest(url, method, body) {
  var options = {
    method: method || 'GET',
    headers: { 'Content-Type': 'application/json' }
  };
  if (body) options.body = JSON.stringify(body);
  return fetch(url, options).then(function(res) {
    if (!res.ok) {
      return res.json().then(function(err) {
        throw new Error(err.message || 'Request failed');
      });
    }
    return res.json();
  });
}

// ── Node.js export ────────────────────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { formatDate, seatPercent, isFull, validateRegistration, validateEvent, apiRequest };
}

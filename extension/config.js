/**
 * Extension Configuration
 * Change BACKEND_URL here to switch between local and production
 */

// PRODUCTION: Cloud Run deployment
const PRODUCTION_URL = 'https://deepfake-backend-kpu7yogeia-uc.a.run.app';

// LOCAL: For testing on localhost
const LOCAL_URL = 'http://localhost:5000';

// CHANGE THIS TO SWITCH ENVIRONMENTS
// Set to 'production' or 'local'
const ENVIRONMENT = 'production';  // Change to 'production' for Cloud Run

// Export the active backend URL
const CONFIG = {
  BACKEND_URL: ENVIRONMENT === 'production' ? PRODUCTION_URL : LOCAL_URL,
  CAPTURE_INTERVAL: 1000,  // Default capture interval in ms
  TIMEOUT: 30000  // Backend timeout in ms
};

// Make config available globally
if (typeof window !== 'undefined') {
  window.CONFIG = CONFIG;
}

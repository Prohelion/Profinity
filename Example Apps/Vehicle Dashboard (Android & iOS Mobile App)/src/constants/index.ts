// API Configuration
export const API_CONFIG = {
  BASE_URL: 'http://localhost:3000',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
};

// App Configuration
export const APP_CONFIG = {
  VERSION: '1.0.0',
  ENVIRONMENT: process.env.NODE_ENV || 'development',
};

// Navigation Configuration
export const NAVIGATION_CONFIG = {
  ANIMATION_DURATION: 300,
  HEADER_HEIGHT: 60,
};

// Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: '@auth_token',
  USER_PREFERENCES: '@user_preferences',
}; 
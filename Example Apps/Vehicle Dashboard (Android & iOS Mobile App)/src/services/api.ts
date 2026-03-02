import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getApiConfig } from './configService';

// Types and Interfaces
interface LoginResponse {
  token: string;
  expiration: string;
}

interface AxiosError {
  response?: {
    data?: {
      message?: string;
      errors?: any;
    };
    status?: number;
    statusText?: string;
  };
  message?: string;
  code?: string;
}

// API Endpoints
const ENDPOINTS = {
  AUTH: '/api/V2/Users/Authenticate',
  BMU: '/api/v2/Data/Prohelion%20BMU',
  MOTOR_CONTROLLER: '/api/v2/Data/Tritium%20WaveSculptor%2022%20-%20Left',
} as const;

// Create axios instance with default config
const api = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Configuration
export const updateApiBaseUrl = async () => {
  const config = await getApiConfig();
  console.log('Setting API base URL to:', config.serverUrl);
  api.defaults.baseURL = config.serverUrl;
  console.log('Current API base URL:', api.defaults.baseURL);
};

// Initialize the baseURL
updateApiBaseUrl();

// Add request interceptor for authentication
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Authentication Services
export const login = async (username: string, password: string): Promise<void> => {
  try {
    console.log('Starting login process...');
    console.log('Current base URL:', api.defaults.baseURL);
    console.log('Login request to:', ENDPOINTS.AUTH);
    
    const response = await api.post<LoginResponse>(ENDPOINTS.AUTH, {
      username,
      password,
    });
    
    console.log('Login API response:', {
      hasToken: !!response.data.token,
      tokenLength: response.data.token?.length,
      hasExpiration: !!response.data.expiration,
      expiration: response.data.expiration
    });
    
    if (response.data.token) {
      await AsyncStorage.setItem('token', response.data.token);
      // Store expiration if provided
      if (response.data.expiration) {
        await AsyncStorage.setItem('tokenExpiration', response.data.expiration);
        console.log('Stored token and expiration in AsyncStorage');
      }
    } else {
      console.error('No token in response:', response.data);
      throw new Error('No token received from server');
    }

    // Verify the token was stored
    const storedToken = await AsyncStorage.getItem('token');
    console.log('Verification - Token in storage:', !!storedToken);
    
    // Test the authentication state immediately after login
    const isAuth = await isAuthenticated();
    console.log('Authentication check after login:', isAuth);

  } catch (error: unknown) {
    console.error('Login error details:', {
      error,
      isAxiosError: error && (error as any).isAxiosError,
      response: (error as any).response?.data,
      status: (error as any).response?.status,
      message: (error as any).message,
      config: {
        baseURL: (error as any).config?.baseURL,
        url: (error as any).config?.url,
        fullUrl: (error as any).config?.baseURL + (error as any).config?.url
      }
    });

    // Log the full error object
    console.error('Full error object:', JSON.stringify(error, null, 2));

    const axiosError = error as AxiosError;

    if (axiosError.response) {
      console.error('Axios response error:', {
        status: axiosError.response.status,
        statusText: axiosError.response.statusText,
        data: axiosError.response.data
      });
      throw new Error(axiosError.response.data?.message || `Login failed with status ${axiosError.response.status}`);
    } else if (axiosError.message) {
      console.error('Axios error message:', axiosError.message);
      throw new Error(`Network error: ${axiosError.message}`);
    } else {
      console.error('Unexpected error type:', typeof error);
      throw new Error('An unexpected error occurred during login');
    }
  }
};

export const logout = async (): Promise<void> => {
  try {
    // Remove both token and expiration
    await AsyncStorage.multiRemove(['token', 'tokenExpiration']);
    console.log('Successfully logged out and cleared tokens');
  } catch (error) {
    console.error('Error during logout:', error);
    // Even if there's an error, we'll consider the logout successful
    // since the user should still be able to log out
  }
};

export const isAuthenticated = async (): Promise<boolean> => {
  try {
    const [token, expiration] = await Promise.all([
      AsyncStorage.getItem('token'),
      AsyncStorage.getItem('tokenExpiration')
    ]);
    
    console.log('Authentication check details:', { 
      hasToken: !!token,
      tokenFirstChars: token ? token.substring(0, 10) : null,
      hasExpiration: !!expiration,
      expiration: expiration
    });
    
    if (!token) {
      console.log('No token found in storage');
      return false;
    }
    
    if (expiration) {
      const expirationDate = new Date(expiration);
      const now = new Date();
      const isValid = expirationDate > now;
      console.log('Token expiration check:', {
        expirationDate: expirationDate.toISOString(),
        currentTime: now.toISOString(),
        isValid
      });
      return isValid;
    }
    
    // If no expiration provided, check JWT expiration
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const now = Date.now();
      const isValid = payload.exp * 1000 > now;
      console.log('JWT expiration check:', {
        jwtExp: new Date(payload.exp * 1000).toISOString(),
        currentTime: new Date(now).toISOString(),
        isValid
      });
      return isValid;
    } catch (error) {
      console.error('JWT parsing error:', error);
      return false;
    }
  } catch (error) {
    console.error('Authentication check error:', error);
    return false;
  }
};

// Vehicle Data Services
export const getProhelionBMUData = async () => {
  try {
    const response = await api.get(ENDPOINTS.BMU);
    return response.data;
  } catch (error) {
    console.error('Error fetching Prohelion BMU data:', error);
    throw error;
  }
};

export const getProhelionMotorControllerData = async () => {
  try {
    const response = await api.get(ENDPOINTS.MOTOR_CONTROLLER);
    return response.data;
  } catch (error) {
    console.error('Error fetching Tritium WaveSculptor data:', error);
    throw error;
  }
};

export const getVehicleVelocity = async (): Promise<number> => {
  try {
    const data = await getProhelionMotorControllerData();
    // Convert m/s to km/h (1 m/s = 3.6 km/h)
    const velocityKmh = data.VelocityMeasurement.VehicleVelocity * 3.6;
    return velocityKmh;
  } catch (error) {
    console.error('Error fetching vehicle velocity:', error);
    throw error;
  }
};

export const getStateOfCharge = async (): Promise<number> => {
  try {
    const data = await getProhelionBMUData();
    // Convert string to number and multiply by 100 to get percentage
    return parseFloat(data.PackStateOfCharge.SOCPercent) * 100;
  } catch (error) {
    console.error('Error fetching state of charge:', error);
    throw error;
  }
};

export default api; 
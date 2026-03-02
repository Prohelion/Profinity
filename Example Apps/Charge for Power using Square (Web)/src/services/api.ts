import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:18080';

interface LoginResponse {
  token: string;
  expiration: string;
}

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`,
      };
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const login = async (username: string, password: string): Promise<void> => {
  try {
    console.log('Attempting login with:', { username });
    const response = await api.post<LoginResponse>('/api/V2/Users/Authenticate', {
      username,
      password,
    });
    
    console.log('Login response:', response.data);
    
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      // Store expiration if provided
      if (response.data.expiration) {
        localStorage.setItem('tokenExpiration', response.data.expiration);
      }
      console.log('Token stored in localStorage');
    } else {
      console.error('No token in response:', response.data);
      throw new Error('No token received from server');
    }
  } catch (error: unknown) {
    console.error('Login error:', error);
    const axiosError = error as { response?: { data?: { message?: string }, status?: number } };
    if (axiosError.response) {
      throw new Error(axiosError.response.data?.message || 'Login failed');
    }
    throw new Error('An unexpected error occurred');
  }
};

export const logout = (): void => {
  localStorage.removeItem('token');
  localStorage.removeItem('tokenExpiration');
};

export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('token');
  const expiration = localStorage.getItem('tokenExpiration');
  
  console.log('Checking authentication:', { 
    hasToken: !!token,
    hasExpiration: !!expiration,
    token: token ? `${token.substring(0, 10)}...` : null
  });
  
  if (!token) return false;
  
  if (expiration) {
    const isValid = new Date(expiration) > new Date();
    console.log('Using server expiration:', { expiration, isValid });
    return isValid;
  }
  
  // If no expiration provided, check JWT expiration
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const isValid = payload.exp * 1000 > Date.now();
    console.log('Using JWT expiration:', { exp: payload.exp, isValid });
    return isValid;
  } catch (error) {
    console.error('Error parsing JWT:', error);
    return false;
  }
};

export const getProhelionBMUData = async () => {
  try {
    const response = await api.get('/api/v2/Data/Prohelion%20BMU');
    return response.data;
  } catch (error) {
    console.error('Error fetching Prohelion BMU data:', error);
    throw error;
  }
};

export default api; 
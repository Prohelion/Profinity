import AsyncStorage from '@react-native-async-storage/async-storage';

const API_SERVER_URL_KEY = 'api_server_url';
const USERNAME_KEY = 'username';

export const DEFAULT_SERVER_URL = 'http://127.0.0.1:18080';

export const getApiConfig = async () => {
  try {
    const serverUrl = await AsyncStorage.getItem(API_SERVER_URL_KEY);
    const username = await AsyncStorage.getItem(USERNAME_KEY);
    if (!serverUrl) {
      return {
        serverUrl: DEFAULT_SERVER_URL,
        username: username || '',
      };
    }
    return {
      serverUrl,
      username: username || '',
    };
  } catch (error) {
    console.error('Error getting API config:', error);
    return {
      serverUrl: DEFAULT_SERVER_URL,
      username: '',
    };
  }
};

export const saveApiConfig = async (serverUrl: string, username?: string) => {
  try {
    await AsyncStorage.setItem(API_SERVER_URL_KEY, serverUrl);
    if (username) {
      await AsyncStorage.setItem(USERNAME_KEY, username);
    }
  } catch (error) {
    console.error('Error saving API config:', error);
    throw error;
  }
}; 
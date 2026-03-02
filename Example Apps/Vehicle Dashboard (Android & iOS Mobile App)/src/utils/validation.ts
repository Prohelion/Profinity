interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

export const validateUsername = (username: string): string | null => {
  if (!username) return 'Username is required';
  if (username.length < 3) return 'Username must be at least 3 characters';
  return null;
};

export const validatePassword = (password: string): string | null => {
  if (!password) return 'Password is required';
  if (password.length < 6) return 'Password must be at least 6 characters';
  return null;
};

export const validateServerUrl = (serverUrl: string): string | null => {
  if (!serverUrl) return 'Server URL is required';
  
  try {
    // Check if it starts with http:// or https://
    if (!serverUrl.startsWith('http://') && !serverUrl.startsWith('https://')) {
      return 'Server URL must start with http:// or https://';
    }

    // Split the URL into protocol and the rest
    const [protocol, rest] = serverUrl.split('://');
    if (!rest) return 'Invalid server URL format';

    // Check if there's a port
    const [host, port] = rest.split(':');
    if (!host) return 'Invalid server URL format';
    
    // Only validate port if it's provided
    if (port && !/^\d+$/.test(port)) {
      return 'Port must be a number';
    }

    return null;
  } catch (error) {
    return 'Invalid server URL format';
  }
};

export const validateLoginForm = (form: { username: string; password: string; serverUrl: string }): ValidationResult => {
  const errors: Record<string, string> = {};
  
  const usernameError = validateUsername(form.username);
  if (usernameError) errors.username = usernameError;
  
  const passwordError = validatePassword(form.password);
  if (passwordError) errors.password = passwordError;

  const serverUrlError = validateServerUrl(form.serverUrl);
  if (serverUrlError) errors.serverUrl = serverUrlError;
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}; 
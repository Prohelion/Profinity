import { DefaultTheme } from '@react-navigation/native';
import { TextStyle } from 'react-native';

export const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#00A3E0',
    secondary: '#1A1A1A',
    background: '#000000',
    card: '#1A1A1A',
    text: '#FFFFFF',
    textSecondary: '#A0A0A0',
    border: '#333333',
    success: '#00A3E0',
    error: '#FF4444',
    warning: '#FFA000',
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  typography: {
    h1: {
      fontSize: 32,
      fontWeight: '700' as TextStyle['fontWeight'],
      color: '#FFFFFF',
    },
    h2: {
      fontSize: 24,
      fontWeight: '600' as TextStyle['fontWeight'],
      color: '#FFFFFF',
    },
    h3: {
      fontSize: 20,
      fontWeight: '600' as TextStyle['fontWeight'],
      color: '#FFFFFF',
    },
    body: {
      fontSize: 16,
      fontWeight: '400' as TextStyle['fontWeight'],
      color: '#FFFFFF',
    },
    caption: {
      fontSize: 14,
      fontWeight: '400' as TextStyle['fontWeight'],
      color: '#A0A0A0',
    },
  },
  borderRadius: {
    sm: 4,
    md: 8,
    lg: 16,
    xl: 24,
    full: 9999,
  },
}; 
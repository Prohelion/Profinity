import { createTheme } from '@mui/material/styles';

// Prohelion brand colors based on their website
export const theme = createTheme({
  palette: {
    primary: {
      main: '#1B365D', // Deep blue from Prohelion's header and buttons
      light: '#2B4A7A',
      dark: '#122440',
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#4CAF50', // Green accent color used in their success indicators
      light: '#6FBF73',
      dark: '#357A38',
      contrastText: '#FFFFFF',
    },
    background: {
      default: '#FFFFFF',
      paper: '#F5F5F5',
    },
    text: {
      primary: '#1B365D',
      secondary: '#666666',
    },
  },
  typography: {
    fontFamily: '"Helvetica Neue", Arial, sans-serif',
    h4: {
      fontWeight: 600,
      fontSize: '2rem',
      lineHeight: 1.2,
      marginBottom: '1rem',
    },
    h5: {
      fontWeight: 500,
      fontSize: '1.5rem',
      lineHeight: 1.4,
    },
    h6: {
      fontWeight: 500,
      fontSize: '1.25rem',
      lineHeight: 1.4,
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 500,
      color: '#666666',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.05)',
          borderRadius: '8px',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#1B365D',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: '4px',
          padding: '8px 24px',
          fontWeight: 500,
        },
      },
    },
  },
}); 
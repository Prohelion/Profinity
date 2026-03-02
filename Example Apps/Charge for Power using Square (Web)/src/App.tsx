import React, { createContext, useState, useEffect, useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { Box, CssBaseline } from '@mui/material';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Home from './components/Home';
import { theme } from './styles/theme';
import { isAuthenticated as checkAuth } from './services/api';

interface AuthContextType {
  isAuthenticated: boolean;
  setAuthenticated: (value: boolean) => void;
}

export const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  setAuthenticated: () => {},
});

// Protected Route component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useContext(AuthContext);
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

// Wrapper component to check current route
const AppContent: React.FC = () => {
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';

  return (
    <Box sx={{ 
      minHeight: '100vh',
      backgroundColor: 'background.default',
      display: 'flex',
      flexDirection: 'column'
    }}>
      {!isLoginPage && <Navbar />}
      <Box sx={{ 
        flex: 1,
        p: 3,
        maxWidth: 1200,
        mx: 'auto',
        width: '100%'
      }}>
        <Routes>
          <Route
            path="/login"
            element={
              <Login />
            }
          />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Box>
    </Box>
  );
};

const App: React.FC = () => {
  const [isAuthenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    // Check authentication status on app load
    const authStatus = checkAuth();
    setAuthenticated(authStatus);
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthContext.Provider value={{ isAuthenticated, setAuthenticated }}>
        <Router>
          <AppContent />
        </Router>
      </AuthContext.Provider>
    </ThemeProvider>
  );
};

export default App;

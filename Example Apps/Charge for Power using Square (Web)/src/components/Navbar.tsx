import React, { useContext } from 'react';
import { AppBar, Toolbar, Typography, Box, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../App';
import { logout } from '../services/api';

const Navbar: React.FC = () => {
  const { isAuthenticated, setAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = (e: React.MouseEvent) => {
    e.preventDefault();
    logout();
    setAuthenticated(false);
    navigate('/login');
  };

  return (
    <AppBar position="static" elevation={0}>
      <Toolbar sx={{ 
        height: 80,
        px: { xs: 2, sm: 4 },
        maxWidth: 1200,
        mx: 'auto',
        width: '100%'
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
          <Typography
            variant="h6"
            component="div"
            sx={{
              fontWeight: 600,
              fontSize: '1.5rem',
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              gap: 2
            }}
          >
            {/* Profinity logo */}
            <img 
              src="/logo192.png" 
              alt="Profinity" 
              style={{ height: 40 }}
            />
            Battery Manager
          </Typography>
        </Box>
        {isAuthenticated && (
          <Button
            onClick={handleLogout}
            sx={{
              color: 'white',
              fontSize: '1.1rem',
              padding: '0.75rem 1.5rem',
              fontWeight: 500,
              textTransform: 'uppercase',
              letterSpacing: '0.5px',
              backgroundColor: 'rgba(255, 255, 255, 0.1)'
            }}
          >
            Logout
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 
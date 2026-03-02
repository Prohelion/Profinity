import React, { useEffect, useState, useRef } from 'react';
import { View, Text, Dimensions, StyleSheet, TouchableOpacity, Image } from 'react-native';
import { getStateOfCharge, getVehicleVelocity, getProhelionBMUData } from '../services/api';
import { logout } from '../services/authService';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { theme } from '../theme';
import { BatteryStatus } from '../components/BatteryStatus';
import { SpeedDial } from '../components/SpeedDial';
import { BackgroundPattern } from '../components/BackgroundPattern';

type RootStackParamList = {
  Login: undefined;
  Dashboard: undefined;
};

type Props = NativeStackScreenProps<RootStackParamList, 'Dashboard'>;

const { width, height } = Dimensions.get('window');
// Calculate logo size based on screen width
const LOGO_SIZE = Math.min(width * 0.3, 150); // 30% of screen width, max 150px

interface VehicleData {
  stateOfCharge: number;
  speed: number;
}

export const Dashboard: React.FC<Props> = ({ navigation }) => {
  const [vehicleData, setVehicleData] = useState<VehicleData>({ 
    stateOfCharge: 0, 
    speed: 0
  });
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const isMounted = useRef(true);

  useEffect(() => {
    isMounted.current = true;
    return () => {
      isMounted.current = false;
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  const fetchData = async () => {
    if (!isMounted.current) return;
    
    try {
      const stateOfCharge = await getStateOfCharge();
      const vehicleVelocity = await getVehicleVelocity();
      
      if (isMounted.current) {
        setVehicleData({
          stateOfCharge: stateOfCharge,
          speed: vehicleVelocity
        });
      }
    } catch (error) {
      console.error('Error fetching vehicle data:', error);
      if ((error as any)?.response?.status === 401) {
        handleLogout();
      }
    }
  };

  useEffect(() => {
    fetchData();
    intervalRef.current = setInterval(fetchData, 1000);
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  const handleLogout = async () => {
    try {
      // Clear the interval first to stop any ongoing data fetches
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      
      // Clear any existing data
      setVehicleData({ stateOfCharge: 0, speed: 0});
      
      // Perform logout
      await logout();
      
      // Navigate back to login screen
      navigation.replace('Login');
    } catch (error) {
      console.error('Logout failed:', error);
      // Even if logout fails, we should still navigate to login
      navigation.replace('Login');
    }
  };

  return (
    <BackgroundPattern>
      <View style={dashboardStyles.container}>
        {/* Logo */}
        <View style={dashboardStyles.logoContainer}>
          <Image 
            source={require('../../assets/profinity-logo.png')}
            style={dashboardStyles.logo}
            resizeMode="contain"
          />
        </View>

        {/* Logout Button */}
        <TouchableOpacity 
          style={dashboardStyles.logoutButton}
          onPress={handleLogout}
        >
          <Text style={dashboardStyles.logoutText}>Logout</Text>
        </TouchableOpacity>

        {/* Speed Dial */}
        <SpeedDial speed={vehicleData.speed} />

        {/* Battery State of Charge */}
        <View style={dashboardStyles.batteryContainer}>
          <BatteryStatus stateOfCharge={vehicleData.stateOfCharge} />
        </View>
      </View>
    </BackgroundPattern>
  );
};

const dashboardStyles = StyleSheet.create({
  container: {
    flex: 1,
    padding: theme.spacing.lg,
  },
  logoutButton: {
    position: 'absolute',
    top: theme.spacing.lg,
    right: theme.spacing.lg,
    padding: theme.spacing.sm,
    backgroundColor: theme.colors.error,
    borderRadius: theme.borderRadius.md,
    borderWidth: 1,
    borderColor: theme.colors.error,
    zIndex: 1,
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  logoutText: {
    ...theme.typography.body,
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
  batteryContainer: {
    flex: 1,
    width: '100%',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: theme.spacing.xl,
    marginBottom: theme.spacing.xl,
  },
  logoContainer: {
    width: '100%',
    alignItems: 'center',
    marginTop: theme.spacing.xl,
    marginBottom: theme.spacing.lg,
  },
  logo: {
    width: LOGO_SIZE,
    height: LOGO_SIZE * 0.5, // Assuming a rectangular logo with 2:1 aspect ratio
  },
}); 
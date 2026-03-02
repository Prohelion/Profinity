import React from 'react';
import { View, StyleSheet, Text, Dimensions } from 'react-native';
import { AnimatedCircularProgress } from 'react-native-circular-progress';
import { theme } from '../theme';

interface SpeedDialProps {
  speed: number;
}

const { width, height } = Dimensions.get('window');
// Calculate speed dial size based on screen dimensions
const SPEED_DIAL_SIZE = Math.min(
  Math.min(width, height) * 0.6, // Use the smaller dimension to ensure it fits
  Math.max(width, height) * 0.4  // But don't let it get too small on larger screens
);

const getSpeedDialColor = (speed: number) => {
  if (speed < 20) return '#4CAF50';
  if (speed < 40) return '#8BC34A';
  if (speed < 60) return '#FFC107';
  if (speed < 80) return '#FF9800';
  return '#F44336';
};

export const SpeedDial: React.FC<SpeedDialProps> = ({ speed }) => {
  return (
    <View style={styles.container}>
      <AnimatedCircularProgress
        size={SPEED_DIAL_SIZE}
        width={15}
        backgroundWidth={5}
        fill={Math.min(speed, 100)}
        tintColor={getSpeedDialColor(speed)}          
        backgroundColor="#3d5875"
        arcSweepAngle={240}
        rotation={240}
        lineCap="round"          
      >
        {(fill) => (
          <View style={styles.content}>
            <Text style={styles.speedText}>{Math.round(speed)}</Text>
            <Text style={styles.unitText}>km/h</Text>
          </View>
        )}
      </AnimatedCircularProgress>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: theme.spacing.xl,
    minHeight: SPEED_DIAL_SIZE + 40, // Add some padding to ensure it doesn't get cut off
  },
  content: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  speedText: {
    ...theme.typography.h1,
    color: theme.colors.primary,
    fontSize: SPEED_DIAL_SIZE * 0.2, // Make font size proportional to dial size
  },
  unitText: {
    ...theme.typography.caption,
    color: theme.colors.textSecondary,
    fontSize: SPEED_DIAL_SIZE * 0.08, // Make unit text proportional to dial size
  },
}); 
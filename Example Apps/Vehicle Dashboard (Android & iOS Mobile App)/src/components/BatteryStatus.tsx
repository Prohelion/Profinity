import React from 'react';
import { View, StyleSheet, Dimensions, Text } from 'react-native';
import Svg, { Path, Rect } from 'react-native-svg';
import { theme } from '../theme';

interface BatteryStatusProps {
  stateOfCharge: number;
}

const getBatteryColor = (soc: number) => {
  if (soc > 80) return '#4CAF50';
  if (soc > 60) return '#8BC34A';
  if (soc > 40) return '#FFC107';
  if (soc > 20) return '#FF9800';
  return '#F44336';
};

export const BatteryStatus: React.FC<BatteryStatusProps> = ({ stateOfCharge }) => {
  const { width, height } = Dimensions.get('window');
  const BATTERY_SIZE = Math.min(
    Math.min(width, height) * 0.5,
    Math.max(width, height) * 0.3
  );
  
  const BATTERY_WIDTH = BATTERY_SIZE;
  const BATTERY_HEIGHT = BATTERY_SIZE * 0.52;
  const BATTERY_CAP_WIDTH = BATTERY_WIDTH * 0.1;
  const BATTERY_CAP_HEIGHT = BATTERY_HEIGHT * 0.4;
  const BATTERY_STROKE_WIDTH = 4;
  const BATTERY_CORNER_RADIUS = 6;
  
  const fillWidth = Math.max(0, Math.min(100, stateOfCharge)) / 100 * (BATTERY_WIDTH - BATTERY_STROKE_WIDTH * 2);
  
  return (
    <View style={styles.container}>
      <Svg width={BATTERY_WIDTH + BATTERY_CAP_WIDTH} height={BATTERY_HEIGHT}>
        {/* Battery Body */}
        <Rect
          x={BATTERY_STROKE_WIDTH / 2}
          y={BATTERY_STROKE_WIDTH / 2}
          width={BATTERY_WIDTH - BATTERY_STROKE_WIDTH}
          height={BATTERY_HEIGHT - BATTERY_STROKE_WIDTH}
          rx={BATTERY_CORNER_RADIUS}
          ry={BATTERY_CORNER_RADIUS}
          stroke={theme.colors.text}
          strokeWidth={BATTERY_STROKE_WIDTH}
          fill="none"
        />
        
        {/* Battery Fill */}
        <Rect
          x={BATTERY_STROKE_WIDTH}
          y={BATTERY_STROKE_WIDTH}
          width={fillWidth}
          height={BATTERY_HEIGHT - BATTERY_STROKE_WIDTH * 2}
          fill={getBatteryColor(stateOfCharge)}
        />
        
        {/* Battery Cap */}
        <Rect
          x={BATTERY_WIDTH}
          y={(BATTERY_HEIGHT - BATTERY_CAP_HEIGHT) / 2}
          width={BATTERY_CAP_WIDTH}
          height={BATTERY_CAP_HEIGHT}
          rx={2}
          ry={2}
          stroke={theme.colors.text}
          strokeWidth={BATTERY_STROKE_WIDTH}
          fill="none"
        />
      </Svg>
      
      {/* Percentage Text */}
      <Text style={[styles.percentageText, { fontSize: BATTERY_SIZE * 0.06 }]}>
        {Math.round(stateOfCharge)}%
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    padding: 16,
  },
  percentageText: {
    color: theme.colors.text,
    marginTop: 8,
    fontWeight: 'bold',
  },
}); 
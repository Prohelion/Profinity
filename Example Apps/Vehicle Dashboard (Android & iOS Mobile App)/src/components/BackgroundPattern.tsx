import React from 'react';
import { ImageBackground, StyleSheet, View } from 'react-native';

interface BackgroundPatternProps {
  children: React.ReactNode;
}

export const BackgroundPattern: React.FC<BackgroundPatternProps> = ({ children }) => {
  return (
    <ImageBackground
      source={require('../../assets/prohelion-sixfold-pattern.png')}
      style={styles.container}
      imageStyle={styles.background}
    >
      <View style={styles.overlay}>
        {children}
      </View>
    </ImageBackground>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
  background: {
    opacity: 0.3,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(27, 27, 27, 0.95)',
  },
}); 
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  Alert,
  TextStyle,
  Image,
  Dimensions,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { theme } from '../theme';
import { validateLoginForm } from '../utils/validation';
import { login } from '../services/api';
import { saveApiConfig, getApiConfig, DEFAULT_SERVER_URL } from '../services/configService';
import { BackgroundPattern } from 'components/BackgroundPattern';

type RootStackParamList = {
  Login: undefined;
  Dashboard: undefined;
};

type Props = NativeStackScreenProps<RootStackParamList, 'Login'>;

interface LoginForm {
  username: string;
  password: string;
  serverUrl: string;
}

interface FormErrors {
  username?: string;
  password?: string;
  serverUrl?: string;
}

const { width } = Dimensions.get('window');
const LOGO_SIZE = Math.min(width * 0.4, 200); // 40% of screen width, max 200px

export const LoginScreen: React.FC<Props> = ({ navigation }) => {
  const [form, setForm] = useState<LoginForm>({
    username: '',
    password: '',
    serverUrl: DEFAULT_SERVER_URL,
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const loadConfig = async () => {
      const config = await getApiConfig();
      setForm(prev => ({ ...prev, serverUrl: config.serverUrl, username: config.username }));
    };
    loadConfig();
  }, []);

  const handleInputChange = (field: keyof LoginForm, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const handleLogin = async () => {
    const validation = validateLoginForm(form);
    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    setIsLoading(true);
    try {
      await saveApiConfig(form.serverUrl, form.username);
      await login(form.username, form.password);
      navigation.replace('Dashboard');
    } catch (error: any) {
      Alert.alert('Login Failed', error.message || 'An error occurred during login');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <BackgroundPattern>
      <SafeAreaView style={styles.container}>
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.keyboardAvoidingView}
        >
          <View style={styles.content}>
            <View style={styles.logoContainer}>
              <Image 
                source={require('../../assets/profinity-logo.png')}
                style={styles.logo}
                resizeMode="contain"
              />
            </View>

            <View style={styles.section}>
              <View style={styles.credentialsContainer}>
                <View style={styles.inputContainer}>
                  <Text style={styles.label}>Username</Text>
                  <TextInput
                    style={[styles.input, errors.username && styles.inputError]}
                    value={form.username}
                    onChangeText={(text: string) => handleInputChange('username', text)}
                    placeholder="Enter username"
                    autoCapitalize="none"
                    editable={!isLoading}
                  />
                  {errors.username && <Text style={styles.errorText}>{errors.username}</Text>}
                </View>

                <View style={styles.inputContainer}>
                  <Text style={styles.label}>Password</Text>
                  <TextInput
                    style={[styles.input, errors.password && styles.inputError]}
                    value={form.password}
                    onChangeText={(text: string) => handleInputChange('password', text)}
                    placeholder="Enter password"
                    secureTextEntry
                    editable={!isLoading}
                  />
                  {errors.password && <Text style={styles.errorText}>{errors.password}</Text>}
                </View>
              </View>
            </View>

            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Profinity Server Location</Text>
              <View style={styles.apiConfigContainer}>
                <View style={styles.apiConfigRow}>
                  <View style={styles.apiConfigItem}>
                    <Text style={styles.label}>Server URL</Text>
                    <TextInput
                      style={[styles.input, errors.serverUrl && styles.inputError]}
                      value={form.serverUrl}
                      onChangeText={(text: string) => handleInputChange('serverUrl', text)}
                      placeholder="Profinity server URL"
                      autoCapitalize="none"
                      editable={!isLoading}
                    />
                    {errors.serverUrl && <Text style={styles.errorText}>{errors.serverUrl}</Text>}
                  </View>
                </View>
              </View>
            </View>

            <TouchableOpacity
              style={[styles.button, isLoading && styles.buttonDisabled]}
              onPress={handleLogin}
              disabled={isLoading}
            >
              <Text style={styles.buttonText}>
                {isLoading ? 'Logging in...' : 'Login'}
              </Text>
            </TouchableOpacity>
          </View>
        </KeyboardAvoidingView>
      </SafeAreaView>
    </BackgroundPattern>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1
  },
  keyboardAvoidingView: {
    flex: 1,
  },
  content: {
    flex: 1,
    padding: theme.spacing.lg,
    justifyContent: 'center',
  },
  logoContainer: {
    width: '100%',
    alignItems: 'center',
    marginBottom: theme.spacing.xl,
  },
  logo: {
    width: LOGO_SIZE,
    height: LOGO_SIZE * 0.5, // Assuming 2:1 aspect ratio
  },
  section: {
    marginBottom: theme.spacing.xl,
  },
  sectionTitle: {
    ...theme.typography.h3,
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  apiConfigContainer: {
    backgroundColor: theme.colors.card,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  apiConfigRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: theme.spacing.md,
  },
  apiConfigItem: {
    flex: 1,
  },
  credentialsContainer: {
    backgroundColor: theme.colors.card,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  inputContainer: {
    marginBottom: theme.spacing.lg,
  },
  label: {
    ...theme.typography.body,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.sm,
  },
  input: {
    ...theme.typography.body,
    color: theme.colors.text,
    marginBottom: 15,
    fontSize: 16,
    backgroundColor: theme.colors.background,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  inputError: {
    borderColor: theme.colors.error,
  },
  errorText: {
    ...theme.typography.caption,
    color: theme.colors.error,
    marginTop: 5,
    fontSize: 14,
  },
  button: {
    backgroundColor: theme.colors.primary,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  buttonText: {
    ...theme.typography.body,
    color: theme.colors.text,
    fontWeight: '600' as TextStyle['fontWeight'],
  },
}); 
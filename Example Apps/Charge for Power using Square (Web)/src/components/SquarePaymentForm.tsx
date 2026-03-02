import React, { useEffect, useRef, useState } from 'react';
import { Box, Button, CircularProgress, Typography } from '@mui/material';

declare global {
  interface Window {
    Square: any;
  }
}

interface SquarePaymentFormProps {
  applicationId: string;
  locationId: string;
  amount: number;
  onPaymentSuccess: (nonce: string) => void;
  onPaymentError: (error: Error) => void;
}

const SquarePaymentForm: React.FC<SquarePaymentFormProps> = ({
  applicationId,
  locationId,
  amount,
  onPaymentSuccess,
  onPaymentError,
}) => {
  const payments = useRef<any>(null);
  const card = useRef<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const validateCredentials = () => {
      if (!applicationId || !locationId) {
        setError('Square credentials are missing');
        return false;
      }

      if (!applicationId.startsWith('sandbox-') && !applicationId.startsWith('sq0idp-')) {
        setError('Invalid Square Application ID format');
        return false;
      }

      return true;
    };

    const initializeSquare = async () => {
      try {
        if (!validateCredentials()) {
          setIsLoading(false);
          return;
        }

        if (!window.Square) {
          const script = document.createElement('script');
          script.src = 'https://web.squarecdn.com/v1/square.js';
          script.onload = initializeSquare;
          document.body.appendChild(script);
          return;
        }

        payments.current = window.Square.payments(applicationId, locationId);
        card.current = await payments.current.card();
        await card.current.attach('#card-container');
        setIsLoading(false);
      } catch (error) {
        setError('Failed to initialize Square payment form');
        onPaymentError(error as Error);
        setIsLoading(false);
      }
    };

    initializeSquare();

    return () => {
      if (card.current) {
        card.current.destroy();
      }
    };
  }, [applicationId, locationId, onPaymentError]);

  const handlePayment = async () => {
    try {
      setIsLoading(true);
      const result = await card.current.tokenize();
      if (result.status === 'OK') {
        onPaymentSuccess(result.token);
      } else {
        const errorMessage = result.errors?.[0]?.message || 'Payment failed';
        setError(errorMessage);
        onPaymentError(new Error(errorMessage));
      }
    } catch (error) {
      setError('Payment processing failed');
      onPaymentError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  if (error) {
    return (
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: 500, mx: 'auto', p: 2 }}>
      <Box id="card-container" sx={{ mb: 2, minHeight: 89 }} />
      <Button
        variant="contained"
        color="primary"
        onClick={handlePayment}
        fullWidth
        disabled={!card.current || isLoading}
      >
        {isLoading ? <CircularProgress size={24} /> : `Pay $${amount.toFixed(2)}`}
      </Button>
    </Box>
  );
};

export default SquarePaymentForm; 
import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress, Paper, Button, Dialog, DialogTitle, DialogContent, DialogActions, Snackbar, Alert } from '@mui/material';
import { getProhelionBMUData } from '../services/api';
import { createSquarePayment } from '../services/square';
import SquarePaymentForm from './SquarePaymentForm';
import { BMUData } from '../types/BMUData';
import '../styles/Home.scss';

interface ChargingSession {
  startCharge: number;
  endCharge: number | null;
  chargeDifference: number | null;
  startTime: number;
  endTime: number | null;
  durationHours: number | null;
  kWhConsumed: number | null;
}

const Home: React.FC = () => {
  const [data, setData] = useState<BMUData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCharging, setIsCharging] = useState(false);
  const [chargingSession, setChargingSession] = useState<ChargingSession | null>(null);
  const [paymentDialogOpen, setPaymentDialogOpen] = useState(false);
  const [paymentStatus, setPaymentStatus] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false,
    message: '',
    severity: 'success'
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getProhelionBMUData();
        setData(response as BMUData);
        setError(null);
      } catch (err) {
        setError('Failed to fetch Prohelion BMU data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    // Initial fetch
    fetchData();

    // Set up interval to fetch every second
    const intervalId = setInterval(fetchData, 1000);

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  const handleStartCharge = () => {
    if (data?.PackStateOfCharge.SOCAh) {
      const startValue = parseFloat(data.PackStateOfCharge.SOCAh);
      if (!isNaN(startValue)) {
        setChargingSession({
          startCharge: startValue,
          endCharge: null,
          chargeDifference: null,
          startTime: Date.now(),
          endTime: null,
          durationHours: null,
          kWhConsumed: null
        });
        setIsCharging(true);
      }
    }
  };

  const handleStopCharge = () => {
    if (data?.PackStateOfCharge.SOCAh && chargingSession) {
      const endValue = parseFloat(data.PackStateOfCharge.SOCAh);
      const endTime = Date.now();
      if (!isNaN(endValue)) {
        const difference = endValue - chargingSession.startCharge;
        const durationMs = endTime - chargingSession.startTime;
        const durationHours = durationMs / (1000 * 60 * 60); // Convert ms to hours
        
        // Calculate kWh: (Voltage × Current × Time) / 1000
        const voltage = parseFloat(data.PackVoltageCurrent.Voltage) / 1000; // Convert mV to V
        const current = parseFloat(data.PackVoltageCurrent.Current) / 1000; // Convert mA to A
        const kWhConsumed = Math.abs((voltage * current * durationHours) / 1000);
        
        setChargingSession({
          ...chargingSession,
          endCharge: endValue,
          chargeDifference: difference,
          endTime: endTime,
          durationHours: durationHours,
          kWhConsumed: kWhConsumed
        });
        setIsCharging(false);
      }
    }
  };

  const handleCreatePaymentRequest = () => {
    setPaymentDialogOpen(true);
  };

  const handlePaymentSuccess = async (nonce: string) => {
    try {
      if (!chargingSession?.kWhConsumed) {
        throw new Error('No charging session data available');
      }

      const amount = chargingSession.kWhConsumed; // $1 per kWh
      const note = `Charging session: ${chargingSession.startCharge.toFixed(3)}Ah to ${chargingSession.endCharge?.toFixed(3)}Ah`;

      await createSquarePayment(amount, note, nonce);
      
      setPaymentStatus({
        open: true,
        message: 'Payment processed successfully',
        severity: 'success'
      });
    } catch (error) {
      console.error('Payment error:', error);
      setPaymentStatus({
        open: true,
        message: 'Failed to process payment',
        severity: 'error'
      });
    } finally {
      setPaymentDialogOpen(false);
    }
  };

  const handlePaymentError = (error: Error) => {
    setPaymentStatus({
      open: true,
      message: error.message || 'Payment failed',
      severity: 'error'
    });
  };

  const handlePaymentCancel = () => {
    setPaymentDialogOpen(false);
  };

  const handleCloseSnackbar = () => {
    setPaymentStatus(prev => ({ ...prev, open: false }));
  };

  if (loading && !data) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  const formatValue = (value: string | undefined, isSOC: boolean = false) => {
    if (!value || value === 'NaN') return 'Not Available';
    const numValue = parseFloat(value);
    return isSOC ? numValue.toFixed(2) : (numValue / 1000).toFixed(2);
  };

  return (
    <div className="home">
      {error && (
        <Typography className="home__error">
          {error}
        </Typography>
      )}
      <div className="home__content">
        <Paper className="home__panel">
          <div className="home__data-box">
            <div className="home__data-grid">
              <div className="home__data-item">
                <Typography className="home__data-label">
                  Voltage
                </Typography>
                <Typography className="home__data-value">
                  {formatValue(data?.PackVoltageCurrent.Voltage)}
                  <span className="home__data-unit">V</span>
                </Typography>
              </div>
              <div className="home__data-item">
                <Typography className="home__data-label">
                  Current
                </Typography>
                <Typography className="home__data-value">
                  {formatValue(data?.PackVoltageCurrent.Current)}
                  <span className="home__data-unit">A</span>
                </Typography>
              </div>
            </div>
          </div>
          <div>
            <div className="home__data-box">
              <div className="home__data-grid">
                <div className="home__data-item">
                  <Typography className="home__data-label">
                    Battery SOC
                  </Typography>
                  <Typography className="home__data-value">
                    {formatValue(data?.PackStateOfCharge.SOCAh, true)}
                    <span className="home__data-unit">Ah</span>
                  </Typography>
                </div>
              </div>
            </div>
          </div>
        </Paper>
        <Paper className="home__panel">
          <div>
            {!isCharging ? (
              <Button
                variant="contained"
                color="primary"
                onClick={handleStartCharge}
                className="home__button"
              >
                Start Charge
              </Button>
            ) : (
              <Button
                variant="contained"
                color="secondary"
                onClick={handleStopCharge}
                className="home__button"
              >
                Stop Charge
              </Button>
            )}
            {chargingSession?.chargeDifference !== null && chargingSession && (
              <>
                <div className="home__data-box">
                  <Typography className="home__data-label">
                    Charge Session Summary
                  </Typography>
                  <div className="home__session-summary">
                    <Typography className="home__summary-text">
                      Start: {chargingSession.startCharge.toFixed(3)} Ah
                    </Typography>
                    <Typography className="home__summary-text">
                      End: {chargingSession.endCharge?.toFixed(3)} Ah
                    </Typography>
                    <Typography className="home__summary-text">
                      Duration: {chargingSession.durationHours?.toFixed(2)} hours
                    </Typography>
                    <Typography className="home__summary-highlight">
                      Charge Provided: {chargingSession.chargeDifference.toFixed(3)} Ah
                    </Typography>
                    <Typography className="home__summary-highlight">
                      Energy Consumed: {chargingSession.kWhConsumed?.toFixed(3)} kWh
                    </Typography>
                  </div>
                </div>
                <Button
                  variant="contained"
                  onClick={handleCreatePaymentRequest}
                  className="home__payment-button"
                >
                  Create Payment Request
                </Button>
              </>
            )}
          </div>
        </Paper>
      </div>

      <Dialog 
        open={paymentDialogOpen} 
        onClose={handlePaymentCancel}
        maxWidth="sm"
        fullWidth
        className="home__dialog"
      >
        <DialogTitle className="home__dialog-title">Process Payment</DialogTitle>
        <DialogContent>
          <Typography className="home__dialog-text">
            Energy Consumed: {chargingSession?.kWhConsumed?.toFixed(3)} kWh
          </Typography>
          <Typography className="home__dialog-text">
            Rate: $1.00 per kWh
          </Typography>
          <Typography className="home__dialog-amount">
            Total Amount: ${(chargingSession?.kWhConsumed || 0).toFixed(2)}
          </Typography>
          {chargingSession?.kWhConsumed && (
            <SquarePaymentForm
              applicationId={process.env.REACT_APP_SQUARE_APPLICATION_ID || ''}
              locationId={process.env.REACT_APP_SQUARE_LOCATION_ID || ''}
              amount={chargingSession.kWhConsumed}
              onPaymentSuccess={handlePaymentSuccess}
              onPaymentError={handlePaymentError}
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handlePaymentCancel}>Cancel</Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={paymentStatus.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={paymentStatus.severity}>
          {paymentStatus.message}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default Home; 
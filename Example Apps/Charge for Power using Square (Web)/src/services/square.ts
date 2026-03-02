import axios from 'axios';

const SQUARE_API_URL = 'https://connect.squareup.com/v2/payments';

export interface SquarePaymentRequest {
  source_id: string;
  amount_money: {
    amount: number;
    currency: string;
  };
  idempotency_key: string;
  note: string;
}

export const createSquarePayment = async (amount: number, note: string, cardNonce: string): Promise<any> => {
  try {
    const paymentRequest: SquarePaymentRequest = {
      source_id: cardNonce,
      amount_money: {
        amount: Math.round(amount * 100), // Convert to cents
        currency: 'USD'
      },
      idempotency_key: `payment_${Date.now()}`,
      note: note
    };

    const response = await axios.post(SQUARE_API_URL, paymentRequest, {
      headers: {
        'Authorization': `Bearer ${process.env.REACT_APP_SQUARE_ACCESS_TOKEN}`,
        'Content-Type': 'application/json'
      }
    });

    return response.data;
  } catch (error) {
    console.error('Error creating Square payment:', error);
    throw error;
  }
}; 
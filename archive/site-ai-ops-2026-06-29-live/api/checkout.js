const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const PRODUCTS = {
  transcript: {
    priceId: 'price_1TmkmV20aAs0tkSoBiqt1d9w',
    name: 'Transcript Content Pipeline',
  },
  obsidian: {
    priceId: 'price_1Tmkmt20aAs0tkSo2DJnlWPw',
    name: 'Obsidian KB Kit',
  },
};

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { product } = req.body;

  if (!product || !PRODUCTS[product]) {
    return res.status(400).json({ error: 'Invalid product' });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: PRODUCTS[product].priceId,
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `https://relaydept.com/download?session_id={CHECKOUT_SESSION_ID}&product=${product}`,
      cancel_url: 'https://relaydept.com',
      metadata: {
        product,
      },
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('Checkout error:', err.message);
    return res.status(500).json({ error: 'Failed to create checkout session' });
  }
};

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const FILES = {
  transcript: {
    filename: 'transcript-content-pipeline-v1.0.zip',
    path: 'downloads/transcript-content-pipeline-v1.0.zip',
  },
  obsidian: {
    filename: 'obsidian-kb-kit-v1.0.zip',
    path: 'downloads/obsidian-kb-kit-v1.0.zip',
  },
};

module.exports = async (req, res) => {
  const { session_id, product } = req.query;

  if (!session_id || !product || !FILES[product]) {
    return res.status(400).send('Invalid download link');
  }

  try {
    // Verify the session with Stripe
    const session = await stripe.checkout.sessions.retrieve(session_id);

    if (session.payment_status !== 'paid') {
      return res.status(403).send('Payment not completed');
    }

    // Accept if metadata matches OR if product query param is valid (for legacy payment links)
    const metaProduct = session.metadata?.product;
    if (metaProduct && metaProduct !== product) {
      return res.status(403).send('Product mismatch');
    }

    // Serve the file
    const file = FILES[product];
    const filePath = path.join(process.cwd(), file.path);

    if (!fs.existsSync(filePath)) {
      return res.status(404).send('File not found');
    }

    const fileBuffer = fs.readFileSync(filePath);
    res.setHeader('Content-Type', 'application/zip');
    res.setHeader('Content-Disposition', `attachment; filename="${file.filename}"`);
    res.setHeader('Content-Length', fileBuffer.length);
    return res.send(fileBuffer);
  } catch (err) {
    console.error('Download error:', err.message);
    return res.status(500).send('Download failed');
  }
};

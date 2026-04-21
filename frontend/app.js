const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

const API_URL = process.env.API_URL || "http://localhost:8000";

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch (err) {
    console.error(`FRONTEND ERROR: Could not POST to ${API_URL}/jobs - ${err.message}`);
    res.status(500).json({ job_id: null, error: err.message });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    console.error(`FRONTEND ERROR: Could not GET status from ${API_URL} - ${err.message}`);
    res.status(500).json({ status: "error", error: err.message });
  }
});

const PORT = 3000;
const HOST = '0.0.0.0';

app.listen(PORT, HOST, () => {
  console.log(`Frontend running on http://${HOST}:${PORT}`);
  console.log(`Target API: ${API_URL}`);
});

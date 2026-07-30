const express = require('express');
const { handleRagQuery } = require('./controllers/ragController');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Healthcheck Route
app.get('/health', (req, res) => {
    res.status(200).json({ status: "UP", service: "NodeJS-AI-Gateway" });
});

// Primary RAG Gateway Endpoint
app.post('/api/v1/query', handleRagQuery);

app.listen(PORT, () => {
    console.log(`Node.js Gateway running on port ${PORT}`);
});
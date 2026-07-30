const axios = require('axios');

/**
 * Handles inbound API requests, validates inputs, and bridges calls
 * to the Python SLM / Chroma DB microservice endpoint.
 */
exports.handleRagQuery = async (req, res) => {
    try {
        const { query } = req.body;

        if (!query || typeof query !== 'string') {
            return res.status(400).json({ error: "Property 'query' is required and must be a string." });
        }

        const pythonServiceUrl = process.env.PYTHON_AI_SERVICE_URL || 'http://localhost:8000/api/rag';
        
        const aiResponse = await axios.post(pythonServiceUrl, {
            prompt: query,
            top_k: 3
        }, {
            headers: { 'Content-Type': 'application/json' },
            timeout: 10000
        });

        return res.status(200).json({
            success: true,
            data: aiResponse.data.answer,
            telemetry: {
                tokens_used: aiResponse.data.tokens_used,
                model: aiResponse.data.model
            }
        });

    } catch (error) {
        console.error(`[RAG Gateway Error]: ${error.message}`);
        return res.status(500).json({
            success: false,
            error: "Failed to process RAG query through Python AI microservice."
        });
    }
};
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

// Chat API
export const chatAPI = {
    sendMessage: async (message) => {
        try {
            const response = await axios.post(`${API_URL}/chat/`, {
                message
            });
            return response.data;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    },

    sendMessageStream: async (message, onChunk, sessionId = 'default-session') => {
        const response = await fetch(`${API_URL}/chat/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, session_id: sessionId }),
        });
        if (!response.body) throw new Error('No response body');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let done = false;
        while (!done) {
            const { value, done: doneReading } = await reader.read();
            done = doneReading;
            if (value) {
                const chunk = decoder.decode(value, { stream: true });
                onChunk(chunk);
            }
        }
    },

    getFAQ: async () => {
        try {
            const response = await axios.get(`${API_URL}/faq/`);
            return response.data;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }
};

// Resume API
export const resumeAPI = {
    upload: async (formData) => {
        try {
            const response = await axios.post(`${API_URL}/resume`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            return response.data;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    },

    getResume: async () => {
        try {
            const response = await axios.get(`${API_URL}/resume`);
            return response.data;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    },

    generateQuestions: async () => {
        try {
            const response = await axios.post(`${API_URL}/resume/generate-questions`);
            return response.data;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    },

    getAnswer: async (id) => {
        try {
            const response = await axios.get(`${API_URL}/resume/answers/${id}`);
            return response.data;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    },

    saveAnswer: async (id, answer) => {
        try {
            const response = await axios.post(`${API_URL}/resume/questions/${id}/answer`, {
                answer
            });
            return response.data;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }
};
    

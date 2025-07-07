import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const chatAPI = {
    // 기존 전체 응답 방식 (axios)
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

    // 스트리밍 응답 방식 (fetch + ReadableStream)
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
    },

    getHistory: async () => {
        try {
            const response = await axios.get(`${API_URL}/history/`);
            return response.data;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }
};

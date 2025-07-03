import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

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

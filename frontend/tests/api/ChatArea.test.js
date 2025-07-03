import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import React from 'react';
import ChatArea from 'src/ChatArea';

// Mock API service
jest.mock('src/api/service', () => {
  const mockSendMessage = jest.fn();
  const mockGetFAQ = jest.fn();
  const mockGetHistory = jest.fn();
  
  return {
    chatAPI: {
      sendMessage: mockSendMessage,
      getFAQ: mockGetFAQ,
      getHistory: mockGetHistory
    }
  };
});

describe('ChatArea Integration Tests', () => {
  let mockChatAPI;
  
  beforeEach(() => {
    // Reset all mocks before each test
    mockChatAPI = require('src/api/service').chatAPI;
    mockChatAPI.sendMessage.mockClear();
    mockChatAPI.getFAQ.mockClear();
    mockChatAPI.getHistory.mockClear();

    // Mock API responses
    mockChatAPI.sendMessage.mockResolvedValue({
      answer: 'Test response from backend'
    });
    mockChatAPI.getFAQ.mockResolvedValue({
      faqs: [
        { question: 'Test FAQ', answer: 'Test answer' }
      ]
    });
    mockChatAPI.getHistory.mockResolvedValue({
      messages: [
        { from: 'bot', text: 'Previous message' }
      ]
    });
  });

  test('sends message to backend', async () => {
    render(<ChatArea chatAPI={mockChatAPI} />);
    
    // Type message
    const input = screen.getByRole('textbox');
    await act(async () => {
      await userEvent.type(input, 'test message');
      fireEvent.click(screen.getByText('전송'));
    });
    
    // Wait for response
    await waitFor(() => {
      expect(screen.getByText('Test response from backend')).toBeInTheDocument();
    });
    
    // Verify API call
    expect(mockChatAPI.sendMessage).toHaveBeenCalledWith('test message');
  });

  test('loads FAQ from backend', async () => {
    render(<ChatArea chatAPI={mockChatAPI} />);
    
    // Click FAQ button
    await act(async () => {
      fireEvent.click(screen.getByText('FAQ'));
    });
    
    // Wait for FAQ to be loaded
    await waitFor(() => {
      expect(mockChatAPI.getFAQ).toHaveBeenCalled();
    });
  });

  test('loads chat history on mount', async () => {
    render(<ChatArea chatAPI={mockChatAPI} />);
    
    // Wait for history to be loaded
    await waitFor(() => {
      expect(mockChatAPI.getHistory).toHaveBeenCalled();
      expect(screen.getByText('Previous message')).toBeInTheDocument();
    });
  });
});

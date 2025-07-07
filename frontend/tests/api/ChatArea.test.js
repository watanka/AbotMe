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
  test('답변이 chunk 단위로 누적되어 출력된다 (streaming)', async () => {
    // 스트리밍 mock 함수 준비
    const chunks = ['안', '녕', '하', '세', '요'];
    const sendMessageStream = jest.fn((msg, onChunk) => {
      return new Promise((resolve) => {
        (async () => {
          for (const chunk of chunks) {
            await new Promise(res => setTimeout(res, 1));
            onChunk(chunk);
          }
          resolve();
        })();
      });
    });
    const chatAPI = {
      sendMessageStream,
      getFAQ: jest.fn(),
      getHistory: jest.fn().mockResolvedValue({ messages: [] }),
    };
    render(<ChatArea chatAPI={chatAPI} />);
    // 사용자 입력
    const input = screen.getByPlaceholderText('메시지를 입력하세요...');
    await act(async () => {
      await userEvent.type(input, '테스트');
      fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });
    });
    // bot 메시지가 점점 길어지는지 확인
    let expected = '';
    for (const chunk of chunks) {
      expected += chunk;
      await waitFor(() => {
        const botMsgs = Array.from(document.querySelectorAll('.msg-bot'));
        expect(botMsgs[botMsgs.length - 1]).toHaveTextContent(expected);
      }, { timeout: 500 });
    }
  });
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

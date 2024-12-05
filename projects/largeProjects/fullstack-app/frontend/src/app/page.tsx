'use client';

import { useState, useEffect, useCallback, useRef } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface Size {
  width: number;
  height: number;
}

interface Position {
  x: number;
  y: number;
}

export default function Home() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [size, setSize] = useState<Size>({ width: 384, height: 600 });
  const [isResizing, setIsResizing] = useState(false);
  const initialMousePos = useRef<Position>({ x: 0, y: 0 });
  const initialSize = useRef<Size>({ width: 0, height: 0 });

  // Auto scroll to bottom when messages change
  useEffect(() => {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }, [messages]);

  // Handle resize
  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (isResizing) {
      e.preventDefault();
      
      // Calculate the difference from initial position
      const deltaX = initialMousePos.current.x - e.clientX;
      const deltaY = initialMousePos.current.y - e.clientY;
      
      // Update size based on the delta
      const newWidth = Math.max(320, Math.min(800, initialSize.current.width + deltaX));
      const newHeight = Math.max(400, Math.min(800, initialSize.current.height + deltaY));
      
      setSize({ width: newWidth, height: newHeight });
    }
  }, [isResizing]);

  const handleMouseUp = useCallback(() => {
    setIsResizing(false);
  }, []);

  const startResize = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    const chatBox = document.getElementById('chat-box');
    if (chatBox) {
      initialMousePos.current = { x: e.clientX, y: e.clientY };
      initialSize.current = { width: chatBox.offsetWidth, height: chatBox.offsetHeight };
      setIsResizing(true);
    }
  }, []);

  useEffect(() => {
    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isResizing, handleMouseMove, handleMouseUp]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    // Add user message to history
    const userMessage: Message = { role: 'user', content: message };
    setMessages(prev => [...prev, userMessage]);
    
    try {
      const res = await fetch('http://localhost:5001/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Credentials': 'include',
        },
        body: JSON.stringify({ message }),
      });
      
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      
      const data = await res.json();
      if (data.status === 'error') {
        throw new Error(data.message);
      }
      
      // Add assistant message to history
      const assistantMessage: Message = { role: 'assistant', content: data.message };
      setMessages(prev => [...prev, assistantMessage]);
      setMessage(''); // Clear input after sending
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
      setError(errorMessage);
    }
    setIsLoading(false);
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-100 to-white relative">
      {/* Main content */}
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">Welcome to your AI Assitant</h1>
        <p className="text-gray-600">Ask the bot any question you have about your work and it will help out.</p>
      </div>

      {/* Chat button */}
      <button
        onClick={() => setIsChatOpen(true)}
        className={`fixed bottom-6 right-6 z-50 ${isChatOpen ? 'hidden' : 'flex'} items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-full shadow-lg hover:bg-blue-700 transition-colors`}
      >
        <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center">
          <span className="text-blue-600 text-xl">💬</span>
        </div>
        <span>Need help?</span>
      </button>

      {/* Chat interface */}
      {isChatOpen && (
        <div
          id="chat-box"
          className="fixed bottom-6 right-6 bg-white rounded-lg shadow-2xl flex flex-col z-50"
          style={{ 
            width: size.width,
            height: size.height,
            overflow: 'hidden',
            minWidth: '320px',
            minHeight: '400px',
            maxWidth: '800px',
            maxHeight: '800px'
          }}
        >
          {/* Resize handle */}
          <div 
            className="absolute top-0 left-0 w-4 h-4 cursor-nw-resize z-50 group"
            onMouseDown={startResize}
            style={{
              background: 'linear-gradient(315deg, transparent 50%, #CBD5E0 50%)',
            }}
          >
            <div className="absolute inset-0 bg-blue-500 opacity-0 group-hover:opacity-20 transition-opacity" />
          </div>

          {/* Chat header */}
          <div className="flex justify-between items-center p-4 border-b bg-white">
            <div className="w-4" /> {/* Spacer for resize handle */}
            <h2 className="text-lg font-semibold text-gray-800">AI Assistant</h2>
            <button
              onClick={() => setIsChatOpen(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>

          {/* Chat messages */}
          <div
            id="chat-container"
            className="flex-grow overflow-y-auto p-4 space-y-4"
            style={{ resize: 'none' }}
          >
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-blue-100'
                      : 'bg-gray-100'
                  }`}
                >
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Input form */}
          <div className="border-t p-4 bg-white">
            <form onSubmit={handleSubmit} className="space-y-2">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your question here..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
              
              <button
                type="submit"
                disabled={isLoading || !message.trim()}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-400"
              >
                {isLoading ? 'Processing...' : 'Send'}
              </button>
            </form>

            {error && (
              <div className="mt-2 p-2 text-sm bg-red-50 rounded border border-red-200">
                <p className="text-red-700">{error}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </main>
  );
}

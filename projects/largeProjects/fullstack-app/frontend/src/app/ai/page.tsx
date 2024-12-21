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
  const [size, setSize] = useState<Size>({ width: Math.min(800, window.innerWidth - 64), height: Math.min(600, window.innerHeight - 200) });
  const [isResizing, setIsResizing] = useState(false);
  const initialMousePos = useRef<Position>({ x: 0, y: 0 });
  const initialSize = useRef<Size>({ width: 0, height: 0 });

  useEffect(() => {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    const handleResize = () => {
      setSize(prev => ({
        width: Math.min(prev.width, window.innerWidth - 64),
        height: Math.min(prev.height, window.innerHeight - 200)
      }));
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (isResizing) {
      e.preventDefault();
      const deltaX = initialMousePos.current.x - e.clientX;
      const deltaY = initialMousePos.current.y - e.clientY;
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
    if (!message.trim()) return;
    
    setIsLoading(true);
    setError('');
    
    const userMessage: Message = { role: 'user', content: message };
    setMessages(prev => [...prev, userMessage]);
    
    try {
      const res = await fetch('http://localhost:5001/api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'X-Session-ID': 'default'
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
      
      const assistantMessage: Message = { 
        role: 'assistant', 
        content: typeof data.message === 'string' ? data.message : JSON.stringify(data.message)
      };
      setMessages(prev => [...prev, assistantMessage]);
      setMessage('');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
      setError(errorMessage);
    }
    setIsLoading(false);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-background-color to-white p-4">
      <div className="container" style={{ animation: 'fadeIn 0.5s ease-out' }}>
        <div className="card">
          <h1 className="text-4xl font-bold mb-8">AI Assistant</h1>
          <div 
            id="chat-box"
            className="relative bg-white rounded-xl shadow-lg overflow-hidden mx-auto"
            style={{ 
              width: '100%',
              maxWidth: size.width,
              height: size.height,
              minHeight: '400px',
            }}
          >
            <div 
              className="absolute top-0 left-0 w-4 h-4 cursor-nw-resize z-10"
              onMouseDown={startResize}
            >
              <div className="w-full h-full bg-gradient-to-br from-gray-200 to-transparent opacity-50 hover:opacity-100 transition-opacity" />
            </div>
            
            <div 
              id="chat-container"
              className="h-[calc(100%-72px)] overflow-y-auto p-6 space-y-4"
            >
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  style={{ animation: 'fadeIn 0.3s ease-out' }}
                >
                  <div
                    className={`max-w-[80%] p-4 rounded-2xl ${
                      msg.role === 'user'
                        ? 'bg-gradient-to-r from-primary-color to-secondary-color text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content)}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 p-4 rounded-2xl animate-pulse">
                    Thinking... 
                  </div>
                </div>
              )}
              {error && (
                <div className="text-error-color text-center p-2 rounded-lg bg-red-50">
                  {error}
                </div>
              )}
            </div>
            
            <form 
              onSubmit={handleSubmit}
              className="absolute bottom-0 left-0 right-0 border-t border-gray-100 p-4 bg-white"
            >
              <div className="flex gap-4">
                <input
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder=" Ask me anything..."
                  className="flex-1"
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  className="btn-primary whitespace-nowrap"
                  disabled={isLoading}
                >
                  Send 
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  );
}

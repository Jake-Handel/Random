'use client';

import { useState } from 'react';

export default function Home() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    try {
      const res = await fetch('http://localhost:5001/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
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
      
      setResponse(data.message);
      setMessage(''); // Clear input after sending
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
      setError(errorMessage);
      setResponse('');
    }
    setIsLoading(false);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-blue-100 to-white">
      <div className="text-center space-y-6 w-full max-w-2xl px-4">
        <h1 className="text-6xl font-bold text-gray-800">
          AI Assistant
        </h1>
        <p className="text-xl text-gray-600">
          Ask me anything!
        </p>
        
        <form onSubmit={handleSubmit} className="space-y-4 mt-8">
          <div className="flex flex-col space-y-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your question here..."
              className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>
          
          <button
            type="submit"
            disabled={isLoading || !message.trim()}
            className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-400"
          >
            {isLoading ? 'Processing...' : 'Ask AI'}
          </button>
        </form>

        {error && (
          <div className="mt-8 p-4 bg-red-50 rounded-lg shadow-md border border-red-200">
            <h2 className="text-lg font-semibold mb-2 text-red-600">Error:</h2>
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {response && (
          <div className="mt-8 p-4 bg-white rounded-lg shadow-md">
            <h2 className="text-lg font-semibold mb-2">Response:</h2>
            <p className="text-gray-700 whitespace-pre-wrap">{response}</p>
          </div>
        )}

        <div className="mt-12 text-sm text-gray-500">
          Powered by Gemini AI
        </div>
      </div>
    </main>
  );
}

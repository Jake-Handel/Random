'use client';

import React, { useState } from 'react';

export default function TodoPage() {
    const [todos, setTodos] = useState<string[]>([]);
    const [input, setInput] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const addTodo = async () => {
        if (input.trim()) {
            setIsLoading(true);
            setError(null); // Reset error state
            try {
                const response = await fetch('http://localhost:5001/todo', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ todo: input }),
                });

                if (response.ok) {
                    setTodos(prev => [...prev, input.trim()]);
                    setInput('');
                } else {
                    const errorData = await response.json();
                    setError(errorData.message || 'Failed to add todo.');
                }
            } catch (error) {
                console.error('Error adding todo:', error);
                setError('An error occurred while adding the todo.');
            } finally {
                setIsLoading(false);
            }
        }
    };

    const removeTodo = (index: number) => {
        const newTodos = todos.filter((_, i) => i !== index);
        setTodos(newTodos);
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            addTodo();
        }
    };

    return (
        <div className="container" style={{ animation: 'fadeIn 0.5s ease-out' }}>
            <div className="card">
                <h1 className="text-4xl font-bold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-primary-color to-secondary-color">
                    Todo List
                </h1>
                <div className="flex gap-4 mb-8">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="✨ What's next on your list?"
                        className="flex-1 text-lg"
                        autoFocus
                        disabled={isLoading}
                    />
                    <button 
                        onClick={addTodo}
                        className="btn-primary px-6"
                        disabled={isLoading}
                    >
                        {isLoading ? 'Adding...' : 'Add ✨'}
                    </button>
                </div>
                {error && (
                    <p className="text-red-500 text-center my-4">{error}</p>
                )}
                {todos.length === 0 ? (
                    <p className="text-center text-gray-500 my-8 animate-pulse">
                        Your todo list is empty. Time to add some tasks! 🚀
                    </p>
                ) : (
                    <ul className="space-y-4">
                        {todos.map((todo, index) => (
                            <li 
                                key={index} 
                                className="todo-item flex items-center justify-between"
                                style={{ animation: 'fadeIn 0.3s ease-out' }}
                            >
                                <span className="flex-1 text-gray-700">{todo}</span>
                                <button 
                                    onClick={() => removeTodo(index)}
                                    className="btn-danger ml-4"
                                    aria-label="Remove todo"
                                >
                                    Remove ×
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}
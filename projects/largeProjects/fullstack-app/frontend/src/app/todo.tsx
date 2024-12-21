import React, { useState } from 'react';

const Todo = () => {
    const [todos, setTodos] = useState<string[]>([]);
    const [input, setInput] = useState<string>('');

    const addTodo = () => {
        if (input) {
            setTodos([...todos, input]);
            setInput('');
        }
    };

    const removeTodo = (index: number) => {
        const newTodos = todos.filter((_, i) => i !== index);
        setTodos(newTodos);
    };

    return (
        <div>
            <h1>Todo List</h1>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Add a new todo"
            />
            <button onClick={addTodo}>Add Todo</button>
            <ul>
                {todos.map((todo, index) => (
                    <li key={index}>
                        {todo} <button onClick={() => removeTodo(index)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Todo;
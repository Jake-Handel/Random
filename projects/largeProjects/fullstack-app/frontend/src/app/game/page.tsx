'use client';

import React, { useState } from 'react';

const TicTacToe = () => {
    const [board, setBoard] = useState<string[]>(Array(9).fill(null));
    const [isXNext, setIsXNext] = useState<boolean>(true);
    const [winner, setWinner] = useState<string | null>(null);
    const [isDraw, setIsDraw] = useState<boolean>(false);

    const handleClick = (index: number) => {
        if (board[index] || winner) return; // Ignore if square is already filled or game is won

        const newBoard = board.slice();
        newBoard[index] = isXNext ? 'X' : 'O';
        setBoard(newBoard);
        setIsXNext(!isXNext);
        checkWinner(newBoard);
    };

    const checkWinner = (squares: string[]) => {
        const lines = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ];

        for (let i = 0; i < lines.length; i++) {
            const [a, b, c] = lines[i];
            if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
                setWinner(squares[a]);
                return;
            }
        }

        // Check for draw
        if (!squares.includes(null)) {
            setIsDraw(true);
        }
    };

    const resetGame = () => {
        setBoard(Array(9).fill(null));
        setIsXNext(true);
        setWinner(null);
        setIsDraw(false);
    };

    return (
        <div className="container" style={{ animation: 'fadeIn 0.5s ease-out' }}>
            <div className="card">
                <h1 className="text-4xl font-bold mb-8">Tic Tac Toe</h1>
                <div className="flex mb-4">
                    <p className="text-2xl mr-4">Current Turn: {isXNext ? 'X' : 'O'}</p>
                </div>
                <table className="mx-auto border-collapse border border-gray-800">
                    <tbody>
                        {[0, 1, 2].map(row => (
                            <tr key={row}>
                                {[0, 1, 2].map(col => {
                                    const index = row * 3 + col;
                                    return (
                                        <td key={col} className="border border-gray-700">
                                            <button
                                                onClick={() => handleClick(index)}
                                                className="w-24 h-24 text-4xl font-bold bg-white hover:bg-gray-200 transition duration-300"
                                            >
                                                {board[index]}
                                            </button>
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
                {winner && <p className="text-2xl mt-4">Winner: {winner}</p>}
                {isDraw && <p className="text-2xl mt-4">It's a draw!</p>}
                <button onClick={resetGame} className="btn-primary mt-4">
                    Reset Game
                </button>
            </div>
        </div>
    );
};

export default function GamePage() {
    return <TicTacToe />;
}
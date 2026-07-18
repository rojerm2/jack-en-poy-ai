import ScoreBoard from '../components/ScoreBoard';
import ResultCard from '../components/ResultCard';
import MoveButton from '../components/MoveButton';
import Footer from '../components/Footer';
import Header from '../components/Header';
import { playGame } from '../services/gameService';
import { useState } from 'react';
import type { GameResult, Move } from '../types/game';

export default function HomePage() {
    const [playerMove, setPlayerMove] = useState<Move | null>(null);
    const [computerMove, setComputerMove] = useState<Move | null>(null);
    const [result, setResult] = useState<GameResult | null>(null);
    const [playerScore, setPlayerScore] = useState(0);
    const [computerScore, setComputerScore] = useState(0);
    const [draws, setDraws] = useState(0);
    const [loading, setLoading] = useState(false);

    const handlePlay = async (move: Move) => {
        setLoading(true);
        try {
            const response = await playGame(move);

            const game = response.data;

            setPlayerMove(game.playerMove);
            setComputerMove(game.computerMove);
            setResult(game.result);

            switch (game.result) {
                case 'PLAYER_WIN':
                    setPlayerScore((score) => score + 1);
                    break;

                case 'COMPUTER_WIN':
                    setComputerScore((score) => score + 1);
                    break;

                case 'DRAW':
                    setDraws((score) => score + 1);
                    break;
            }
        } catch (error) {
            console.error(error);

            alert('Unable to play the game.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="min-h-screen bg-gray-100">
            <div className="mx-auto max-w-4xl p-8">
                <Header />
                <ScoreBoard player={playerScore} computer={computerScore} draw={draws} />
                <ResultCard playerMove={playerMove} computerMove={computerMove} result={result} />
                <div className="mt-8 flex justify-center gap-4">
                    <MoveButton move="ROCK" onClick={handlePlay} disabled={loading} />
                    <MoveButton move="PAPER" onClick={handlePlay} disabled={loading} />
                    <MoveButton move="SCISSORS" onClick={handlePlay} disabled={loading} />
                </div>
                <Footer />
            </div>
        </main>
    );
}

// import { useState } from "react";
// import type { GameResult, Move } from "../types/game";

// // const [playerMove, setPlayerMove] = useState<Move | null>(null);

// // const [computerMove, setComputerMove] = useState<Move | null>(null);

// // const [result, setResult] = useState<GameResult | null>(null);

// // const [playerScore, setPlayerScore] = useState(0);

// // const [computerScore, setComputerScore] = useState(0);

// // const [draws, setDraws] = useState(0);

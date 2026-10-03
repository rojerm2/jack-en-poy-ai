import { useEffect, useRef, useState } from 'react';
import ScoreBoard from '../components/ScoreBoard';
import RoundArena from '../components/RoundArena';
import MoveButton from '../components/MoveButton';
import Footer from '../components/Footer';
import Header from '../components/Header';
import { playGame } from '../services/gameService';
import { waitForReveal } from '../utils/roundAnimation';
import type { GameRound, Move } from '../types/game';

export default function HomePage() {
    const [game, setGame] = useState<GameRound | null>(null);
    const [score, setScore] = useState({ player: 0, computer: 0, draw: 0 });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const activeRound = useRef<AbortController | null>(null);

    useEffect(() => () => activeRound.current?.abort(), []);

    const handlePlay = async (move: Move) => {
        if (activeRound.current) return;
        const controller = new AbortController();
        activeRound.current = controller;
        setLoading(true);
        setGame(null);
        setError('');
        try {
            const [response] = await Promise.all([playGame(move, controller.signal), waitForReveal(controller.signal)]);
            if (controller.signal.aborted) return;
            setGame(response.data);
            setScore(previous => ({
                player: previous.player + Number(response.data.result === 'PLAYER_WIN'),
                computer: previous.computer + Number(response.data.result === 'COMPUTER_WIN'),
                draw: previous.draw + Number(response.data.result === 'DRAW'),
            }));
        } catch {
            if (!controller.signal.aborted) setError('Unable to play this round. Check that the game API is running and try again.');
        } finally {
            if (!controller.signal.aborted) {
                setLoading(false);
                activeRound.current = null;
            }
            controller.abort();
        }
    };

    return (
        <main className="game-shell">
            <Header />
            <ScoreBoard {...score} />
            <RoundArena active={loading} game={game} />
            <div className="move-controls" aria-label="Choose your move">
                {(['ROCK', 'PAPER', 'SCISSORS'] as Move[]).map(move => <MoveButton key={move} move={move} onClick={handlePlay} disabled={loading} />)}
            </div>
            {error && <p className="error-message" role="alert">{error}</p>}
            <Footer />
        </main>
    );
}

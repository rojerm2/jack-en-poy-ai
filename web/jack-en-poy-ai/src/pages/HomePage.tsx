import { useCallback, useEffect, useRef, useState } from 'react';
import ScoreBoard from '../components/ScoreBoard';
import RoundArena from '../components/RoundArena';
import ResultCard from '../components/ResultCard';
import RoundHistory from '../components/RoundHistory';
import MoveButton from '../components/MoveButton';
import Footer from '../components/Footer';
import Header from '../components/Header';
import { playGame, startNewGame } from '../services/gameService';
import { waitForReveal } from '../utils/roundAnimation';
import type { GameRound, Move } from '../types/game';

export default function HomePage() {
    const [game, setGame] = useState<GameRound | null>(null);
    const [score, setScore] = useState({ player: 0, computer: 0, draw: 0 });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [history, setHistory] = useState<GameRound[]>([]);
    const activeRound = useRef<AbortController | null>(null);

    useEffect(() => () => activeRound.current?.abort(), []);

    const handlePlay = useCallback(async (move: Move) => {
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
            setHistory(previous => [response.data, ...previous].slice(0, 6));
            setScore(previous => ({
                player: previous.player + Number(response.data.result === 'PLAYER_WIN'),
                computer: previous.computer + Number(response.data.result === 'COMPUTER_WIN'),
                draw: previous.draw + Number(response.data.result === 'DRAW'),
            }));
        } catch (error) {
            if (!controller.signal.aborted) console.warn('Round failed:', error instanceof Error ? error.message : 'Unknown request error');
            if (!controller.signal.aborted) setError('Unable to play this round. Check that the game API is running and try again.');
        } finally {
            if (!controller.signal.aborted) {
                setLoading(false);
                activeRound.current = null;
            }
            controller.abort();
        }
    }, []);

    useEffect(() => {
        const onKey = (event: KeyboardEvent) => {
            const target = event.target;
            if (event.repeat || event.ctrlKey || event.metaKey || event.altKey ||
                (target instanceof HTMLElement && (target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName)))) return;
            const move = ({ r: 'ROCK', p: 'PAPER', s: 'SCISSORS' } as Record<string, Move>)[event.key.toLowerCase()];
            if (move) { event.preventDefault(); void handlePlay(move); }
        };
        window.addEventListener('keydown', onKey);
        return () => window.removeEventListener('keydown', onKey);
    }, [handlePlay]);

    const handleNewGame = () => {
        if (activeRound.current) return;
        startNewGame();
        setScore({ player: 0, computer: 0, draw: 0 });
        setGame(null);
        setHistory([]);
        setError('');
    };

    return (
        <main className="game-shell">
            <Header />
            <div className="session-toolbar"><span>THIS SESSION</span><button onClick={handleNewGame} disabled={loading}>New game</button></div>
            <ScoreBoard {...score} />
            <RoundArena active={loading} game={game} />
            <div className="move-controls" aria-label="Choose your move">
                {(['ROCK', 'PAPER', 'SCISSORS'] as Move[]).map(move => <MoveButton key={move} move={move} onClick={handlePlay} disabled={loading} />)}
            </div>
            <p className="keyboard-hint">Or use <kbd>R</kbd>, <kbd>P</kbd>, <kbd>S</kbd> on your keyboard.</p>
            {!loading && <ResultCard game={game} />}
            {error && <p className="error-message" role="alert">{error}</p>}
            <RoundHistory rounds={history} />
            <Footer />
        </main>
    );
}

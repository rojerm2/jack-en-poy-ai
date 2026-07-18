import type { GameResult, Move } from '../types/game';

interface Props {
    playerMove: Move | null;
    computerMove: Move | null;
    result: GameResult | null;
}

export default function ResultCard({ playerMove, computerMove, result }: Props) {
    return (
        <div className="mt-8 rounded-xl bg-white p-6 shadow">
            <h2 className="mb-4 text-xl font-semibold">Last Round</h2>

            <p>Player : {playerMove ?? '-'}</p>

            <p>Computer : {computerMove ?? '-'}</p>

            <p>Result : {result ?? 'Waiting...'}</p>
        </div>
    );
}

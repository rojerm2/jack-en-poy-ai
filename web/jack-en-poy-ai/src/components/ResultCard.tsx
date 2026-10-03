import type { GameRound } from '../types/game';

interface Props { game: GameRound | null; }

export default function ResultCard({ game }: Props) {
    const prediction = game?.prediction;
    const ml = prediction?.strategy === 'ML';
    const repetition = prediction?.strategy === 'ADAPTIVE';
    return <section className="strategy-card" aria-label="Computer strategy">
        <span className={`strategy-dot ${ml || repetition ? 'strategy-ml' : ''}`} aria-hidden="true" />
        <div><strong>{ml ? 'Playing your pattern' : repetition ? 'Countering repeated moves' : 'Random play'}</strong>
            <p>{ml ? `Predicted ${prediction.predictedMove?.toLowerCase()} · ${Math.round((prediction.confidence ?? 0) * 100)}% model confidence` :
                repetition ? `Your last three moves were ${prediction.predictedMove?.toLowerCase()}. Expecting another ${prediction.predictedMove?.toLowerCase()}.` :
                !game || prediction?.fallbackReason === 'insufficient_history' ? 'Three completed moves give the model a starting point.' : 'Prediction is unavailable. The game keeps going.'}</p>
            {ml && <small>Classifier confidence is not a guaranteed win rate.</small>}
        </div>
    </section>;
}

import type { GameRound } from '../types/game';

interface Props { game: GameRound | null; }

export default function ResultCard({ game }: Props) {
    const prediction = game?.prediction;
    return <section className="strategy-card" aria-label="Computer strategy">
        <span className={`strategy-dot ${prediction?.strategy === 'ML' ? 'strategy-ml' : ''}`} aria-hidden="true" />
        <div><strong>{prediction?.strategy === 'ML' ? 'Playing your pattern' : 'Random play'}</strong>
            <p>{prediction?.strategy === 'ML' ? `Predicted ${prediction.predictedMove?.toLowerCase()} · ${Math.round((prediction.confidence ?? 0) * 100)}% model confidence` :
                !game || prediction?.fallbackReason === 'insufficient_history' ? 'Three completed moves give the model a starting point.' : 'Prediction is unavailable. The game keeps going.'}</p>
            {prediction?.strategy === 'ML' && <small>Classifier confidence is not a guaranteed win rate.</small>}
        </div>
    </section>;
}

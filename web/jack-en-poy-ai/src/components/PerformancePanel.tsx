import type { SessionAnalytics } from '../types/game';

const percent = (value: number | null) => value === null ? '—' : `${Math.round(value * 100)}%`;

export default function PerformancePanel({ analytics }: { analytics: SessionAnalytics | null }) {
    if (!analytics) return null;
    return <details className="performance-panel"><summary>Session statistics <span>{analytics.totalRounds} rounds</span></summary>
        <dl className="metric-grid">
            <div><dt>ML prediction accuracy</dt><dd>{percent(analytics.predictionAccuracy)}</dd><small>{analytics.predictionsCorrect} correct / {analytics.mlRounds} predictions</small></div>
            <div><dt>Computer wins · ML</dt><dd>{percent(analytics.mlWinRate)}</dd><small>{analytics.mlRounds} rounds using predictions</small></div>
            <div><dt>Computer wins · random</dt><dd>{percent(analytics.randomWinRate)}</dd><small>{analytics.randomRounds} random rounds</small></div>
            {analytics.adaptiveRounds > 0 && <div><dt>Computer wins · repetition</dt><dd>{percent(analytics.adaptiveWinRate)}</dd><small>{analytics.adaptiveRounds} rounds countering repeated moves</small></div>}
        </dl>
        <div className="move-distribution" aria-label="Your move distribution">{(['ROCK', 'PAPER', 'SCISSORS'] as const).map(move => <div key={move}><span>{move.toLowerCase()}</span><meter min="0" max={analytics.totalRounds || 1} value={analytics.moveCounts[move]} aria-label={`${move.toLowerCase()} frequency`} /><span>{analytics.moveCounts[move]}</span></div>)}</div>
        <p>Rates describe different rounds in this session, so this is not a controlled comparison. No predictions yet is shown as —.</p>
    </details>;
}

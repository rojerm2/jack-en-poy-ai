import { render, screen } from '@testing-library/react';
import { expect, it } from 'vitest';
import PerformancePanel from './PerformancePanel';
import type { SessionAnalytics } from '../types/game';

const empty: SessionAnalytics = { totalRounds: 0, playerWins: 0, computerWins: 0, draws: 0, adaptiveRounds: 0, adaptiveWinRate: null, mlRounds: 0, randomRounds: 0, predictionsCorrect: 0, predictionAccuracy: null, mlWinRate: null, randomWinRate: null, averageConfidence: null, moveCounts: { ROCK: 0, PAPER: 0, SCISSORS: 0 } };

it('keeps absent predictions distinct from zero accuracy', () => {
    render(<PerformancePanel analytics={empty} />);
    expect(screen.getAllByText('—')).toHaveLength(3);
    expect(screen.getByText('0 correct / 0 predictions')).toBeInTheDocument();
});

it('renders observed rates and separate sample counts', () => {
    render(<PerformancePanel analytics={{ ...empty, totalRounds: 5, mlRounds: 2, randomRounds: 3, predictionsCorrect: 1, predictionAccuracy: .5, mlWinRate: .5, randomWinRate: 1/3 }} />);
    expect(screen.getByText('1 correct / 2 predictions')).toBeInTheDocument();
    expect(screen.getByText('3 random rounds')).toBeInTheDocument();
    expect(screen.getByText('33%')).toBeInTheDocument();
});


it('shows repetition rounds separately from model accuracy and random play', () => {
    render(<PerformancePanel analytics={{ ...empty, totalRounds: 4, randomRounds: 3, adaptiveRounds: 1, adaptiveWinRate: 1 }} />);
    expect(screen.getByText('Computer wins · repetition')).toBeInTheDocument();
    expect(screen.getByText('1 round countering repeated moves')).toBeInTheDocument();
    expect(screen.getByText('0 correct / 0 predictions')).toBeInTheDocument();
    expect(screen.getByText('3 random rounds')).toBeInTheDocument();
});

import { expect, it, vi, afterEach } from 'vitest';
import { DemoGame } from './demoGame';
import type { Move } from '../types/game';

afterEach(() => vi.restoreAllMocks());

it.each(['ROCK', 'PAPER', 'SCISSORS'] as Move[])('counters repeated %s from completed history without claiming ML', move => {
    const game = new DemoGame();
    for (let round = 1; round <= 5; round++) {
        const response = game.play(move, 'demo');
        expect(response.data.round).toBe(round);
        expect(response.data.analytics.mlRounds).toBe(0);
        if (round > 3) {
            expect(response.data.prediction.strategy).toBe('ADAPTIVE');
            expect(response.data.result).toBe('COMPUTER_WIN');
            expect(response.data.prediction.confidence).toBeNull();
        }
    }
});

it('keeps previous snapshots immutable and tallies wins, draws and losses', () => {
    vi.spyOn(Math, 'random').mockReturnValue(0);
    const game = new DemoGame();
    const first = game.play('PAPER', 'demo');
    game.play('ROCK', 'demo');
    const third = game.play('SCISSORS', 'demo');
    expect(first.data.analytics.totalRounds).toBe(1);
    expect(first.data.analytics.moveCounts.ROCK).toBe(0);
    expect(third.data.analytics).toMatchObject({ playerWins: 1, draws: 1, computerWins: 1, randomRounds: 3 });
});

it('does not use a changed current move when predicting repetition', () => {
    const game = new DemoGame();
    for (let round = 0; round < 3; round++) game.play('ROCK', 'demo');
    const changed = game.play('SCISSORS', 'demo');
    expect(changed.data.prediction.predictedMove).toBe('ROCK');
    expect(changed.data.computerMove).toBe('PAPER');
    expect(changed.data.result).toBe('PLAYER_WIN');
});

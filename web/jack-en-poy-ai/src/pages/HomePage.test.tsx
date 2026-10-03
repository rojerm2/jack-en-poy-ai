import { act, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import HomePage from './HomePage';
import { playGame, startNewGame } from '../services/gameService';
import type { GameResult, PlayResponse } from '../types/game';

vi.mock('../services/gameService', () => ({ playGame: vi.fn(), startNewGame: vi.fn() }));

function response(result: GameResult = 'PLAYER_WIN'): PlayResponse {
    return { success: true, message: 'done', data: { playerMove: 'ROCK', computerMove: 'SCISSORS', result, sessionId: 'a', round: 1, prediction: { strategy: 'RANDOM', predictedMove: null, confidence: null, modelName: null, modelVersion: null, fallbackReason: 'insufficient_history' } } };
}

describe('round animation', () => {
    beforeEach(() => { vi.useFakeTimers(); vi.mocked(playGame).mockResolvedValue(response()); });
    afterEach(() => { vi.useRealTimers(); vi.clearAllMocks(); });

    it('hides the result and score until the chant finishes and rejects duplicate clicks', async () => {
        render(<HomePage />);
        fireEvent.click(screen.getByRole('button', { name: 'Play rock' }));
        fireEvent.click(screen.getByRole('button', { name: 'Play paper' }));
        expect(playGame).toHaveBeenCalledTimes(1);
        expect(screen.getByRole('button', { name: 'Play rock' })).toBeDisabled();
        await act(async () => { await vi.advanceTimersByTimeAsync(1349); });
        expect(screen.queryByText('You win!')).not.toBeInTheDocument();
        expect(screen.getByTestId('player-score')).toHaveTextContent('0');
        await act(async () => { await vi.advanceTimersByTimeAsync(1); });
        expect(screen.getByText('You win!')).toBeInTheDocument();
        expect(screen.getByTestId('player-score')).toHaveTextContent('1');
        expect(screen.getByRole('button', { name: 'Play rock' })).toBeEnabled();
    });

    it('waits for a slow API after the animation finishes', async () => {
        let finish!: (value: PlayResponse) => void;
        vi.mocked(playGame).mockReturnValue(new Promise(resolve => { finish = resolve; }));
        render(<HomePage />);
        fireEvent.click(screen.getByRole('button', { name: 'Play rock' }));
        await act(async () => { await vi.advanceTimersByTimeAsync(2000); });
        expect(screen.queryByText('You win!')).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Play rock' })).toBeDisabled();
        await act(async () => { finish(response()); });
        expect(screen.getByText('You win!')).toBeInTheDocument();
    });

    it.each(['COMPUTER_WIN', 'DRAW'] as GameResult[])('updates %s exactly once', async result => {
        vi.mocked(playGame).mockResolvedValue(response(result));
        render(<HomePage />);
        fireEvent.click(screen.getByRole('button', { name: 'Play rock' }));
        await act(async () => { await vi.advanceTimersByTimeAsync(1350); });
        expect(screen.getByTestId(result === 'DRAW' ? 'draw-score' : 'computer-score')).toHaveTextContent('1');
        expect(screen.getByTestId('player-score')).toHaveTextContent('0');
    });

    it('recovers from API errors without updating the score', async () => {
        vi.mocked(playGame).mockRejectedValue(new Error('offline'));
        render(<HomePage />);
        await act(async () => { fireEvent.click(screen.getByRole('button', { name: 'Play rock' })); });
        expect(screen.getByRole('alert')).toHaveTextContent('Unable to play');
        expect(screen.getByTestId('player-score')).toHaveTextContent('0');
        expect(screen.getByRole('button', { name: 'Play rock' })).toBeEnabled();
    });
});

describe('gameplay controls', () => {
    beforeEach(() => { vi.useFakeTimers(); vi.mocked(playGame).mockResolvedValue(response()); });
    afterEach(() => { vi.useRealTimers(); vi.clearAllMocks(); });

    it('supports keyboard play and resets the session and visible scores', async () => {
        render(<HomePage />);
        fireEvent.keyDown(window, { key: 'r' });
        expect(playGame).toHaveBeenCalledWith('ROCK', expect.any(AbortSignal));
        expect(screen.getByRole('button', { name: 'New game' })).toBeDisabled();
        await act(async () => { await vi.advanceTimersByTimeAsync(1350); });
        expect(screen.getByRole('table')).toBeInTheDocument();
        fireEvent.click(screen.getByRole('button', { name: 'New game' }));
        expect(startNewGame).toHaveBeenCalledOnce();
        expect(screen.getByTestId('player-score')).toHaveTextContent('0');
        expect(screen.queryByRole('table')).not.toBeInTheDocument();
    });

    it('does not play when typing in a field or using a modifier', () => {
        render(<><input aria-label="Notes" /><HomePage /></>);
        fireEvent.keyDown(screen.getByRole('textbox'), { key: 'r' });
        fireEvent.keyDown(window, { key: 'r', ctrlKey: true });
        fireEvent.keyDown(window, { key: 'r', repeat: true });
        expect(playGame).not.toHaveBeenCalled();
    });

    it('shows prediction metadata only after reveal', async () => {
        const ml = response();
        ml.data.prediction = { strategy: 'ML', predictedMove: 'ROCK', confidence: .8, modelName: 'tree', modelVersion: 'v1', fallbackReason: null };
        vi.mocked(playGame).mockResolvedValue(ml);
        render(<HomePage />);
        fireEvent.click(screen.getByRole('button', { name: 'Play rock' }));
        expect(screen.queryByText('Playing your pattern')).not.toBeInTheDocument();
        await act(async () => { await vi.advanceTimersByTimeAsync(1350); });
        expect(screen.getByText(/80% model confidence/)).toBeInTheDocument();
    });
});

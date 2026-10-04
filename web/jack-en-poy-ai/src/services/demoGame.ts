import type { GameRound, Move, PlayResponse, SessionAnalytics } from '../types/game';

const moves: Move[] = ['ROCK', 'PAPER', 'SCISSORS'];
const counter: Record<Move, Move> = { ROCK: 'PAPER', PAPER: 'SCISSORS', SCISSORS: 'ROCK' };

export class DemoGame {
    private history: Move[] = [];
    private analytics: SessionAnalytics = {
        totalRounds: 0, playerWins: 0, computerWins: 0, draws: 0,
        mlRounds: 0, randomRounds: 0, adaptiveRounds: 0, adaptiveWinRate: null,
        predictionsCorrect: 0, predictionAccuracy: null, mlWinRate: null,
        randomWinRate: null, averageConfidence: null, moveCounts: { ROCK: 0, PAPER: 0, SCISSORS: 0 },
    };
    private randomWins = 0;
    private adaptiveWins = 0;

    play(playerMove: Move, sessionId: string): PlayResponse {
        const repeated = this.history.length === 3 && this.history.every(move => move === this.history[0]);
        const predictedMove = repeated ? this.history[0] : null;
        const computerMove = predictedMove ? counter[predictedMove] : moves[Math.floor(Math.random() * moves.length)];
        const result = playerMove === computerMove ? 'DRAW' : counter[computerMove] === playerMove ? 'PLAYER_WIN' : 'COMPUTER_WIN';
        const stats = this.analytics;
        stats.totalRounds++;
        stats.moveCounts[playerMove]++;
        if (result === 'PLAYER_WIN') stats.playerWins++;
        else if (result === 'COMPUTER_WIN') stats.computerWins++;
        else stats.draws++;
        if (repeated) {
            stats.adaptiveRounds++;
            if (result === 'COMPUTER_WIN') this.adaptiveWins++;
            stats.adaptiveWinRate = this.adaptiveWins / stats.adaptiveRounds;
        } else {
            stats.randomRounds++;
            if (result === 'COMPUTER_WIN') this.randomWins++;
            stats.randomWinRate = this.randomWins / stats.randomRounds;
        }
        this.history = [...this.history, playerMove].slice(-3);
        const round: GameRound = {
            playerMove, computerMove, result, sessionId, round: stats.totalRounds,
            prediction: { strategy: repeated ? 'ADAPTIVE' : 'RANDOM', predictedMove,
                confidence: null, modelName: null, modelVersion: null, fallbackReason: repeated ? null : 'browser_demo' },
            analytics: { ...stats, moveCounts: { ...stats.moveCounts } },
        };
        return { success: true, message: 'Browser demo round', data: round };
    }
}

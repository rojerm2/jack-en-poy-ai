export type Move = 'ROCK' | 'PAPER' | 'SCISSORS';
export type GameResult = 'PLAYER_WIN' | 'COMPUTER_WIN' | 'DRAW';

export interface PredictionMetadata {
    strategy: 'ML' | 'RANDOM' | 'ADAPTIVE';
    predictedMove: Move | null;
    confidence: number | null;
    modelName: string | null;
    modelVersion: string | null;
    fallbackReason: string | null;
}

export interface SessionAnalytics {
    totalRounds: number;
    playerWins: number;
    computerWins: number;
    draws: number;
    mlRounds: number;
    randomRounds: number;
    adaptiveRounds: number;
    adaptiveWinRate: number | null;
    predictionsCorrect: number;
    predictionAccuracy: number | null;
    mlWinRate: number | null;
    randomWinRate: number | null;
    averageConfidence: number | null;
    moveCounts: Record<Move, number>;
}

export interface GameRound {
    playerMove: Move;
    computerMove: Move;
    result: GameResult;
    sessionId: string;
    round: number;
    prediction: PredictionMetadata;
    analytics: SessionAnalytics;
}

export interface PlayResponse {
    success: boolean;
    message: string;
    data: GameRound;
}

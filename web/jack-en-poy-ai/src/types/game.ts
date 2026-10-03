export type Move = 'ROCK' | 'PAPER' | 'SCISSORS';
export type GameResult = 'PLAYER_WIN' | 'COMPUTER_WIN' | 'DRAW';

export interface PredictionMetadata {
    strategy: 'ML' | 'RANDOM';
    predictedMove: Move | null;
    confidence: number | null;
    modelName: string | null;
    modelVersion: string | null;
    fallbackReason: string | null;
}

export interface GameRound {
    playerMove: Move;
    computerMove: Move;
    result: GameResult;
    sessionId: string;
    round: number;
    prediction: PredictionMetadata;
}

export interface PlayResponse {
    success: boolean;
    message: string;
    data: GameRound;
}

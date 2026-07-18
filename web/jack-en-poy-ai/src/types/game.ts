export type Move = "ROCK" | "PAPER" | "SCISSORS";

export type GameResult = "PLAYER_WIN" | "COMPUTER_WIN" | "DRAW";

export interface PlayRequest {
  playerMove: Move;
}

export interface PlayResponse {
  success: boolean;

  message: string;

  data: {
    playerMove: Move;

    computerMove: Move;

    result: GameResult;
  };
}

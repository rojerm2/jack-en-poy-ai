package com.orcific.jackenpoyai.util;

import com.orcific.jackenpoyai.enums.GameResult;
import com.orcific.jackenpoyai.enums.Move;

public final class WinnerEvaluator {
    public static GameResult evaluate(Move player, Move computer) {
        if (player == computer) {
            return GameResult.DRAW;
        }

        if ((player == Move.ROCK && computer == Move.SCISSORS)
                || (player == Move.PAPER && computer == Move.ROCK)
                || (player == Move.SCISSORS && computer == Move.PAPER)) {

            return GameResult.PLAYER_WIN;
        }

        return GameResult.COMPUTER_WIN;
    }
}

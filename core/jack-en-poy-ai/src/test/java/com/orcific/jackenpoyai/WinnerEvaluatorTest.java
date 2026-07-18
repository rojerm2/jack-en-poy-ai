package com.orcific.jackenpoyai;

import com.orcific.jackenpoyai.enums.GameResult;
import com.orcific.jackenpoyai.enums.Move;
import com.orcific.jackenpoyai.util.WinnerEvaluator;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;


public class WinnerEvaluatorTest {
    @Test
    void rockShouldBeatScissors() {
        GameResult result = WinnerEvaluator.evaluate(Move.ROCK, Move.SCISSORS);
        assertEquals(GameResult.PLAYER_WIN, result);
    }

    @Test
    void rockShouldLoseToPaper() {
        GameResult result = WinnerEvaluator.evaluate(Move.ROCK, Move.PAPER);
        assertEquals(GameResult.COMPUTER_WIN, result);
    }

    @Test
    void rockShouldDrawToRock() {
        GameResult result = WinnerEvaluator.evaluate(Move.ROCK, Move.ROCK);
        assertEquals(GameResult.DRAW, result);
    }

    @Test
    void paperShouldBeatRock() {
        GameResult result = WinnerEvaluator.evaluate(Move.PAPER, Move.ROCK);
        assertEquals(GameResult.PLAYER_WIN, result);
    }

    @Test
    void paperShouldLoseToScissors() {
        GameResult result = WinnerEvaluator.evaluate(Move.PAPER, Move.SCISSORS);
        assertEquals(GameResult.COMPUTER_WIN, result);
    }

    @Test
    void paperShouldDrawToPaper() {
        GameResult result = WinnerEvaluator.evaluate(Move.PAPER, Move.PAPER);
        assertEquals(GameResult.DRAW, result);
    }

    @Test
    void scissorsShouldBeatPaper() {
        GameResult result = WinnerEvaluator.evaluate(Move.SCISSORS, Move.PAPER);
        assertEquals(GameResult.PLAYER_WIN, result);
    }

    @Test
    void scissorsShouldLoseToRock() {
        GameResult result = WinnerEvaluator.evaluate(Move.SCISSORS, Move.ROCK);
        assertEquals(GameResult.COMPUTER_WIN, result);
    }

    @Test
    void scissorsShouldDrawToScissors() {
        GameResult result = WinnerEvaluator.evaluate(Move.SCISSORS, Move.SCISSORS);
        assertEquals(GameResult.DRAW, result);
    }
}

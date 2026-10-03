package com.orcific.jackenpoyai;

import com.orcific.jackenpoyai.dto.GameRecord;
import com.orcific.jackenpoyai.dto.PredictionMetadata;
import com.orcific.jackenpoyai.enums.GameResult;
import com.orcific.jackenpoyai.enums.Move;
import com.orcific.jackenpoyai.service.SessionStatistics;
import org.junit.jupiter.api.Test;
import java.time.Instant;
import static org.junit.jupiter.api.Assertions.*;

class SessionStatisticsTest {
    @Test
    void empty_rates_are_null() {
        var stats = new SessionStatistics().snapshot();
        assertEquals(0, stats.totalRounds());
        assertNull(stats.predictionAccuracy());
        assertNull(stats.mlWinRate());
        assertNull(stats.averageConfidence());
    }

    @Test
    void counts_prediction_accuracy_separately_from_round_results() {
        var stats = new SessionStatistics();
        stats.record(new GameRecord(1, Instant.now(), "s", Move.ROCK, Move.PAPER, GameResult.COMPUTER_WIN, PredictionMetadata.random("insufficient_history")));
        stats.record(new GameRecord(2, Instant.now(), "s", Move.ROCK, Move.PAPER, GameResult.COMPUTER_WIN, new PredictionMetadata("ML", Move.ROCK, .8, "tree", "v1", null)));
        stats.record(new GameRecord(3, Instant.now(), "s", Move.SCISSORS, Move.PAPER, GameResult.PLAYER_WIN, new PredictionMetadata("ML", Move.ROCK, .6, "tree", "v1", null)));
        var result = stats.snapshot();
        assertEquals(3, result.totalRounds());
        assertEquals(2, result.computerWins());
        assertEquals(1, result.playerWins());
        assertEquals(.5, result.predictionAccuracy());
        assertEquals(.5, result.mlWinRate());
        assertEquals(1., result.randomWinRate());
        assertEquals(.7, result.averageConfidence(), 1e-9);
        assertEquals(2L, result.moveCounts().get("ROCK"));
    }
}

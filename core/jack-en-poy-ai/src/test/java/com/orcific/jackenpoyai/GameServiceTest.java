package com.orcific.jackenpoyai;

import com.orcific.jackenpoyai.dto.GameRecord;
import com.orcific.jackenpoyai.dto.PredictionMetadata;
import com.orcific.jackenpoyai.enums.Move;
import com.orcific.jackenpoyai.service.GameService;
import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class GameServiceTest {
    @Test
    void prediction_sees_only_completed_session_moves() {
        var calls = new ArrayList<List<Move>>();
        var records = new ArrayList<GameRecord>();
        var service = new GameService(records::add, history -> {
            calls.add(history);
            return history.size() < 3 ? PredictionMetadata.random("insufficient_history") :
                    new PredictionMetadata("ML", Move.ROCK, 0.8, "tree", "v1", null);
        });
        service.play(Move.ROCK, "a");
        service.play(Move.PAPER, "a");
        service.play(Move.SCISSORS, "a");
        var fourth = service.play(Move.PAPER, "a");
        assertEquals(List.of(Move.ROCK, Move.PAPER, Move.SCISSORS), calls.get(3));
        assertEquals(Move.PAPER, fourth.computerMove());
        assertEquals(4, fourth.round());
        service.play(Move.SCISSORS, "b");
        assertTrue(calls.get(4).isEmpty());
        assertEquals(5, records.size());
    }

    @Test
    void covers_all_counter_moves() {
        assertEquals(Move.PAPER, GameService.counter(Move.ROCK));
        assertEquals(Move.SCISSORS, GameService.counter(Move.PAPER));
        assertEquals(Move.ROCK, GameService.counter(Move.SCISSORS));
    }

    @Test
    void storage_failure_does_not_advance_history() {
        var calls = new ArrayList<List<Move>>();
        var service = new GameService(record -> { throw new java.io.UncheckedIOException(new java.io.IOException()); }, history -> {
            calls.add(history);
            return PredictionMetadata.random("insufficient_history");
        });
        assertThrows(java.io.UncheckedIOException.class, () -> service.play(Move.ROCK, "a"));
        assertThrows(java.io.UncheckedIOException.class, () -> service.play(Move.ROCK, "a"));
        assertTrue(calls.get(1).isEmpty());
    }
}

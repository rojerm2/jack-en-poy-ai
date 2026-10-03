package com.orcific.jackenpoyai;

import com.orcific.jackenpoyai.dto.GameRecord;
import com.orcific.jackenpoyai.dto.PredictionMetadata;
import com.orcific.jackenpoyai.enums.GameResult;
import com.orcific.jackenpoyai.enums.Move;
import com.orcific.jackenpoyai.service.CsvGameHistoryStore;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import java.nio.file.Path;
import java.nio.file.Files;
import java.time.Instant;
import static org.junit.jupiter.api.Assertions.*;

class CsvGameHistoryStoreTest {
    @TempDir Path temporary;

    @Test
    void writes_one_header_and_session_rounds() throws Exception {
        var path = temporary.resolve("nested/history.csv");
        var store = new CsvGameHistoryStore(path.toString());
        var record = new GameRecord(1, Instant.now(), "session", Move.ROCK, Move.PAPER, GameResult.COMPUTER_WIN, PredictionMetadata.random("insufficient_history"));
        store.save(record);
        store.save(record);
        var lines = Files.readAllLines(path);
        assertEquals(3, lines.size());
        assertTrue(lines.get(0).contains("sessionId"));
        assertTrue(lines.get(1).contains("session"));
        assertTrue(lines.get(1).contains("RANDOM"));
    }

    @Test
    void rejects_legacy_schema_without_modifying_it() throws Exception {
        var path = temporary.resolve("legacy.csv");
        Files.writeString(path, "round,timestamp,playerMove,computerMove,result\n");
        var before = Files.readString(path);
        var store = new CsvGameHistoryStore(path.toString());
        assertThrows(java.io.UncheckedIOException.class, () -> store.save(new GameRecord(1, Instant.now(), "s", Move.ROCK, Move.PAPER, GameResult.COMPUTER_WIN, PredictionMetadata.random("test"))));
        assertEquals(before, Files.readString(path));
    }
}

package com.orcific.jackenpoyai;

import com.orcific.jackenpoyai.controller.HealthController;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import static org.junit.jupiter.api.Assertions.*;

class HealthControllerTest {
    @TempDir Path directory;

    @Test
    void ready_only_when_history_can_be_written_without_exposing_its_path() {
        var health = new HealthController(directory.resolve("history/live.csv").toString());
        assertEquals(200, health.health().getStatusCode().value());
        assertEquals(java.util.Map.of("status", "ready"), health.health().getBody());
    }

    @Test
    void unavailable_when_history_path_is_a_directory() throws Exception {
        Path history = Files.createDirectory(directory.resolve("live.csv"));
        var health = new HealthController(history.toString());
        assertEquals(503, health.health().getStatusCode().value());
    }

    @Test
    void unavailable_when_parent_is_a_file() throws Exception {
        Path file = Files.writeString(directory.resolve("blocked"), "file");
        var health = new HealthController(file.resolve("live.csv").toString());
        assertEquals(503, health.health().getStatusCode().value());
    }
}

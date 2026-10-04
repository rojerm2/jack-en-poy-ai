package com.orcific.jackenpoyai.controller;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {
    private final Path history;

    public HealthController(@Value("${game.history.path}") String historyPath) {
        history = Path.of(historyPath).toAbsolutePath();
    }

    @GetMapping("/api/health")
    public ResponseEntity<Map<String, String>> health() {
        try {
            Files.createDirectories(history.getParent());
            boolean writable = Files.exists(history) ? Files.isRegularFile(history) && Files.isWritable(history) : Files.isWritable(history.getParent());
            return ResponseEntity.status(writable ? 200 : 503).body(Map.of("status", writable ? "ready" : "unavailable"));
        } catch (IOException | SecurityException error) {
            return ResponseEntity.status(503).body(Map.of("status", "unavailable"));
        }
    }
}

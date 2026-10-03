package com.orcific.jackenpoyai.service;

import com.orcific.jackenpoyai.dto.GameRecord;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Service
public class CsvGameHistoryStore implements GameHistoryStore {
    private static final String HEADER = "round,timestamp,sessionId,playerMove,computerMove,result,strategy,predictedMove,confidence,modelName,modelVersion,fallbackReason";
    private final Path path;

    public CsvGameHistoryStore(@Value("${game.history.path}") String filePath) {
        path = Path.of(filePath);
    }

    @Override
    public synchronized void save(GameRecord record) {
        try {
            if (path.getParent() != null) Files.createDirectories(path.getParent());
            if (Files.notExists(path) || Files.size(path) == 0) {
                Files.writeString(path, HEADER + "\n", StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
            }
            try (var reader = Files.newBufferedReader(path)) {
                if (!HEADER.equals(reader.readLine())) throw new IOException("Incompatible history schema; use a separate live history file");
            }
            var p = record.prediction();
            String row = Stream.of(record.round(), record.timestamp(), record.sessionId(), record.playerMove(),
                    record.computerMove(), record.result(), p.strategy(), p.predictedMove(), p.confidence(),
                    p.modelName(), p.modelVersion(), p.fallbackReason()).map(CsvGameHistoryStore::csv).collect(Collectors.joining(","));
            Files.writeString(path, row + "\n", StandardOpenOption.APPEND);
        } catch (IOException error) {
            throw new UncheckedIOException("Unable to record game history", error);
        }
    }

    private static String csv(Object value) {
        if (value == null) return "";
        String text = value.toString();
        return "\"" + text.replace("\"", "\"\"") + "\"";
    }
}

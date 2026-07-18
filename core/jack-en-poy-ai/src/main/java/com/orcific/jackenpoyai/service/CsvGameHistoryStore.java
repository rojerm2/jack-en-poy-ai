package com.orcific.jackenpoyai.service;

import com.orcific.jackenpoyai.dto.GameRecord;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

@Service
public class CsvGameHistoryStore implements  GameHistoryStore {
    @Value("${game.history.path}")
    String filePath;
    @Override
    public void save(GameRecord gameRecord) {
        Path path = initializeAndRetrieveFilePath();

        try (BufferedWriter writer = Files.newBufferedWriter( path, StandardOpenOption.APPEND)) {
            writer.write(String.format("%d,%s,%s,%s,%s%n",
                    gameRecord.round(),
                    gameRecord.timestamp(),
                    gameRecord.playerMove().toString(),
                    gameRecord.computerMove().toString(),
                    gameRecord.result().toString())
            );
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }

    private Path initializeAndRetrieveFilePath(){
        try {
            Path path = Paths.get(filePath);

            if (path.getParent() != null) {
                Files.createDirectories(path.getParent());
            }

            if (Files.notExists(path)) {
                Files.createFile(path);

                Files.writeString(path, "round,timestamp,playerMove,computerMove,result\n");
            }

            return path;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}

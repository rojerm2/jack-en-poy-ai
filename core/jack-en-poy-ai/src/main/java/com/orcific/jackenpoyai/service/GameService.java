package com.orcific.jackenpoyai.service;

import com.orcific.jackenpoyai.dto.GameRecord;
import com.orcific.jackenpoyai.dto.PlayResponse;
import com.orcific.jackenpoyai.enums.GameResult;
import com.orcific.jackenpoyai.enums.Move;
import com.orcific.jackenpoyai.util.MoveGenerator;
import com.orcific.jackenpoyai.util.WinnerEvaluator;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class GameService {
    private final GameHistoryStore historyStore;

    public PlayResponse play(Move playerMove){
        Move computerMove = MoveGenerator.randomMove();

        GameResult result = WinnerEvaluator.evaluate(playerMove, computerMove);

        GameRecord record = new GameRecord(0, LocalDateTime.now(), playerMove, computerMove, result);
        historyStore.save(record);

        return new  PlayResponse(playerMove, computerMove, result);
    }
}

package com.orcific.jackenpoyai.service;

import com.orcific.jackenpoyai.dto.PlayResponse;
import com.orcific.jackenpoyai.enums.GameResult;
import com.orcific.jackenpoyai.enums.Move;
import com.orcific.jackenpoyai.util.MoveGenerator;
import com.orcific.jackenpoyai.util.WinnerEvaluator;
import org.springframework.stereotype.Service;

@Service
public class GameService {
    public PlayResponse play(Move playerMove){
        Move computerMove = MoveGenerator.randomMove();

        GameResult result = WinnerEvaluator.evaluate(playerMove, computerMove);

        return new  PlayResponse(playerMove, computerMove, result);
    }
}

package com.orcific.jackenpoyai.dto;

import com.orcific.jackenpoyai.enums.GameResult;
import com.orcific.jackenpoyai.enums.Move;

public record PlayResponse(Move playerMove, Move computerMove, GameResult result,
                           String sessionId, long round, PredictionMetadata prediction) {}

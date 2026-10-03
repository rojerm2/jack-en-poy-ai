package com.orcific.jackenpoyai.dto;

import com.orcific.jackenpoyai.enums.GameResult;
import com.orcific.jackenpoyai.enums.Move;
import java.time.Instant;

public record GameRecord(long round, Instant timestamp, String sessionId, Move playerMove,
                         Move computerMove, GameResult result, PredictionMetadata prediction) {}

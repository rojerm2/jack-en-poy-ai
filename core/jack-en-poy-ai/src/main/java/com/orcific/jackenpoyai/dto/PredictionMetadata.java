package com.orcific.jackenpoyai.dto;

import com.orcific.jackenpoyai.enums.Move;

public record PredictionMetadata(String strategy, Move predictedMove, Double confidence,
                                 String modelName, String modelVersion, String fallbackReason) {
    public static PredictionMetadata repetition(Move move) {
        return new PredictionMetadata("ADAPTIVE", move, null, null, null, null);
    }

    public static PredictionMetadata random(String reason) {
        return new PredictionMetadata("RANDOM", null, null, null, null, reason);
    }
}

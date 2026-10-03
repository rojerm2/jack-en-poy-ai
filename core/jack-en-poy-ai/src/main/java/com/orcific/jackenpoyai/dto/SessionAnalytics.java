package com.orcific.jackenpoyai.dto;

import java.util.Map;

public record SessionAnalytics(long totalRounds, long playerWins, long computerWins, long draws,
                               long mlRounds, long randomRounds, long predictionsCorrect,
                               Double predictionAccuracy, Double mlWinRate, Double randomWinRate,
                               Double averageConfidence, Map<String, Long> moveCounts,
                               long adaptiveRounds, Double adaptiveWinRate) {}

package com.orcific.jackenpoyai.service;

import com.orcific.jackenpoyai.dto.GameRecord;
import com.orcific.jackenpoyai.dto.SessionAnalytics;
import com.orcific.jackenpoyai.enums.GameResult;
import java.util.LinkedHashMap;
import java.util.Map;

public class SessionStatistics {
    private long total, playerWins, computerWins, draws, ml, random, correct, mlWins, randomWins, adaptive, adaptiveWins;
    private double confidenceSum;
    private final Map<String, Long> moves = new LinkedHashMap<>(Map.of("ROCK", 0L, "PAPER", 0L, "SCISSORS", 0L));

    public void record(GameRecord round) {
        total++;
        switch (round.result()) {
            case PLAYER_WIN -> playerWins++;
            case COMPUTER_WIN -> computerWins++;
            case DRAW -> draws++;
        }
        moves.merge(round.playerMove().name(), 1L, Long::sum);
        if ("ML".equals(round.prediction().strategy())) {
            ml++;
            if (round.prediction().predictedMove() == round.playerMove()) correct++;
            if (round.result() == GameResult.COMPUTER_WIN) mlWins++;
            confidenceSum += round.prediction().confidence();
        } else if ("ADAPTIVE".equals(round.prediction().strategy())) {
            adaptive++;
            if (round.result() == GameResult.COMPUTER_WIN) adaptiveWins++;
        } else {
            random++;
            if (round.result() == GameResult.COMPUTER_WIN) randomWins++;
        }
    }

    public SessionAnalytics snapshot() {
        return new SessionAnalytics(total, playerWins, computerWins, draws, ml, random, correct,
                ratio(correct, ml), ratio(mlWins, ml), ratio(randomWins, random),
                ml == 0 ? null : confidenceSum / ml, Map.copyOf(moves), adaptive, ratio(adaptiveWins, adaptive));
    }

    private static Double ratio(long numerator, long denominator) {
        return denominator == 0 ? null : (double) numerator / denominator;
    }
}

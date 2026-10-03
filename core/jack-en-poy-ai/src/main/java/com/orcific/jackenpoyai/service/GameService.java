package com.orcific.jackenpoyai.service;

import com.orcific.jackenpoyai.dto.GameRecord;
import com.orcific.jackenpoyai.dto.PlayResponse;
import com.orcific.jackenpoyai.dto.SessionAnalytics;
import com.orcific.jackenpoyai.enums.Move;
import com.orcific.jackenpoyai.util.MoveGenerator;
import com.orcific.jackenpoyai.util.WinnerEvaluator;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
public class GameService {
    private final GameHistoryStore historyStore;
    private final MovePredictor predictor;
    private final Map<String, Session> sessions = new LinkedHashMap<>(16, 0.75f, true);

    private static class Session {
        final List<Move> history = new ArrayList<>();
        long round;
        final SessionStatistics statistics = new SessionStatistics();
    }

    public GameService(GameHistoryStore historyStore, MovePredictor predictor) {
        this.historyStore = historyStore;
        this.predictor = predictor;
    }

    public synchronized PlayResponse play(Move playerMove, String requestedSession) {
        var id = requestedSession == null ? UUID.randomUUID().toString() : requestedSession;
        var session = sessions.computeIfAbsent(id, ignored -> new Session());
        if (sessions.size() > 1000) sessions.remove(sessions.keySet().iterator().next());

        // Choose the strategy before adding this round's move to completed history.
        var prediction = predictor.predict(List.copyOf(session.history));
        var computerMove = prediction.predictedMove() == null ? MoveGenerator.randomMove() : counter(prediction.predictedMove());
        var result = WinnerEvaluator.evaluate(playerMove, computerMove);
        var round = session.round + 1;
        var record = new GameRecord(round, Instant.now(), id, playerMove, computerMove, result, prediction);
        historyStore.save(record);
        session.statistics.record(record);
        session.round = round;
        session.history.add(playerMove);
        if (session.history.size() > 3) session.history.removeFirst();
        return new PlayResponse(playerMove, computerMove, result, id, round, prediction, session.statistics.snapshot());
    }

    public synchronized SessionAnalytics analytics(String sessionId) {
        var session = sessions.get(sessionId);
        return session == null ? new SessionStatistics().snapshot() : session.statistics.snapshot();
    }

    public static Move counter(Move move) {
        return switch (move) {
            case ROCK -> Move.PAPER;
            case PAPER -> Move.SCISSORS;
            case SCISSORS -> Move.ROCK;
        };
    }
}

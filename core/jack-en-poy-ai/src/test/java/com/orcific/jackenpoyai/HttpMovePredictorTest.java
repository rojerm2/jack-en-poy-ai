package com.orcific.jackenpoyai;

import com.orcific.jackenpoyai.enums.Move;
import com.orcific.jackenpoyai.service.HttpMovePredictor;
import com.sun.net.httpserver.HttpServer;
import org.junit.jupiter.api.Test;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import static org.junit.jupiter.api.Assertions.*;

class HttpMovePredictorTest {
    private static final List<Move> HISTORY = List.of(Move.ROCK, Move.PAPER, Move.SCISSORS);

    @Test
    void sends_only_history_and_parses_prediction() throws Exception {
        var body = new AtomicReference<String>();
        var server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/predict", exchange -> {
            body.set(new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8));
            byte[] json = "{\"predictedMove\":\"ROCK\",\"confidence\":0.8,\"modelName\":\"tree\",\"modelVersion\":\"v1\",\"historyLength\":3}".getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, json.length);
            exchange.getResponseBody().write(json);
            exchange.close();
        });
        server.start();
        try {
            var predictor = new HttpMovePredictor("http://127.0.0.1:" + server.getAddress().getPort(), true, 600);
            assertEquals("ML", predictor.predict(HISTORY).strategy());
            assertTrue(body.get().contains("history"));
            assertFalse(body.get().contains("playerMove"));
            assertEquals("insufficient_history", predictor.predict(List.of()).fallbackReason());
        } finally { server.stop(0); }
    }

    @Test
    void falls_back_when_disabled_or_unreachable() {
        assertEquals("ml_disabled", new HttpMovePredictor("http://127.0.0.1:1", false, 100).predict(HISTORY).fallbackReason());
        assertEquals("service_unavailable", new HttpMovePredictor("http://127.0.0.1:1", true, 100).predict(HISTORY).fallbackReason());
    }

    @Test
    void rejects_invalid_response_and_server_errors() throws Exception {
        var server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/predict", exchange -> {
            byte[] json = "{\"predictedMove\":\"ROCK\",\"confidence\":2,\"modelName\":\"tree\",\"modelVersion\":\"v1\",\"historyLength\":3}".getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, json.length);
            exchange.getResponseBody().write(json);
            exchange.close();
        });
        server.start();
        try {
            assertEquals("invalid_prediction", new HttpMovePredictor("http://127.0.0.1:" + server.getAddress().getPort(), true, 600).predict(HISTORY).fallbackReason());
        } finally { server.stop(0); }
    }

    @Test
    void timeout_and_http_failure_use_random_fallback() throws Exception {
        var slow = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        slow.createContext("/predict", exchange -> {
            try { Thread.sleep(400); } catch (InterruptedException ignored) { Thread.currentThread().interrupt(); }
            try { exchange.sendResponseHeaders(503, -1); } finally { exchange.close(); }
        });
        slow.start();
        try {
            var predictor = new HttpMovePredictor("http://127.0.0.1:" + slow.getAddress().getPort(), true, 100);
            long start = System.nanoTime();
            assertEquals("service_unavailable", predictor.predict(HISTORY).fallbackReason());
            assertTrue((System.nanoTime() - start) / 1_000_000 < 1500);
        } finally { slow.stop(0); }
        var unavailable = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        unavailable.createContext("/predict", exchange -> { exchange.sendResponseHeaders(503, -1); exchange.close(); });
        unavailable.start();
        try {
            assertEquals("service_unavailable", new HttpMovePredictor("http://127.0.0.1:" + unavailable.getAddress().getPort(), true, 600).predict(HISTORY).fallbackReason());
        } finally { unavailable.stop(0); }
    }
}

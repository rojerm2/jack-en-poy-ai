package com.orcific.jackenpoyai;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.beans.factory.annotation.Value;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class CorsTest {
    @Value("${local.server.port}") int port;

    @Test
    void accepts_both_local_preview_origins_and_rejects_others() throws Exception {
        try (var client = HttpClient.newHttpClient()) {
            for (var origin : new String[]{"http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:4173", "http://127.0.0.1:4173", "https://unknown.example"}) {
                var request = HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + port + "/api/game/play"))
                        .header("Origin", origin).header("Access-Control-Request-Method", "POST")
                        .method("OPTIONS", HttpRequest.BodyPublishers.noBody()).build();
                var response = client.send(request, HttpResponse.BodyHandlers.ofString());
                if ((origin.endsWith(":5173") || origin.endsWith(":4173"))) {
                    assertEquals(200, response.statusCode());
                    assertEquals(origin, response.headers().firstValue("Access-Control-Allow-Origin").orElseThrow());
                } else assertEquals(403, response.statusCode());
            }
        }
    }
}

package com.orcific.jackenpoyai.service;

import com.orcific.jackenpoyai.dto.PredictionMetadata;
import com.orcific.jackenpoyai.enums.Move;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.JdkClientHttpRequestFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

import java.net.http.HttpClient;
import java.time.Duration;
import java.util.List;
import java.util.Map;

@Service
public class HttpMovePredictor implements MovePredictor {
    private final RestClient client;
    private final boolean enabled;

    public HttpMovePredictor(@Value("${ml.service.url}") String url,
                             @Value("${ml.service.enabled:true}") boolean enabled,
                             @Value("${ml.service.timeout-ms:600}") int timeout) {
        this.enabled = enabled;
        var http = HttpClient.newBuilder().connectTimeout(Duration.ofMillis(timeout)).build();
        var factory = new JdkClientHttpRequestFactory(http);
        factory.setReadTimeout(Duration.ofMillis(timeout));
        this.client = RestClient.builder().baseUrl(url).requestFactory(factory).build();
    }

    public record Prediction(Move predictedMove, Double confidence, String modelName,
                             String modelVersion, int historyLength) {}

    @Override
    public PredictionMetadata predict(List<Move> history) {
        if (history.size() < 3) return PredictionMetadata.random("insufficient_history");
        if (!enabled) return PredictionMetadata.random("ml_disabled");
        try {
            var previous = List.copyOf(history.subList(history.size() - 3, history.size()));
            var response = client.post().uri("/predict").body(Map.of("history", previous))
                    .retrieve().body(Prediction.class);
            if (response == null || response.predictedMove() == null || response.confidence() == null
                    || !Double.isFinite(response.confidence()) || response.confidence() < 0 || response.confidence() > 1
                    || response.historyLength() != 3 || !validText(response.modelName()) || !validText(response.modelVersion())) {
                return PredictionMetadata.random("invalid_prediction");
            }
            return new PredictionMetadata("ML", response.predictedMove(), response.confidence(),
                    response.modelName(), response.modelVersion(), null);
        } catch (RestClientException | IllegalArgumentException error) {
            return PredictionMetadata.random("service_unavailable");
        }
    }

    private static boolean validText(String value) {
        return value != null && !value.isBlank() && value.length() <= 128;
    }
}

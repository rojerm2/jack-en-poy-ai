package com.orcific.jackenpoyai;

import com.orcific.jackenpoyai.controller.GameController;
import com.orcific.jackenpoyai.dto.PredictionMetadata;
import com.orcific.jackenpoyai.exception.GlobalExceptionHandler;
import com.orcific.jackenpoyai.service.GameService;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.http.MediaType;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

class GameApiTest {
    @Test
    void validates_moves_and_sessions() throws Exception {
        var service = new GameService(record -> {}, history -> PredictionMetadata.random("test"));
        var mvc = MockMvcBuilders.standaloneSetup(new GameController(service)).setControllerAdvice(new GlobalExceptionHandler()).build();
        mvc.perform(post("/api/game/play").contentType(MediaType.APPLICATION_JSON).content("{}"))
                .andExpect(status().isBadRequest()).andExpect(jsonPath("$.success").value(false));
        mvc.perform(post("/api/game/play").contentType(MediaType.APPLICATION_JSON).content("{\"playerMove\":\"BAD\"}"))
                .andExpect(status().isBadRequest());
        mvc.perform(post("/api/game/play").contentType(MediaType.APPLICATION_JSON).content("{\"playerMove\":\"ROCK\",\"sessionId\":\"bad\"}"))
                .andExpect(status().isBadRequest());
        mvc.perform(post("/api/game/play").contentType(MediaType.APPLICATION_JSON).content("{\"playerMove\":\"ROCK\"}"))
                .andExpect(status().isOk()).andExpect(jsonPath("$.data.round").value(1))
                .andExpect(jsonPath("$.data.prediction.strategy").value("RANDOM"));
    }
}

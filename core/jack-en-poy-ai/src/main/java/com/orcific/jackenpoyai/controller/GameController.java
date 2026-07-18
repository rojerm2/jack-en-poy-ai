package com.orcific.jackenpoyai.controller;

import com.orcific.jackenpoyai.dto.ApiResponse;
import com.orcific.jackenpoyai.dto.PlayRequest;
import com.orcific.jackenpoyai.dto.PlayResponse;
import com.orcific.jackenpoyai.enums.Move;
import com.orcific.jackenpoyai.service.GameService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("api/game")
@RequiredArgsConstructor
public class GameController {
    private final GameService gameService;

    @PostMapping("/play")
    public ApiResponse<PlayResponse> play(@Valid @RequestBody PlayRequest playRequest){
        return ApiResponse.success(
                gameService.play(playRequest.playerMove())
        );
    }
}

package com.orcific.jackenpoyai.dto;

import com.orcific.jackenpoyai.enums.GameResult;
import com.orcific.jackenpoyai.enums.Move;

import java.time.LocalDateTime;

public record GameRecord(
        long round,
        LocalDateTime timestamp,
        Move playerMove,
        Move computerMove,
        GameResult result
) {
}

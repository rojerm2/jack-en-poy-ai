package com.orcific.jackenpoyai.dto;

import com.orcific.jackenpoyai.enums.Move;

public record PlayRequest(
        Move playerMove
) {
}

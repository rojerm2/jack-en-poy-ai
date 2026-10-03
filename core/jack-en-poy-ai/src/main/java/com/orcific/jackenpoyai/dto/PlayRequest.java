package com.orcific.jackenpoyai.dto;

import com.orcific.jackenpoyai.enums.Move;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

public record PlayRequest(
        @NotNull(message = "playerMove is required") Move playerMove,
        @Pattern(regexp = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", message = "sessionId must be a UUID") String sessionId
) {}

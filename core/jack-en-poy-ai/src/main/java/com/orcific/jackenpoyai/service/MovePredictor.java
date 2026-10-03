package com.orcific.jackenpoyai.service;

import com.orcific.jackenpoyai.dto.PredictionMetadata;
import com.orcific.jackenpoyai.enums.Move;
import java.util.List;

public interface MovePredictor {
    PredictionMetadata predict(List<Move> completedHistory);
}

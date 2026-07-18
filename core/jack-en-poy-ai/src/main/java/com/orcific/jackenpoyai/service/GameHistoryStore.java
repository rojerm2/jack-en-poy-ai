package com.orcific.jackenpoyai.service;

import com.orcific.jackenpoyai.dto.GameRecord;

public interface GameHistoryStore {
    void save(GameRecord gameRecord);
}

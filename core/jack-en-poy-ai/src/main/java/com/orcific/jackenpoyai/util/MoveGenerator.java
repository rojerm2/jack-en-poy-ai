package com.orcific.jackenpoyai.util;

import com.orcific.jackenpoyai.enums.Move;

import java.util.concurrent.ThreadLocalRandom;

public final class MoveGenerator {
    public static Move randomMove() {
        Move[] moves = Move.values();

        return moves[
                ThreadLocalRandom.current()
                        .nextInt(moves.length)
                ];
    }
}

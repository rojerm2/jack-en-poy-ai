import api from '../api/api';
import type { Move, PlayResponse } from '../types/game';

export async function playGame(move: Move): Promise<PlayResponse> {
    const response = await api.post('/game/play', {
        playerMove: move,
    });

    return response.data;
}

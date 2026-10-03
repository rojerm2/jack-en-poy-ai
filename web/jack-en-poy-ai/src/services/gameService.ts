import api from '../api/api';
import type { Move, PlayResponse } from '../types/game';

let sessionId = crypto.randomUUID();

export async function playGame(move: Move): Promise<PlayResponse> {
    const response = await api.post('/game/play', { playerMove: move, sessionId });
    sessionId = response.data.data.sessionId;
    return response.data;
}

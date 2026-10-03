import api from '../api/api';
import type { Move, PlayResponse } from '../types/game';

let sessionId: string = crypto.randomUUID();

export async function playGame(move: Move, signal?: AbortSignal): Promise<PlayResponse> {
    const response = await api.post<PlayResponse>('/game/play', { playerMove: move, sessionId }, { signal });
    if (!response.data.success) throw new Error(response.data.message);
    sessionId = response.data.data.sessionId;
    return response.data;
}

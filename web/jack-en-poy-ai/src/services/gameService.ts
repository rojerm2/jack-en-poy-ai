import api from '../api/api';
import { DemoGame } from './demoGame';
import type { Move, PlayResponse } from '../types/game';

let sessionId: string = crypto.randomUUID();
let demo = new DemoGame();

export async function playGame(move: Move, signal?: AbortSignal): Promise<PlayResponse> {
    if (signal?.aborted) throw new DOMException('Round cancelled', 'AbortError');
    if (import.meta.env.VITE_DEMO_MODE === 'true') return demo.play(move, sessionId);
    const response = await api.post<PlayResponse>('/game/play', { playerMove: move, sessionId }, { signal });
    if (!response.data.success) throw new Error(response.data.message);
    sessionId = response.data.data.sessionId;
    return response.data;
}

export function startNewGame(): void {
    sessionId = crypto.randomUUID();
    demo = new DemoGame();
}

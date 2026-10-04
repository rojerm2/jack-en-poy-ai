import { afterEach, expect, it, vi } from 'vitest';
import api from '../api/api';
import { DemoGame } from './demoGame';
import { playGame, startNewGame } from './gameService';

vi.mock('../api/api', () => ({ default: { post: vi.fn() } }));
afterEach(() => { vi.unstubAllEnvs(); vi.clearAllMocks(); startNewGame(); });

it('plays and resets a demo without making any HTTP request', async () => {
    vi.stubEnv('VITE_DEMO_MODE', 'true');
    startNewGame();
    for (let round = 0; round < 4; round++) await playGame('ROCK');
    expect(api.post).not.toHaveBeenCalled();
    startNewGame();
    const first = await playGame('PAPER');
    expect(first.data.round).toBe(1);
    expect(first.data.analytics.adaptiveRounds).toBe(0);
});

it('uses the real API in normal builds', async () => {
    vi.stubEnv('VITE_DEMO_MODE', 'false');
    const response = new DemoGame().play('ROCK', crypto.randomUUID());
    vi.mocked(api.post).mockResolvedValue({ data: response });
    const signal = new AbortController().signal;
    expect(await playGame('ROCK', signal)).toEqual(response);
    expect(api.post).toHaveBeenCalledWith('/game/play', { playerMove: 'ROCK', sessionId: expect.any(String) }, { signal });
});

it('does not record cancelled demo rounds', async () => {
    vi.stubEnv('VITE_DEMO_MODE', 'true');
    startNewGame();
    const controller = new AbortController();
    controller.abort();
    await expect(playGame('ROCK', controller.signal)).rejects.toMatchObject({ name: 'AbortError' });
    expect((await playGame('ROCK')).data.round).toBe(1);
});

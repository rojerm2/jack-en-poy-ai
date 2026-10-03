export const ROUND_DURATION = 1350;

export function waitForReveal(signal: AbortSignal): Promise<void> {
    return new Promise((resolve, reject) => {
        if (signal.aborted) return reject(new DOMException('Cancelled', 'AbortError'));
        const cancel = () => {
            clearTimeout(timer);
            reject(new DOMException('Cancelled', 'AbortError'));
        };
        const timer = setTimeout(() => {
            signal.removeEventListener('abort', cancel);
            resolve();
        }, ROUND_DURATION);
        signal.addEventListener('abort', cancel, { once: true });
    });
}

import type { Move } from '../types/game';

interface Props { move: Move; onClick: (move: Move) => void; disabled: boolean; }
const symbols = { ROCK: '✊', PAPER: '✋', SCISSORS: '✌' };

export default function MoveButton({ move, onClick, disabled }: Props) {
    return <button className="move-button" disabled={disabled} onClick={() => onClick(move)} aria-label={`Play ${move.toLowerCase()}`}>
        <span className="move-symbol" aria-hidden="true">{symbols[move]}</span><span>{move.charAt(0) + move.slice(1).toLowerCase()}</span>
    </button>;
}

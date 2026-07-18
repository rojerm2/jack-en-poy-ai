import type { Move } from '../types/game';

interface Props {
    move: Move;
    onClick: (move: Move) => void;
    disabled: boolean;
}

export default function MoveButton({ move, onClick, disabled }: Props) {
    return (
        <button
            className="rounded-lg bg-blue-600 px-8 py-3 font-semibold text-white transition hover:bg-blue-700"
            disabled={disabled}
            onClick={() => onClick(move)}
        >
            {move}
        </button>
    );
}

import type { Move } from '../types/game';

interface Props { move: Move; side: 'player' | 'computer'; }

export default function Hand({ move, side }: Props) {
    return (
        <svg viewBox="0 0 180 240" className={`hand hand-${side}`} aria-hidden="true">
            <path d="M63 127 L119 127 L128 240 L48 240 Z" fill="#e8af82" />
            {move === 'PAPER' && <g fill="#f2bf94" stroke="#c78d64" strokeWidth="2.5">
                <rect x="48" y="44" width="20" height="84" rx="10" transform="rotate(-12 58 128)" />
                <rect x="70" y="20" width="20" height="99" rx="10" />
                <rect x="92" y="27" width="20" height="94" rx="10" />
                <rect x="114" y="48" width="18" height="78" rx="9" transform="rotate(9 123 126)" />
            </g>}
            {move === 'SCISSORS' && <g fill="#f2bf94" stroke="#c78d64" strokeWidth="2.5">
                <rect x="65" y="22" width="23" height="109" rx="11" transform="rotate(-13 77 126)" />
                <rect x="92" y="22" width="23" height="109" rx="11" transform="rotate(13 103 126)" />
            </g>}
            <path d="M51 84 Q49 71 62 68 L115 68 Q129 68 132 85 L131 117 Q130 145 105 156 L69 154 Q49 139 48 118 Z" fill="#f2bf94" stroke="#c78d64" strokeWidth="2.5" />
            {move === 'ROCK' && <g fill="#f2bf94" stroke="#c78d64" strokeWidth="2.5">
                <rect x="47" y="64" width="23" height="43" rx="10" />
                <rect x="68" y="60" width="23" height="45" rx="10" />
                <rect x="89" y="62" width="23" height="43" rx="10" />
                <rect x="110" y="69" width="22" height="39" rx="10" />
            </g>}
            {move === 'SCISSORS' && <g fill="#f2bf94" stroke="#c78d64" strokeWidth="2.5">
                <rect x="105" y="78" width="25" height="40" rx="11" />
                <rect x="85" y="91" width="25" height="35" rx="11" />
            </g>}
            <path d="M53 107 Q32 91 38 80 Q44 69 53 79 L76 101 Q83 109 73 117 Q64 123 53 107 Z" fill="#f2bf94" stroke="#c78d64" strokeWidth="2.5" />
            <path d="M62 144 Q91 151 120 144 L128 240 L48 240 Z" fill={side === 'player' ? '#4267d5' : '#dd7258'} />
            <path d="M61 151 Q90 159 122 151" fill="none" stroke={side === 'player' ? '#294ab0' : '#bf5740'} strokeWidth="6" />
        </svg>
    );
}

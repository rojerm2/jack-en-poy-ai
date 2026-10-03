import type { GameRound } from '../types/game';
import Hand from './Hand';

interface Props { active: boolean; game: GameRound | null; }
const resultText = { PLAYER_WIN: 'You win!', COMPUTER_WIN: 'Computer wins', DRAW: 'A draw. Go again!' };

export default function RoundArena({ active, game }: Props) {
    return (
        <section className={`arena ${active ? 'arena-active' : ''}`} aria-label="First-person game table" aria-busy={active}>
            <span className="table-label opponent-label">COMPUTER</span>
            <div className="opponent-arm"><Hand move={active ? 'ROCK' : game?.computerMove ?? 'ROCK'} side="computer" /></div>
            <div className="arena-message" role="status" aria-live="polite">
                {active ? <><span className="sr-only">Round in progress. Jack, En, Poy!</span><div className="chant" aria-hidden="true"><span>Jack</span><span>En</span><span>Poy!</span></div></> :
                    <><span className="eyebrow">{game ? `ROUND ${game.round}` : 'READY WHEN YOU ARE'}</span><h2>{game ? resultText[game.result] : 'Make your move.'}</h2><p>{game ? `${game.playerMove.toLowerCase()} vs ${game.computerMove.toLowerCase()}` : 'Three moves. One mind game.'}</p></>}
            </div>
            <div className="player-arm"><Hand move={active ? 'ROCK' : game?.playerMove ?? 'ROCK'} side="player" /></div>
            <span className="table-label player-label">YOU</span>
        </section>
    );
}

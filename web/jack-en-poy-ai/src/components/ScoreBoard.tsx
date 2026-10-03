interface Props { player: number; computer: number; draw: number; }

export default function ScoreBoard({ player, computer, draw }: Props) {
    return <section className="scoreboard" aria-label="Score board">
        <div className="score-player"><span>YOU</span><strong data-testid="player-score">{player}</strong></div>
        <div className="score-draw"><span>DRAWS</span><strong data-testid="draw-score">{draw}</strong></div>
        <div className="score-computer"><span>COMPUTER</span><strong data-testid="computer-score">{computer}</strong></div>
    </section>;
}

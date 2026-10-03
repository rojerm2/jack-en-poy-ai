import type { GameRound } from '../types/game';

export default function RoundHistory({ rounds }: { rounds: GameRound[] }) {
    if (!rounds.length) return null;
    const labels = { PLAYER_WIN: 'You won', COMPUTER_WIN: 'Computer won', DRAW: 'Draw' };
    return <section className="round-history" aria-label="Recent rounds"><h2>Recent rounds</h2>
        <div className="history-scroll"><table><thead><tr><th>Round</th><th>You</th><th>Computer</th><th>Result</th></tr></thead>
            <tbody>{rounds.map(round => <tr key={round.round}><td>{round.round}</td><td>{round.playerMove.toLowerCase()}</td><td>{round.computerMove.toLowerCase()}</td><td className={`outcome-${round.result.toLowerCase()}`}>{labels[round.result]}</td></tr>)}</tbody>
        </table></div>
    </section>;
}

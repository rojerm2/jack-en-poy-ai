interface Props {
    player: number;
    computer: number;
    draw: number;
}

export default function ScoreBoard({ player, computer, draw }: Props) {
    return (
        <div className="rounded-xl bg-white p-6 shadow">
            <h2 className="mb-4 text-xl font-semibold">Score Board</h2>

            <div className="space-y-2">
                <p>Player : {player}</p>

                <p>Computer : {computer}</p>

                <p>Draws : {draw}</p>
            </div>
        </div>
    );
}

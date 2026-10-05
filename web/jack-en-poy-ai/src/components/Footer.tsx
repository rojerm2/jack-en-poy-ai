export default function Footer() {
    return <footer className="game-footer">{import.meta.env.VITE_DEMO_MODE === 'true' ? 'Browser demo built with React.' : 'Built with React, Spring Boot & scikit-learn.'}<br />The computer studies your previous moves. Stay unpredictable.</footer>;
}

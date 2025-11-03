export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-background to-muted">
      <div className="max-w-5xl w-full items-center justify-between font-mono text-sm">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold mb-4 text-primary">
            🐭 Mausritter Tools
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            Generátory, campaign management a character sheets pro Mausritter TTRPG
          </p>
          <div className="flex gap-4 justify-center">
            <button className="bg-primary text-primary-foreground px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition">
              Start Free →
            </button>
            <button className="bg-secondary text-secondary-foreground px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition">
              Learn More
            </button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-card p-6 rounded-lg border-2 border-border shadow-sm">
            <div className="text-4xl mb-4">🎲</div>
            <h3 className="text-xl font-semibold mb-2">Generátory</h3>
            <p className="text-muted-foreground">
              17 nástrojů pro generování postav, NPC, hexů, dungeonů a dalších
            </p>
          </div>

          <div className="bg-card p-6 rounded-lg border-2 border-border shadow-sm">
            <div className="text-4xl mb-4">🗺️</div>
            <h3 className="text-xl font-semibold mb-2">Hexcrawl Manager</h3>
            <p className="text-muted-foreground">
              Spravuj kampaně, mapy, zvěsti a objevování světa
            </p>
          </div>

          <div className="bg-card p-6 rounded-lg border-2 border-border shadow-sm">
            <div className="text-4xl mb-4">⚔️</div>
            <h3 className="text-xl font-semibold mb-2">Character Sheets</h3>
            <p className="text-muted-foreground">
              Sleduj své postavy, inventář, HP a progression
            </p>
          </div>
        </div>

        {/* Features List */}
        <div className="bg-card p-8 rounded-lg border-2 border-border shadow-sm mb-16">
          <h2 className="text-2xl font-bold mb-4">✨ Features</h2>
          <ul className="space-y-2 text-muted-foreground">
            <li className="flex items-center gap-2">
              <span className="text-green-500">✅</span>
              17 generátorů (character, NPC, hex, dungeon, settlement, atd.)
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">✅</span>
              Campaign management pro GM
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">✅</span>
              Character sheets pro hráče
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">✅</span>
              Real-time dice roller
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">✅</span>
              100% zdarma
            </li>
          </ul>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-muted-foreground">
          <p>🐭 Mausritter Tools © 2025</p>
          <p className="mt-2">
            Mausritter je © Games Omnivorous (neoficiální fan tool)
          </p>
          <div className="flex gap-4 justify-center mt-4">
            <a href="#" className="hover:text-primary transition">GitHub</a>
            <a href="#" className="hover:text-primary transition">Discord</a>
            <a href="#" className="hover:text-primary transition">Docs</a>
          </div>
        </footer>
      </div>
    </main>
  )
}

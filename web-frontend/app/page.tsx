import Link from "next/link";

export default function Home() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-background to-muted">
      <div className="max-w-5xl w-full items-center justify-between font-mono text-sm">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold mb-4 text-primary">
            🐭 Mausritter Tools
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            16 generátorů pro Mausritter TTRPG - postavy, NPC, hexy, dungeony a další
          </p>
          <div className="flex justify-center">
            <Link href="/generators" className="bg-primary text-primary-foreground px-10 py-4 rounded-lg text-lg font-semibold hover:opacity-90 transition shadow-lg">
              Zobrazit Generátory →
            </Link>
          </div>
        </div>

        {/* Coming Soon */}
        <div className="bg-card/50 border-2 border-dashed border-primary/30 rounded-lg p-8 mb-16 max-w-2xl mx-auto text-center">
          <p className="text-lg text-muted-foreground">
            <span className="text-2xl mr-2">💡</span>
            <strong className="text-foreground">Připravujeme:</strong> Campaign Tracker
          </p>
          <p className="text-sm text-muted-foreground mt-2">
            Správa kampaní, persistentní postavy a sdílené herní session - již brzy!
          </p>
          <Link href="/roadmap" className="mt-4 inline-block text-primary hover:underline font-semibold transition">
            → Zjisti, co připravujeme! 🗺️
          </Link>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-muted-foreground">
          <p>🐭 Mausritter Tools © 2025</p>
          <p className="mt-2">
            Mausritter je © Games Omnivorous (neoficiální fan tool)
          </p>
          <div className="flex gap-4 justify-center mt-4">
            <Link href="/generators" className="hover:text-primary transition">
              Generátory
            </Link>
            <Link href="/roadmap" className="hover:text-primary transition">
              Roadmap
            </Link>
            <a href={`${apiUrl}/docs`} target="_blank" rel="noopener noreferrer" className="hover:text-primary transition">
              API Docs
            </a>
            <a href="https://mausritter.com" target="_blank" rel="noopener noreferrer" className="hover:text-primary transition">
              Mausritter
            </a>
          </div>
        </footer>
      </div>
    </main>
  )
}

import type { Mouse } from '@/lib/types/campaign';

interface PartyPanelProps {
  party: Mouse[];
  onMouseClick: (mouse: Mouse) => void;
}

export default function PartyPanel({ party, onMouseClick }: PartyPanelProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-4 mb-6">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-xl font-semibold text-amber-900">
          🐭 Party
        </h2>
        <button className="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700 transition">
          + Add Mouse
        </button>
      </div>

      <div className="flex gap-3 overflow-x-auto">
        {party.length === 0 ? (
          <div className="text-gray-500 text-center w-full py-4">
            No mice in the party yet. Add your first mouse!
          </div>
        ) : (
          party.map((mouse) => (
            <button
              key={mouse.id}
              onClick={() => onMouseClick(mouse)}
              className="flex-shrink-0 flex flex-col items-center p-3 bg-amber-50 rounded-lg hover:bg-amber-100 transition border-2 border-amber-200 hover:border-amber-400 cursor-pointer group"
            >
              {/* Mouse Icon */}
              <div className="text-4xl mb-2 group-hover:scale-110 transition-transform">
                🐭
              </div>

              {/* Mouse Name */}
              <div className="font-semibold text-amber-900 text-sm">
                {mouse.name}
              </div>

              {/* HP Bar */}
              <div className="w-full mt-2">
                <div className="flex justify-between text-xs text-gray-600 mb-1">
                  <span>HP</span>
                  <span>{mouse.hp}/{mouse.maxHp}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      mouse.hp > mouse.maxHp * 0.5
                        ? 'bg-green-500'
                        : mouse.hp > mouse.maxHp * 0.25
                        ? 'bg-yellow-500'
                        : 'bg-red-500'
                    }`}
                    style={{ width: `${(mouse.hp / mouse.maxHp) * 100}%` }}
                  />
                </div>
              </div>

              {/* Conditions Badge */}
              {mouse.conditions && mouse.conditions.length > 0 && (
                <div className="mt-2 text-xs bg-red-100 text-red-800 px-2 py-1 rounded">
                  {mouse.conditions[0]}
                </div>
              )}
            </button>
          ))
        )}
      </div>
    </div>
  );
}

import type { Mouse } from '@/lib/types/campaign';

interface MouseDetailSidebarProps {
  mouse: Mouse | null;
  isOpen: boolean;
  onClose: () => void;
}

export default function MouseDetailSidebar({ mouse, isOpen, onClose }: MouseDetailSidebarProps) {
  if (!isOpen || !mouse) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-30 z-40"
        onClick={onClose}
      />

      {/* Sidebar */}
      <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl z-50 overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-amber-600 text-white p-4 flex items-center justify-between">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <span>🐭</span>
            <span>{mouse.name}</span>
          </h2>
          <button
            onClick={onClose}
            className="text-white hover:text-amber-200 text-2xl leading-none"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Basic Stats */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-amber-900 mb-3">
              Stats
            </h3>
            <div className="space-y-3">
              {/* HP */}
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium">Hit Points (HP)</span>
                  <span className="font-bold">{mouse.hp} / {mouse.maxHp}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full transition-all ${
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

              {/* Grit */}
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium">Grit</span>
                  <span className="font-bold">{mouse.grit} / {mouse.maxGrit}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="h-3 rounded-full bg-blue-500 transition-all"
                    style={{ width: `${(mouse.grit / mouse.maxGrit) * 100}%` }}
                  />
                </div>
              </div>

              {/* Pips */}
              <div className="flex justify-between text-sm">
                <span className="font-medium">Pips</span>
                <span className="font-bold">{mouse.pips}</span>
              </div>

              {/* Level */}
              <div className="flex justify-between text-sm">
                <span className="font-medium">Level</span>
                <span className="font-bold">{mouse.level}</span>
              </div>
            </div>
          </div>

          {/* Character Info */}
          {mouse.background && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-amber-900 mb-3">
                Character Info
              </h3>
              <div className="space-y-2 text-sm">
                <div>
                  <span className="font-medium text-gray-600">Background:</span>
                  <span className="ml-2">{mouse.background}</span>
                </div>
                {mouse.disposition && (
                  <div>
                    <span className="font-medium text-gray-600">Disposition:</span>
                    <span className="ml-2">{mouse.disposition}</span>
                  </div>
                )}
                {mouse.birthsign && (
                  <div>
                    <span className="font-medium text-gray-600">Birthsign:</span>
                    <span className="ml-2">{mouse.birthsign}</span>
                  </div>
                )}
                {mouse.coat && (
                  <div>
                    <span className="font-medium text-gray-600">Coat:</span>
                    <span className="ml-2">{mouse.coat}</span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Conditions */}
          {mouse.conditions && mouse.conditions.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-amber-900 mb-3">
                Conditions
              </h3>
              <div className="flex flex-wrap gap-2">
                {mouse.conditions.map((condition, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium"
                  >
                    {condition}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Inventory - Placeholder */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-amber-900 mb-3">
              Inventory
            </h3>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center text-gray-500">
              <p className="mb-2">🎒</p>
              <p className="text-sm">Inventory system coming soon</p>
              <p className="text-xs mt-1">Will show equipped items, carried items, etc.</p>
            </div>
          </div>

          {/* Notes */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-amber-900 mb-3">
              Notes
            </h3>
            <textarea
              className="w-full h-24 p-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-amber-500"
              placeholder="Add notes about this character..."
              defaultValue={mouse.notes || ''}
            />
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            <button className="flex-1 px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-700 transition">
              Edit Character
            </button>
            <button className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition">
              Export
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

import type { CampaignState } from '@/lib/types/campaign';

interface TimeWeatherPanelProps {
  campaign: CampaignState;
  onUpdateCampaign: (campaign: CampaignState) => void;
}

export default function TimeWeatherPanel({ campaign, onUpdateCampaign }: TimeWeatherPanelProps) {
  const watchOrder = ['morning', 'afternoon', 'evening', 'night'] as const;

  const handleNextWatch = () => {
    const currentIndex = watchOrder.indexOf(campaign.currentWatch);
    const nextIndex = (currentIndex + 1) % watchOrder.length;
    const nextWatch = watchOrder[nextIndex];

    const updatedCampaign = {
      ...campaign,
      currentWatch: nextWatch,
      currentDay: nextWatch === 'morning' ? campaign.currentDay + 1 : campaign.currentDay,
    };

    onUpdateCampaign(updatedCampaign);
  };

  const handleRollWeather = () => {
    // Roll 2d6 for weather
    const die1 = Math.floor(Math.random() * 6) + 1;
    const die2 = Math.floor(Math.random() * 6) + 1;
    const total = die1 + die2;

    let weatherResult = 'Normal';
    let effects: string[] = [];

    if (total <= 3) {
      weatherResult = 'Harsh Weather';
      effects = ['Movement stopped', 'Seek shelter'];
    } else if (total >= 10 && total <= 11) {
      weatherResult = 'Favourable';
      effects = ['Comfortable conditions'];
    } else if (total === 12) {
      weatherResult = 'Extreme!';
      effects = ['Roll on seasonal table'];
    }

    const updatedCampaign = {
      ...campaign,
      weather: {
        ...campaign.weather,
        current: weatherResult,
        roll: total,
        effects,
      },
      weatherLog: [
        ...campaign.weatherLog,
        {
          current: weatherResult,
          roll: total,
          season: campaign.weather.season,
          effects,
        },
      ],
    };

    onUpdateCampaign(updatedCampaign);
  };

  const getWatchEmoji = (watch: string) => {
    switch (watch) {
      case 'morning':
        return '🌅';
      case 'afternoon':
        return '☀️';
      case 'evening':
        return '🌆';
      case 'night':
        return '🌙';
      default:
        return '⏰';
    }
  };

  const getWeatherEmoji = (weather: string) => {
    if (weather.includes('Harsh')) return '⛈️';
    if (weather.includes('Favourable')) return '☀️';
    if (weather.includes('Extreme')) return '🌪️';
    return '🌤️';
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      {/* Time Tracker */}
      <div className="bg-white rounded-lg shadow-lg p-4">
        <h3 className="text-lg font-semibold text-amber-900 mb-3 flex items-center gap-2">
          <span>📅</span>
          <span>Time</span>
        </h3>
        <div className="space-y-2">
          <div className="text-sm text-gray-600">
            Day <span className="font-bold text-lg text-amber-900">{campaign.currentDay}</span>
          </div>
          <div className="text-sm text-gray-600">
            Watch:{' '}
            <span className="font-bold text-lg text-amber-900">
              {getWatchEmoji(campaign.currentWatch)} {campaign.currentWatch.charAt(0).toUpperCase() + campaign.currentWatch.slice(1)}
            </span>
          </div>
          <button
            onClick={handleNextWatch}
            className="w-full mt-3 px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-700 transition"
          >
            Next Watch →
          </button>
        </div>
      </div>

      {/* Weather */}
      <div className="bg-white rounded-lg shadow-lg p-4">
        <h3 className="text-lg font-semibold text-amber-900 mb-3 flex items-center gap-2">
          <span>{getWeatherEmoji(campaign.weather.current)}</span>
          <span>Weather</span>
        </h3>
        <div className="space-y-2">
          <div className="text-sm text-gray-600">
            Current:{' '}
            <span className="font-bold text-lg text-amber-900">
              {campaign.weather.current}
            </span>
          </div>
          <div className="text-xs text-gray-500">
            Last roll: {campaign.weather.roll} (2d6)
          </div>
          {campaign.weather.effects && campaign.weather.effects.length > 0 && (
            <div className="text-xs text-blue-600 mt-2">
              {campaign.weather.effects.join(', ')}
            </div>
          )}
          <button
            onClick={handleRollWeather}
            className="w-full mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            Roll Weather
          </button>
        </div>
      </div>

      {/* Encounter Tracker */}
      <div className="bg-white rounded-lg shadow-lg p-4">
        <h3 className="text-lg font-semibold text-amber-900 mb-3 flex items-center gap-2">
          <span>⚔️</span>
          <span>Encounters</span>
        </h3>
        <div className="space-y-2">
          <div className="text-sm text-gray-600">
            Active:{' '}
            <span className="font-bold text-lg text-amber-900">
              {campaign.encounters.filter((e) => e.active).length}
            </span>
          </div>
          <div className="text-xs text-gray-500">
            Next roll: {campaign.currentWatch === 'morning' || campaign.currentWatch === 'evening' ? 'Now!' : 'Morning/Evening'}
          </div>
          <button
            className="w-full mt-3 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
          >
            Roll Encounter
          </button>
        </div>
      </div>
    </div>
  );
}

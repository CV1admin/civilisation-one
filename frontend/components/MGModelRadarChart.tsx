import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { metric: '\u03b1 (Awareness)', value: 0.98 },
  { metric: 'E (Energy)', value: 0.94 },
  { metric: 'T (Time)', value: 0.99 },
  { metric: 'Q (Quantime)', value: 0.92 },
];

export default function MGModelRadarChart() {
  return (
    <div className="p-4 bg-white rounded-2xl shadow-xl w-full max-w-xl mx-auto">
      <h2 className="text-xl font-bold text-center mb-4">MG Model Cognitive Radar</h2>
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="metric" tick={{ fontSize: 12 }} />
          <PolarRadiusAxis angle={30} domain={[0, 1]} tickCount={6} />
          <Radar name="Score" dataKey="value" stroke="#6366f1" fill="#6366f1" fillOpacity={0.6} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

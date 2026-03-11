"use client";
import { LightBulbIcon } from '@heroicons/react/24/outline';

type InsightProps = {
  result: {
    name: string;
    confidence: number;
    calories?: number;
  };
};

export default function InsightPanel({ result }: InsightProps) {
  const confidencePct = Math.round(result.confidence * 100);
  return (
    <section className="card mt-8">
      <h2 className="text-2xl font-semibold flex items-center gap-2 text-primary mb-4">
        <LightBulbIcon className="h-6 w-6" />
        What Did We See?
      </h2>
      <p className="text-lg mb-2">
        <span className="font-medium">Food:</span> {result.name}
      </p>
      <p className="text-lg mb-2">
        <span className="font-medium">Confidence:</span> {confidencePct}%
      </p>
      {result.calories && (
        <p className="text-lg">
          <span className="font-medium">Estimated Calories:</span> {result.calories} kcal
        </p>
      )}
    </section>
  );
}

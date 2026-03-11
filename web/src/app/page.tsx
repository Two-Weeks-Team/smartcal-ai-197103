"use client";
import { useCallback, useEffect, useState } from "react";
import Hero from '@/components/Hero';
import InsightPanel from '@/components/InsightPanel';
import CollectionPanel from '@/components/CollectionPanel';
import StatsStrip from '@/components/StatsStrip';
import StatePanel from '@/components/StatePanel';
import { recognizeFood, fetchItems } from '@/lib/api';

type FoodResult = {
  name: string;
  confidence: number;
  calories?: number;
};

export default function HomePage() {
  const [foodResult, setFoodResult] = useState<FoodResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savedItems, setSavedItems] = useState<any[]>([]);
  const [itemsLoading, setItemsLoading] = useState(true);

  const loadSavedItems = useCallback(async () => {
    try {
      const data = await fetchItems();
      setSavedItems(data.items ?? []);
    } catch (e) {
      console.error(e);
    } finally {
      setItemsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSavedItems();
  }, [loadSavedItems]);

  const handleImageUpload = async (file: File) => {
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('image', file);
      const data = await recognizeFood(formData);
      const result: FoodResult = {
        name: data.food_item?.name ?? 'Unknown',
        confidence: data.food_item?.confidence ?? 0,
        calories: data.food_item?.calories
      };
      setFoodResult(result);
    } catch (e: any) {
      setError(e.message || 'Unexpected error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex-1 flex flex-col gap-8 p-6 md:p-12 max-w-5xl mx-auto">
      <Hero onUpload={handleImageUpload} />
      <StatsStrip />
      {loading && <StatePanel state="loading" />}
      {error && <StatePanel state="error" message={error} />}
      {foodResult && <InsightPanel result={foodResult} />}
      <section className="mt-8">
        <h2 className="text-2xl font-semibold mb-4 text-primary">Recent Food Log</h2>
        {itemsLoading ? (
          <StatePanel state="loading" />
        ) : savedItems.length === 0 ? (
          <StatePanel state="empty" message="No logged meals yet. Try the Smart Plate above!" />
        ) : (
          <CollectionPanel items={savedItems} />
        )}
      </section>
    </main>
  );
}

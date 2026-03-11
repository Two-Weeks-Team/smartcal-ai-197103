export async function fetchItems() {
  const base = process.env.NEXT_PUBLIC_API_URL ?? '';
  const res = await fetch(`${base}/items`);
  if (!res.ok) {
    throw new Error('Failed to fetch items');
  }
  return res.json();
}

export async function generateMealPlan(payload: { user_id: string; preferences: any }) {
  const base = process.env.NEXT_PUBLIC_API_URL ?? '';
  const res = await fetch(`${base}/generate-meal-plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error('Meal plan generation failed');
  }
  return res.json();
}

export async function recognizeFood(formData: FormData) {
  const base = process.env.NEXT_PUBLIC_API_URL ?? '';
  const res = await fetch(`${base}/recognize-food`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) {
    throw new Error('Food recognition failed');
  }
  return res.json();
}

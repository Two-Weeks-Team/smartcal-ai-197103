"use client";
import { useRef } from "react";
import { CameraIcon } from '@heroicons/react/24/outline';

type HeroProps = {
  onUpload: (file: File) => Promise<void>;
};

export default function Hero({ onUpload }: HeroProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleButtonClick = () => {
    inputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await onUpload(file);
    }
  };

  return (
    <section className="text-center py-12">
      <h1 className="text-4xl md:text-5xl font-bold text-primary mb-4">
        SmartCal AI
      </h1>
      <p className="text-lg text-foreground mb-6">
        Revolutionize your calorie tracking with AI‑powered personalization and smart food recognition.
      </p>
      <button
        onClick={handleButtonClick}
        className="inline-flex items-center gap-2 bg-accent text-white px-6 py-3 rounded-radius shadow-shadow hover:bg-accent/90 transition"
      >
        <CameraIcon className="h-5 w-5" />
        Snap a Meal (Smart Plate)
      </button>
      <input
        type="file"
        accept="image/*"
        ref={inputRef}
        className="hidden"
        onChange={handleFileChange}
      />
    </section>
  );
}

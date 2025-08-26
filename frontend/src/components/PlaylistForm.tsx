import React, { useState } from "react";
import Papa from "papaparse";
import ErrorCard from "./ErrorCard";
import RecommendationCard from "./RecommendationCard";
import type { PlaylistResponse } from "../types/playlist";
import DataTable from "./DataTable";
import CsvUpload from "./CsvUpload";

export default function PlaylistForm() {
  const [form, setForm] = useState({
    time_of_day: "",
    calendar_event: "",
    location: "",
    social_post: "",
  });

  const [error, setError] = useState<string | null>(null);
  const [csvData, setCsvData] = useState<any[]>([]);
  const [recommendation, setRecommendation] = useState<PlaylistResponse | null>(
    null
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleCSVUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        setCsvData(results.data as any[]);
      },
    });
  };

  const handleRowSelect = (row: any) => {
    setForm({
      time_of_day: row.time || row.timestamp,
      calendar_event: row.event,
      location: row.location,
      social_post: "",
    });
  };

  const fetchRecommendation = async () => {
    try {
      const params = new URLSearchParams(
        Object.entries(form).filter(([_, v]) => v)
      );
      const response = await fetch(
        `http://localhost:8000/api/v1/recommend/?${params.toString()}`
      );
      const data = await response.json();
      setRecommendation(data);
      console.log("Received recommendation:", data);
    } catch (error) {
      setError("Failed to fetch recommendation: " + (error as Error).message);
    }
  };

  return (
    <div className="border-4 border-dotted border-white p-6 rounded-xl shadow space-y-6">
      <div className="space-y-3">
        <input
          type="text"
          name="time_of_day"
          placeholder="Time of Day (e.g. 09:00)"
          value={form.time_of_day}
          onChange={handleInputChange}
          className="border p-2 rounded w-full"
        />
        <input
          type="text"
          name="calendar_event"
          placeholder="Calendar Event"
          value={form.calendar_event}
          onChange={handleInputChange}
          className="border p-2 rounded w-full"
        />
        <input
          type="text"
          name="location"
          placeholder="Location"
          value={form.location}
          onChange={handleInputChange}
          className="border p-2 rounded w-full"
        />
        <input
          type="text"
          name="social_post"
          placeholder="Social Media Post"
          value={form.social_post}
          onChange={handleInputChange}
          className="border p-2 rounded w-full"
        />
      </div>

      <button
        onClick={fetchRecommendation}
        className="bg-nothing-red text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Get Recommendation
      </button>

      <CsvUpload onUpload={handleCSVUpload} />

      <DataTable data={csvData} onRowSelect={handleRowSelect} />

      {recommendation && <RecommendationCard recommendation={recommendation} />}

      {error && <ErrorCard message={error} onDismiss={() => setError(null)} />}
    </div>
  );
}

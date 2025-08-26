import React from "react";
import type { PlaylistResponse } from "../types/playlist";

const RecommendationCard: React.FC<{ recommendation: PlaylistResponse }> = ({
  recommendation,
}) => (
  <div className="border-4 border-dotted border-white bg-gray-500 mt-6 p-4 border rounded">
    <h3 className="font-semibold">Recommended Playlist</h3>
    <h3>
      <b>Name:</b> {recommendation.mood}
    </h3>
    <ul className="list-disc pl-5">
      {recommendation.playlist.map((t, i) => (
        <li key={i}>{t}</li>
      ))}
    </ul>
  </div>
);

export default RecommendationCard;

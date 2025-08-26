import React from "react";
import type { ErrorCardProps } from "../types/error";

const ErrorCard: React.FC<ErrorCardProps> = ({ message, onDismiss }) => (
  <div className="relative max-w-md mx-auto my-4 p-4 pr-10 border border-red-400 bg-red-100 text-red-800 rounded-lg shadow">
    <button
      className="absolute top-2 right-2 text-red-500 hover:text-red-700 text-base px-1 py-0.5 rounded focus:outline-none"
      onClick={onDismiss}
      aria-label="Dismiss"
      type="button"
    >
      &times;
    </button>
    <div className="font-bold mb-2">Error</div>
    <div>{message}</div>
  </div>
);

export default ErrorCard;

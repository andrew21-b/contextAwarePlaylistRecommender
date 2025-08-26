import React from "react";
import type { CsvUploadProps } from "../types/upload";

const CsvUpload: React.FC<CsvUploadProps> = ({ onUpload }) => (
  <div>
    <label htmlFor="csv-upload" className="cursor-pointer">
      <h3 className="font-semibold mb-2">Upload Calendar</h3>
      <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
        <span className="font-semibold">Click to upload</span> or drag and drop
      </p>
      <input
        id="csv-upload"
        type="file"
        accept=".csv"
        className="hidden"
        onChange={onUpload}
      />
    </label>
  </div>
);

export default CsvUpload;

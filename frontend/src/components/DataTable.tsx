import React from "react";
import type { DataTableProps } from "../types/table";

const DataTable: React.FC<DataTableProps> = ({ data, onRowSelect }) => {
  if (!data.length) return null;
  return (
    <table className="border mt-4 w-full text-sm">
      <thead className="bg-gray-500">
        <tr>
          {Object.keys(data[0]).map((col) => (
            <th key={col} className="border px-2 py-1">
              {col}
            </th>
          ))}
        </tr>
      </thead>
      <tbody className="bg-gray-500">
        {data.map((row, idx) => (
          <tr
            key={idx}
            onClick={() => onRowSelect(row)}
            className="cursor-pointer hover:bg-gray-100"
          >
            {Object.values(row).map((val, i) => (
              <td key={i} className="border px-2 py-1">
                {val as string}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DataTable;

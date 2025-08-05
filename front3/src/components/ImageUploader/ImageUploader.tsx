// src/components/ImageUploader/ImageUploader.tsx

import { useState } from "react";
import "./ImageUploader.css";

interface ImageUploaderProps {
  onUpload: (files: File[]) => void;
  multiple?: boolean;
}

export default function ImageUploader({ onUpload, multiple = true }: ImageUploaderProps) {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    const filesArray = Array.from(e.target.files);
    setSelectedFiles(filesArray);
    onUpload(filesArray);
  };

  return (
    <div className="image-uploader">
      <label htmlFor="file-upload" className="upload-label">
        Select Image{multiple ? "s" : ""}
      </label>
      <input
        id="file-upload"
        type="file"
        multiple={multiple}
        accept="image/*"
        onChange={handleFileChange}
        className="file-input"
      />
      {selectedFiles.length > 0 && (
        <ul className="file-list">
          {selectedFiles.map((file, i) => (
            <li key={i}>{file.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
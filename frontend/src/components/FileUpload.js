import React, { useState } from 'react';
import { toast } from 'react-toastify';

const FileUpload = () => {
  const [file, setFile] = useState(null);

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const onUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'kalendarz.ics');
        document.body.appendChild(link);
        link.click();
        link.remove();
        toast.success('Wygenerowano plik kalendarza 😄');
      } else {
        const errorData = await response.text();
        toast.error(errorData);
      }
    } catch (error) {
      toast.error(error.message);
    }
  };

  return (
    <div>
      <input type="file" onChange={onFileChange} />
      <button className="custom-button" onClick={onUpload} disabled={!file}>Generuj plik .ics</button>
    </div>
  );
};

export default FileUpload;
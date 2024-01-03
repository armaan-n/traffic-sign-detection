'use client';

import { SetStateAction, useState } from "react";
import { FileUploader } from "react-drag-drop-files";

const fileTypes = ["JPG", "PNG", "GIF"];
const requestUrl = "http://127.0.0.1:5000/process";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [image, setImage] = useState<string | null>(null);
  const [cat, setCat] = useState<string | null>(null);

  function handleChange(file: File) {
    setFile(file);
  }

  function processFile() {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      fetch(requestUrl + "/get_image", {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        body: formData
      }).then(response => response.blob())
        .then(responseImage => setImage(URL.createObjectURL(responseImage)))
        .catch(error => console.error(error));

      fetch(requestUrl + "/get_class", {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        body: formData
      }).then(response => response.json())
        .then(response => setCat(response["class"]))
        .catch(error => console.error(error));
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <FileUploader handleChange={handleChange} name="file" types={fileTypes} />
      {cat && <label>{cat}</label>}
      {image && <img src={image}></img>}
      <button onClick={processFile}>Process</button>
    </main>
  )
}

import React, { useState } from 'react';
import axios from 'axios';
import Dashboards from './components/Dashboards';

function App() {
  const [video, setVideo] = useState(null);
  const [videoUrl, setVideoUrl] = useState('');
  const [processing, setProcessing] = useState(false);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('video', video);
    setProcessing(true);
    const res = await axios.post('http://localhost:5000/upload', formData);
    setVideoUrl('http://localhost:5000/video');
    setProcessing(false);
  };

  return (
    <div className="min-h-screen p-6 bg-gray-100 text-center">
      <h1 className="text-3xl font-bold mb-4 text-indigo-700">
        Smart Emergency Vehicle Clearance System
      </h1>

      <input
        type="file"
        accept="video/*"
        onChange={(e) => setVideo(e.target.files[0])}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        disabled={!video || processing}
        className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
      >
        {processing ? 'Processing...' : 'Process'}
      </button>

      {videoUrl && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
          <div className="col-span-2">
            <h2 className="text-xl font-semibold text-gray-700 mb-2">Live Tracking</h2>
            <video src={videoUrl} controls className="w-full rounded shadow" />
          </div>

          <Dashboards />
        </div>
      )}
    </div>
  );
}

export default App;

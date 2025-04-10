import React, { useState, useEffect } from 'react';

function Dashboards() {
  const [ambulanceTimer, setAmbulanceTimer] = useState(0);
  const [vehicleTimer, setVehicleTimer] = useState(0);
  const [detected, setDetected] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      if (detected) {
        setAmbulanceTimer(prev => prev + 1);
        setVehicleTimer(0);
      } else {
        setVehicleTimer(prev => prev + 1);
        setAmbulanceTimer(0);
      }

      // Auto-clear detection after 5s
      if (vehicleTimer >= 5) setDetected(false);
    }, 1000);

    return () => clearInterval(interval);
  }, [detected, vehicleTimer]);

  return (
    <div className="grid gap-4">
      {/* Ambulance Dashboard */}
      <div className="bg-white p-4 shadow-md rounded">
        <h3 className="text-lg font-bold text-blue-700 mb-2">Ambulance Dashboard</h3>
        {detected ? (
          <p className="text-green-600 font-semibold">
            Vehicle is detected! Time: {ambulanceTimer}s
          </p>
        ) : vehicleTimer < 5 ? (
          <p className="text-yellow-600 font-semibold">
            No recent detection. Waiting... {vehicleTimer}s
          </p>
        ) : (
          <p className="text-gray-500 font-semibold">Lane is clear.</p>
        )}
      </div>

      {/* Vehicle Dashboard */}
      <div className="bg-white p-4 shadow-md rounded">
        <h3 className="text-lg font-bold text-red-700 mb-2">Vehicle Dashboard</h3>
        {detected ? (
          <div className="animate-pulse text-red-600 font-semibold">
            🚨 Clear the lane for Ambulance! {ambulanceTimer}s
          </div>
        ) : vehicleTimer < 5 ? (
          <p className="text-orange-500 font-semibold">
            Cooldown: Give way, ambulance is closer! {vehicleTimer}s
          </p>
        ) : (
          <p className="text-gray-600 font-semibold">No ambulance is near you.</p>
        )}
      </div>
    </div>
  );
}

export default Dashboards;

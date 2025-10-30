import React, { useState, useEffect } from "react";
import { LuRefreshCcw } from "react-icons/lu";

const Dashboard = () => {
  const [status, setStatus] = useState({
    mode: "camera",
    camera_detected: false,
    ldr_value: null,
    last_update: null,
  });

  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:8000/status"); // FastAPI endpoint
        if (!res.ok) throw new Error("Server error");
        const data = await res.json();
        setStatus(data);
        setError("");
      } catch (err) {
        setError("⚠️ Backend not connected");
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative bg-gray-900/80 border border-cyan-500/30 shadow-[0_0_25px_#00ffff40] rounded-3xl p-10 w-[460px] text-white backdrop-blur-md transition-transform hover:scale-105 hover:shadow-[0_0_40px_#00ffff60]">
      <h2 className="text-3xl font-extrabold mb-6 text-center text-cyan-400">
        Smart Object Detection Dashboard
      </h2>

      {error && <div className="text-red-500 text-center text-sm mb-4">{error}</div>}

      <div className="space-y-3 text-center">
        <div>
          <span className="font-semibold">Current Mode:</span>{" "}
          <span className="text-cyan-400 font-bold uppercase">
            {status.mode}
          </span>
        </div>

        <div>
          <span className="font-semibold">Camera Status:</span>{" "}
          <span
            className={
              status.camera_detected
                ? "text-green-500 font-bold"
                : "text-gray-500"
            }
          >
            {status.camera_detected ? "Object Detected" : "No Object"}
          </span>
        </div>

        <div>
          <span className="font-semibold">LDR Value:</span>{" "}
          <span className="text-blue-400 font-bold">
            {status.ldr_value !== null ? status.ldr_value : "—"}
          </span>
        </div>

        <div>
          <span className="font-semibold">Last Updated:</span>{" "}
          <span className="text-yellow-400 font-semibold">
            {status.last_update
              ? new Date(status.last_update * 1000).toLocaleTimeString()
              : "—"}
          </span>
        </div>
      </div>

      <p className="mt-6 text-xs text-gray-300 text-center flex items-center justify-center gap-2">
        <LuRefreshCcw className="animate-spin-slow text-cyan-400" />
        Updates every 1 second
      </p>
    </div>
  );
};

export default Dashboard;

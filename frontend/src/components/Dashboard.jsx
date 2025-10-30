import React, { useState, useEffect } from "react";
import { LuRefreshCcw } from "react-icons/lu";

const Dashboard = () => {
  const [status, setStatus] = useState({
    mode: "camera",
    camera_detected: false,
    ldr_value: "—",
    last_update: null,
  });

  const [isFetching, setIsFetching] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      setIsFetching(true);
      try {
        const res = await fetch("http://localhost:8000/status");
        if (!res.ok) throw new Error("Server error");
        const data = await res.json();

        // Format and display latest data
        setStatus({
          mode: data.mode || "—",
          camera_detected: data.camera_detected || false,
          ldr_value: data.ldr_value !== null ? data.ldr_value : "—",
          last_update: data.last_update ? data.last_update : null,
        });

        setError("");
      } catch (err) {
        setError("⚠️ Unable to connect to backend");
      }
      setIsFetching(false);
    };

    fetchData();
    const interval = setInterval(fetchData, 1000); // fetch every second
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-gray-900 via-gray-800 to-black text-white">
      <div className="bg-gray-900/80 border border-cyan-400/40 shadow-[0_0_25px_#00ffff40] rounded-3xl p-10 w-[420px] backdrop-blur-md transition-transform hover:scale-105 hover:shadow-[0_0_40px_#00ffff60]">
        <h2 className="text-3xl font-extrabold mb-6 text-center text-cyan-400">
          Hybrid Object Detection
        </h2>

        {error && (
          <div className="text-red-500 text-center text-sm mb-4">{error}</div>
        )}

        <div className="space-y-3 text-center">
          <div>
            <span className="font-semibold text-gray-300">Current Mode: </span>
            <span
              className={`font-bold uppercase ${
                status.mode === "camera" ? "text-green-400" : "text-blue-400"
              }`}
            >
              {status.mode}
            </span>
          </div>

          <div>
            <span className="font-semibold text-gray-300">Camera Status: </span>
            <span
              className={
                status.camera_detected
                  ? "text-green-500 font-bold"
                  : "text-gray-500 font-semibold"
              }
            >
              {status.camera_detected ? "Object Detected" : "No Object"}
            </span>
          </div>

          <div>
            <span className="font-semibold text-gray-300">LDR Value: </span>
            <span className="text-yellow-400 font-bold">
              {status.ldr_value}
            </span>
          </div>

          <div>
            <span className="font-semibold text-gray-300">Last Updated: </span>
            <span className="text-cyan-400 font-semibold">
              {status.last_update
                ? new Date(status.last_update * 1000).toLocaleTimeString()
                : "—"}
            </span>
          </div>
        </div>

        <p className="mt-6 text-xs text-gray-400 text-center flex items-center justify-center gap-2">
          <LuRefreshCcw
            className={`${
              isFetching ? "animate-spin" : ""
            } text-cyan-400 transition-all`}
          />
          Updates every 1 second
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
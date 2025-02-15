import React, { useState, useEffect } from "react";
import DownloadButton from "@/app/components/DownloadButton";
import "@/app/style/loadAnimation.css";

type VideoUrl = {
  videoUrl: string | null;
  loading: boolean;
};

const VideoComponent = ({ videoUrl, loading }: VideoUrl) => {
  if (loading) {
    return (
      <div
        className="w-full h-[27rem] border-slate-100/30 shadow-lg rounded-xl dark:bg-gray-200/30 border-gray-200/30 flex flex-col items-center justify-center"
        style={{ backgroundColor: "#1d2630" }}
      >
        <div className="spinner-box">
          <div className="blue-orbit leo"></div>

          <div className="green-orbit leo"></div>

          <div className="red-orbit leo"></div>

          <div className="white-orbit w1 leo"></div>
          <div className="white-orbit w2 leo"></div>
          <div className="white-orbit w3 leo"></div>
        </div>
        <p className="loading-text mt-4">LOADING…</p>
      </div>
    );
  }

  if (!videoUrl) {
    return (
      <div
        className="w-full h-[27rem] border-slate-100/30 shadow-lg rounded-xl dark:bg-gray-200/30 border-gray-200/30 flex items-center justify-center"
        style={{ backgroundColor: "#1d2630" }}
      >
        {/* なにも表示しないスペース */}
        <p className="text-gray-400">動画がありません</p>
      </div>
    );
  }

  return (
    <div className="relative w-full flex justify-center">
      {/* ✅ 動画プレーヤー */}
      {!loading && (
        <video
          controls
          width="768"
          className="object-fill rounded-xl"
          autoPlay
          muted
        >
          <source src={videoUrl} type="video/mp4" />
          お使いのブラウザは video タグをサポートしていません。
        </video>
      )}
    </div>
  );
};

export default VideoComponent;

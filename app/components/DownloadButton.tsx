import { useState } from "react";
import fetchVideo from "@/app/utils/fetchVideo";


type DownloadButtonProps =  {
    videoUrl: string;
}

const DawnloadButton = ({videoUrl}:DownloadButtonProps) => {
    const [loading, setLoading] = useState(false);

    const handleDownload = async () => {
    setLoading(true);
    const blob = await fetchVideo(videoUrl);
    setLoading(false);

    if (!blob) return;

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "video.mp4"; // 🔹 MP4形式でダウンロード
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    };

    return (
    <button 
        onClick={handleDownload} 
        disabled={loading} 
        className="p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
    >
        {loading ? "Downloading..." : "Download MP4"}
    </button>
    );
}

export default DawnloadButton;
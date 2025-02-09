"use client";

import React, { useState } from "react";
import { readStreamableValue } from "ai/rsc";
import { StreamEvent } from "@langchain/core/tracers/log_stream";
import Tabs from "./components/Tabs";
import Forms from "./components/form";
import VideoComponent from "@/app/components/VIdeo";



export default function Page() {
    const [videoUrl, setVideoUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [userPrompt, setUserPrompt] = useState("");
    


    async function handleSubmit(e: React.FormEvent) {
        setLoading(true);
        const defulatpath = process.env.NEXT_PUBLIC_API_URL

        console.log(defulatpath)
        const path =  defulatpath+"/api/prompt";
        e.preventDefault();
        if (!userPrompt) return;
        // VideoIdsession管理
        const videoId = "test";

        try {
            // 1. プロンプトを送信
            
            const videoResponse = await fetch(path, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_prompt: userPrompt, video_id: videoId }),
            });

            if (!videoResponse.ok) {
                throw new Error("動画生成に失敗しました。");
            }

            const blob = await videoResponse.blob();
            const url = URL.createObjectURL(blob);
            setVideoUrl(url);
        } catch (err) {
            setError((err as Error).message);
        } finally {
            setLoading(false);
        }
    }



    return (
        <div className="flex flex-col w-full h-full gap-2">
            <h1>動画生成</h1>

            <Forms input={userPrompt} handleSubmit={handleSubmit} setInput={setUserPrompt} loading={loading} />

            <Tabs />  

            {error && <p style={{ color: "red" }}>{error}</p>}
            
            {videoUrl && (
                <VideoComponent videoUrl={videoUrl} />
            )}


        </div>
    );
}

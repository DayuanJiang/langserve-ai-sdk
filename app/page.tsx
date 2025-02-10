"use client";
import React, { useState, useEffect } from "react";
import Tabs from "./components/Tabs";
import TextInputForm from "./components/TextInputForm";
import ClipboardCopy from "./components/ClipboardCopy";
import VideoComponent from "@/app/components/VIdeo";
import Headers from "@/app/components/header";
import { examplePrompt,examplePromptfilter } from "@/app/data/examplePrompt";
import DawnloadButton from "@/app/components/DownloadButton";


export default function Page() {
    const [videoUrl, setVideoUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [userPrompt, setUserPrompt] = useState("");
    const [activeTab, setActiveTab] = useState(0);
    const [filteredExamplePrompt, setFilteredExamplePrompt] = useState(examplePrompt.generateAnimationPrompt);


    useEffect(()=>{
        setFilteredExamplePrompt(examplePromptfilter(examplePrompt, activeTab))
    },[activeTab])

    async function handleSubmit(e: React.FormEvent) {
        setLoading(true);
        const defulatpath = process.env.NEXT_PUBLIC_API_URL

        console.log(defulatpath)
        const path =  defulatpath+"/api/prompt";
        e.preventDefault();
        if (!userPrompt) return;
        // VideoId session管理はちょっと後で考える
        const videoId = "test_9";

        try {
            // 1. プロンプトを送信
            const videoResponse = await fetch(path, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_prompt: userPrompt, video_id: videoId ,instruction_type : activeTab}),
            });

            if (!videoResponse.ok) {
                throw new Error("動画生成に失敗しました。");
            }

            const blob = await videoResponse.blob();
            const url = URL.createObjectURL(blob);
            setVideoUrl(url);
        } catch (err) {
            setError((err as Error).message);
            console.log(error)
        } finally {
            setLoading(false);
        }
    }
    return (
        <div className="flex flex-col w-full gap-2">
            <Headers />
        <div className="flex w-full gap-2 justify-center">
            <div className="flex flex-col w-[40%] ">
                <div className="ml-10 mt-10">
                    <TextInputForm input={userPrompt}  handleSubmit={handleSubmit} setInput={setUserPrompt} loading={loading} />
                </div>
                
                <div className="mb-5">
                    <Tabs activeTab={activeTab} setActiveTab={setActiveTab} /> 
                </div>

                <div className="flex flex-col ml-10 mt-4 mb-1 gap-y-4">
                    {
                        filteredExamplePrompt.map((prompt) => {
                            return (
                                    <div className="flex flex-col gap-2">
                                        <ClipboardCopy defaultText={prompt.prompt} />
                                    </div>
                            );
                        })
                    }
                </div>
                
            </div>
            <div className="flex flex-col w-[40%] ">
                <VideoComponent videoUrl={videoUrl}/>
                
            </div>

        </div>   
        </div>
        
    );
}
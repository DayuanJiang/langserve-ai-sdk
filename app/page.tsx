"use client";

import React, { useState } from "react";
import { readStreamableValue } from "ai/rsc";
import { StreamEvent } from "@langchain/core/tracers/log_stream";
import Tabs from "./components/Tabs";
import TextInputForm from "./components/TextInputForm";
import ClipboardCopy from "./components/ClipboardCopy";
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
        <div className="flex flex-col w-full gap-2">
            <TextInputForm/>
            <Tabs />  
            <ClipboardCopy/>
            <ClipboardCopy/>
            <div className="flex flex-col w-full gap-2">
                <div
                    className="flex flex-col gap-2 px-2 h-[650px] overflow-y-auto"
                >
                    {
                        chatResults.map((item: any, i: number) => {
                            switch (item.type) {
                                case "tool":
                                    return (
                                        <div key={i} className="p-4 bg-slate-100 rounded-lg">
                                            <strong><code>{item.name}</code> Input</strong>
                                            <pre className="break-all text-sm">
                                                {JSON.stringify(item.input, null, 2)}
                                            </pre>
                                            {item.output && (
                                                <>
                                                    <strong>Tool result</strong>
                                                    <pre className="break-all text-sm">
                                                        {JSON.stringify(item.output, null, 2)}
                                                    </pre>
                                                </>
                                            )}
                                        </div>
                                    );
                                case "message":
                                    if (item.output === "") return null;
                                    return (
                                        <div key={i} className="p-4 bg-slate-100 rounded-lg prose">
                                            {item.output}
                                        </div>
                                    );
                                default:
                                    return null;
                            }
                        })
                    }
                </div>
            </div>
        </div>
    );
}

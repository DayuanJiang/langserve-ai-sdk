"use client";

import React, { useState } from "react";
import { readStreamableValue } from "ai/rsc";
import { StreamEvent } from "@langchain/core/tracers/log_stream";
import Tabs from "./components/Tabs";
import TextInputForm from "./components/TextInputForm";
import ClipboardCopy from "./components/ClipboardCopy";
import Forms from "./components/form";


export default function Page() {
    const [input, setInput] = useState("");

    async function handleSubmit(e: React.FormEvent) {
        const path = process.env.NEXT_PUBLIC_API_URL + "/api/prompts";
        e.preventDefault();
        if (!input) return;
        // とりあえず一つで管理する
        const vido_id = "test";
        const response = await fetch(path,{
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_prompt: input, video_id: vido_id }),
        });
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

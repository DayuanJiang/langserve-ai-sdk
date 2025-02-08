"use client";

import React, { useState } from "react";
import { readStreamableValue } from "ai/rsc";
import { StreamEvent } from "@langchain/core/tracers/log_stream";
import Tabs from "./components/Tabs";
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

            <Forms input={input} handleSubmit={handleSubmit} setInput={setInput} />

            <Tabs />  
        </div>
    );
}

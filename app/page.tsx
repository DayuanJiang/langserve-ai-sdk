"use client";

import React, { useState } from "react";
import { readStreamableValue } from "ai/rsc";
import { runAgent } from "./actions";
import { StreamEvent } from "@langchain/core/tracers/log_stream";
import Tabs from "./components/Tabs";

export default function Page() {
    const [input, setInput] = useState("");
    const [data, setData] = useState<StreamEvent[]>([]);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!input) return;
        const { streamData } = await runAgent(input);
        for await (const item of readStreamableValue(streamData)) {
            setData((prev) => [...prev, item]);
        }
    }
    let chatResults: any = [];
    for (let i = 0; i < data.length; i++) {
        switch (data[i].event) {
            case "on_tool_start":
                chatResults.push({
                    type: "tool",
                    runID: data[i].run_id,
                    input: data[i].data.input,
                    output: null,
                    name: data[i].name,
                });
                break;
            case "on_tool_end":
                const toolIndex = chatResults.findIndex(
                    (item: any) => item.runID === data[i].run_id
                );
                chatResults[toolIndex].output = data[i].data.output;
                break;
            case "on_chat_model_start":
                chatResults.push({
                    type: "message",
                    runID: data[i].run_id,
                    output: "",
                });
                break;
            case "on_chat_model_stream":
                const messageIndex = chatResults.findIndex(
                    (item: any) => item.runID === data[i].run_id
                );
                chatResults[messageIndex].output = chatResults[messageIndex].output + data[i].data.chunk.kwargs.content;
                break;
        }
    }

    return (
        <div className="flex flex-col w-full gap-2">
            <form onSubmit={handleSubmit} className="flex flex-col gap-2 w-1/3 m-10 relative">
            <textarea
                className="w-full h-40 px-5 py-2 pb-10 outline-none resize-none rounded-3xl shadow-lg"
                placeholder="文章を入力して"
                value={input}
                onChange={(e) => setInput(e.target.value)} 
            />
             <button
            type="submit"
            className={`absolute right-0 bottom-4 mb-1 mr-4 w-10 h-10 rounded-full flex items-center justify-center ${input ? "bg-slate-700" : "bg-gray-400 cursor-not-allowed"}`}
            disabled={!input}
        >
            <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-white" viewBox="0 0 24 24">
                <path fill="currentColor" d="M3 20V4l19 8M5 17l11.85-5L5 7v3.5l6 1.5l-6 1.5M5 17V7v6.5Z" />
            </svg>
        </button>
            </form>

            <Tabs />  

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

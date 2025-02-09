import React, { useState } from "react"; 


type VideoUrl = {
    videoUrl: string;
}

const VideoComponent = ({videoUrl}:VideoUrl) => {
    return (
        <div>
            <video controls width="400">
                <source src={videoUrl} type="video/mp4" />
                お使いのブラウザは video タグをサポートしていません。
            </video>
        </div>
    )
}

export default VideoComponent;
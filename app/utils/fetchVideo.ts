const fetchVideo = async(videoUrl:string):Promise<Blob| null> => { 
    try {
        const path = process.env.NEXT_PUBLIC_API_URL + "/api/get_video/" + videoUrl;
        const response = await fetch(
            path,
            {
                method: "GET",
                headers: { "Content-Type": "application/json" }
            }
        )

        if (!response.ok) {
            throw new Error("動画の取得に失敗しました");
        };
        const blob = await response.blob();
        return blob;
    } catch (err) {
        console.error("Error fetching video:" ,err);
        return null;
    }
}

export default fetchVideo;
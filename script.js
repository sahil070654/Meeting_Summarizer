// Replace with your Railway backend URL
const backendURL = "https://meetingsummarizer-production.up.railway.app";

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("uploadBtn").addEventListener("click", async () => {
        const fileInput = document.getElementById("audioFile");
        if (fileInput.files.length === 0) {
            alert("Please select an audio file");
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append("file", file);

        document.getElementById("transcript").innerText = "Transcribing...";
        document.getElementById("summary").innerText = "";

        try {
            console.log("Sending POST to:", `${backendURL}/summarize_audio/`);
            const response = await fetch(`${backendURL}/summarize_audio/`, {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Failed to summarize. Status: ${response.status}, ${text}`);
            }

            const data = await response.json();
            document.getElementById("transcript").innerText = data.transcript;
            document.getElementById("summary").innerText = data.summary;

        } catch (error) {
            document.getElementById("transcript").innerText = "";
            document.getElementById("summary").innerText = "Error: " + error.message;
        }
    });
});

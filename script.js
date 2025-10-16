// Set your Railway backend base URL
const backendURL = "https://meetingsummarizer-production.up.railway.app";

document.getElementById("uploadBtn").addEventListener("click", async () => {
    const fileInput = document.getElementById("audioFile");
    if (fileInput.files.length === 0) {
        alert("Please select an audio file");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    // Clear previous results
    document.getElementById("transcript").innerText = "Transcribing...";
    document.getElementById("summary").innerText = "";

    try {
        const response = await fetch(`${backendURL}/summarize_audio`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Failed to summarize. Check backend logs.");
        }

        const data = await response.json();
        document.getElementById("transcript").innerText = data.transcript;
        document.getElementById("summary").innerText = data.summary;

    } catch (error) {
        document.getElementById("transcript").innerText = "";
        document.getElementById("summary").innerText = "Error: " + error.message;
    }
});

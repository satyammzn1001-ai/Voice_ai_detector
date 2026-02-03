function uploadAudio() {
  const file = document.getElementById("audioFile").files[0];
  if (!file) return alert("Upload MP3 file");

  const reader = new FileReader();

  reader.onload = async () => {
    try {
      const base64 = reader.result.split(",")[1];

      const response = await fetch("https://voice-ai-detector-j0dx.onrender.com/detect-voice", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer MY_SECRET_KEY"
        },
        body: JSON.stringify({ audio_base64: base64 })
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error(err);
      }

      const data = await response.json();

      document.getElementById("result").innerHTML =
        `Result: <b>${data.result}</b><br>Confidence: ${data.confidence}`;

    } catch (error) {
      console.error(error);
      document.getElementById("result").innerHTML =
        `<span style="color:red">Error: ${error.message}</span>`;
    }
  };

  reader.readAsDataURL(file);
}

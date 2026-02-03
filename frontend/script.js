function uploadAudio() {
  const fileInput = document.getElementById("audioFile");
  const file = fileInput.files[0];

  if (!file) {
    alert("Upload MP3 file");
    return;
  }

  document.getElementById("loader").classList.remove("hidden");
  document.getElementById("result").innerHTML = "";

  // 🔴 IMPORTANT: FormData use karo (base64 ❌)
  const formData = new FormData();
  formData.append("audio", file); // 🔴 key name MUST be "audio"

  fetch("https://voice-ai-detector-j0dx.onrender.com/detect-voice", {
    method: "POST",
    headers: {
      "x-api-key": "MY_SECRET_KEY"
      // ❌ Content-Type mat likho
      // ❌ Authorization / Bearer mat bhejo
    },
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("result").innerHTML =
        `Result: <b>${data.result}</b><br>
         Confidence: ${data.confidence}<br>
         Explanation: ${data.explanation}`;
    })
    .catch(err => {
      console.error(err);
      document.getElementById("result").innerHTML =
        `<span style="color:red">Error occurred</span>`;
    })
    .finally(() => {
      document.getElementById("loader").classList.add("hidden");
    });
}

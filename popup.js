document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get(["snippetText", "imageUrl", "croppedImage"], async (data) => {
    // Paste text from right-click snippet
    if (data.snippetText) {
      document.getElementById("text-input").value = data.snippetText;
      chrome.storage.local.remove("snippetText");
    }

    // Process right-clicked image
    if (data.imageUrl) {
      try {
        const imageBlob = await fetch(data.imageUrl).then(res => res.blob());
        const reader = new FileReader();
        reader.onloadend = async () => {
          const base64Img = reader.result.split(",")[1];

          const res = await fetch("http://localhost:5000/analyze-image", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: base64Img }),
          });
          const result = await res.json();
          chrome.storage.local.remove("imageUrl");

          if (result.error) return alert("Image analysis failed.");

          document.getElementById("text-input").value = result.ocr_text;
          document.getElementById("summary-output").innerText = result.summary;
          document.getElementById("sentiment-output").innerText =
            `${result.sentiment.overall_sentiment} ${result.sentiment.emoji}`;

          const wcRes = await fetch("http://localhost:5000/wordcloud", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: result.ocr_text }),
          });
          const wcData = await wcRes.json();
          document.getElementById("wordcloud-output").src = `data:image/png;base64,${wcData.image}`;
        };
        reader.readAsDataURL(imageBlob);
      } catch (e) {
        alert("Failed to load image from URL");
      }
    }

    // Process cropped screenshot
    if (data.croppedImage) {
      const base64Img = data.croppedImage.split(",")[1];

      const res = await fetch("http://localhost:5000/analyze-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64Img }),
      });

      const result = await res.json();
      chrome.storage.local.remove("croppedImage");

      if (result.error) return alert("Image analysis failed.");

      document.getElementById("text-input").value = result.ocr_text;
      document.getElementById("summary-output").innerText = result.summary;
      document.getElementById("sentiment-output").innerText =
        `${result.sentiment.overall_sentiment} ${result.sentiment.emoji}`;

      const wcRes = await fetch("http://localhost:5000/wordcloud", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: result.ocr_text }),
      });
      const wcData = await wcRes.json();
      document.getElementById("wordcloud-output").src = `data:image/png;base64,${wcData.image}`;
    }
  });
});

document.getElementById("capture-snippet").addEventListener("click", async () => {
  // Inject the content script that lets user drag-select an area to capture
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      files: ["contentScript.js"]
    });
  });
});


// Analyze plain text
document.getElementById("analyze-text").addEventListener("click", async () => {
  const inputText = document.getElementById("text-input").value.trim();
  if (!inputText) return alert("Paste some text first!");

  const [summaryRes, sentimentRes, wcRes] = await Promise.all([
    fetch("http://localhost:5000/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: inputText }),
    }),
    fetch("http://localhost:5000/sentiment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: inputText }),
    }),
    fetch("http://localhost:5000/wordcloud", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: inputText }),
    })
  ]);

  const summaryData = await summaryRes.json();
  const sentimentData = await sentimentRes.json();
  const wcData = await wcRes.json();

  document.getElementById("summary-output").innerText = summaryData.summary || "Error";
  document.getElementById("sentiment-output").innerText =
    `${sentimentData.overall_sentiment} ${sentimentData.emoji}`;
  document.getElementById("wordcloud-output").src = `data:image/png;base64,${wcData.image}`;
});

// OCR + Summary + Sentiment from Image
document.getElementById("analyze-image").addEventListener("click", () => {
  document.getElementById("image-file").click();
});

document.getElementById("image-file").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async () => {
    const base64Img = reader.result.split(",")[1];

    const res = await fetch("http://localhost:5000/analyze-image", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: base64Img }),
    });
    const data = await res.json();

    if (data.error) return alert("Image analysis failed.");

    document.getElementById("text-input").value = data.ocr_text;
    document.getElementById("summary-output").innerText = data.summary;
    document.getElementById("sentiment-output").innerText =
      `${data.sentiment.overall_sentiment} ${data.sentiment.emoji}`;

    const wcRes = await fetch("http://localhost:5000/wordcloud", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: data.ocr_text }),
    });
    const wcData = await wcRes.json();
    document.getElementById("wordcloud-output").src = `data:image/png;base64,${wcData.image}`;
  };

  reader.readAsDataURL(file);
});

// Analyze article URL
document.getElementById("analyze-url").addEventListener("click", async () => {
  const url = document.getElementById("url-input").value.trim();
  if (!url) return alert("Paste a URL first!");

  const res = await fetch("http://localhost:5000/analyze-url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  const data = await res.json();

  if (data.error) return alert("URL analysis failed.");

  document.getElementById("text-input").value = data.content;
  document.getElementById("summary-output").innerText = data.summary;
  document.getElementById("sentiment-output").innerText =
    `${data.sentiment.overall_sentiment} ${data.sentiment.emoji}`;
  document.getElementById("wordcloud-output").src = `data:image/png;base64,${data.wordcloud}`;
});

// Analyze YouTube video
document.getElementById("analyze-youtube").addEventListener("click", async () => {
  const ytUrl = document.getElementById("yt-url").value.trim();
  if (!ytUrl) return alert("Paste a YouTube link!");

  const res = await fetch("http://localhost:5000/analyze-youtube", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: ytUrl }),
  });
  const data = await res.json();

  if (data.error) return alert("Video analysis failed.");

  document.getElementById("text-input").value = data.transcript;
  document.getElementById("summary-output").innerText = data.summary;
  document.getElementById("sentiment-output").innerText =
    `${data.sentiment.overall_sentiment} ${data.sentiment.emoji}`;
  document.getElementById("wordcloud-output").src = `data:image/png;base64,${data.wordcloud}`;
});

// Generate WordCloud only
document.getElementById("generate-wordcloud").addEventListener("click", async () => {
  const text = document.getElementById("text-input").value;
  if (!text.trim()) return alert("Paste some text first!");

  const res = await fetch("http://localhost:5000/wordcloud", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  const data = await res.json();
  document.getElementById("wordcloud-output").src = `data:image/png;base64,${data.image}`;
});

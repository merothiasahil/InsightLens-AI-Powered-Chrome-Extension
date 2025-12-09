chrome.runtime.onInstalled.addListener(() => {
    // Context menu for selected text
    chrome.contextMenus.create({
      id: "insightlens-snippet",
      title: "Analyze Text with InsightLens",
      contexts: ["selection"]
    });
  
    // Context menu for right-clicked images
    chrome.contextMenus.create({
      id: "insightlens-image",
      title: "Analyze Image with InsightLens",
      contexts: ["image"]
    });
  });
  
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "insightlens-snippet") {
      const selectedText = info.selectionText;
      chrome.storage.local.set({ snippetText: selectedText }, () => {
        chrome.action.openPopup();
      });
    }
  
    if (info.menuItemId === "insightlens-image") {
      const imageUrl = info.srcUrl;
      chrome.storage.local.set({ imageUrl: imageUrl }, () => {
        chrome.action.openPopup(); // popup.html reads and processes this
      });
    }
  });
  
  // Handle cropped screenshot from custom snipping overlay
  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "captureCrop") {
      chrome.tabs.captureVisibleTab(null, { format: "png" }, async (dataUrl) => {
        try {
          const base64 = dataUrl.split(",")[1];
          const binary = atob(base64);
          const bytes = new Uint8Array(binary.length);
          for (let i = 0; i < binary.length; i++) {
            bytes[i] = binary.charCodeAt(i);
          }
          const blob = new Blob([bytes], { type: "image/png" });
          const bitmap = await createImageBitmap(blob);
  
          const canvas = new OffscreenCanvas(msg.area.width, msg.area.height);
          const ctx = canvas.getContext("2d");
  
          ctx.drawImage(
            bitmap,
            msg.area.x, msg.area.y,
            msg.area.width, msg.area.height,
            0, 0,
            msg.area.width, msg.area.height
          );
  
          const blobOut = await canvas.convertToBlob();
          const reader = new FileReader();
          reader.onloadend = () => {
            const croppedDataUrl = reader.result;
            chrome.storage.local.set({ croppedImage: croppedDataUrl }, () => {
              chrome.windows.create({
                url: chrome.runtime.getURL("popup.html"),
                type: "popup",
                width: 400,
                height: 650
              });
            });
          };
          reader.readAsDataURL(blobOut);
        } catch (err) {
          console.error("Cropping failed:", err);
        }
      });
    }
  });
  
  
  
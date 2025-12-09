(function () {
    if (document.getElementById("insightlens-snipper")) return;
  
    const overlay = document.createElement("div");
    overlay.id = "insightlens-snipper";
    overlay.style.position = "fixed";
    overlay.style.top = 0;
    overlay.style.left = 0;
    overlay.style.width = "100vw";
    overlay.style.height = "100vh";
    overlay.style.zIndex = 999999;
    overlay.style.cursor = "crosshair";
    overlay.style.background = "rgba(0, 0, 0, 0.2)";
    document.body.appendChild(overlay);
  
    let startX, startY, endX, endY;
    const selection = document.createElement("div");
    selection.style.position = "absolute";
    selection.style.border = "2px dashed red";
    selection.style.background = "rgba(255,255,255,0.2)";
    overlay.appendChild(selection);
  
    overlay.addEventListener("mousedown", (e) => {
      startX = e.clientX;
      startY = e.clientY;
  
      const onMouseMove = (e) => {
        endX = e.clientX;
        endY = e.clientY;
  
        selection.style.left = `${Math.min(startX, endX)}px`;
        selection.style.top = `${Math.min(startY, endY)}px`;
        selection.style.width = `${Math.abs(endX - startX)}px`;
        selection.style.height = `${Math.abs(endY - startY)}px`;
      };
  
      const onMouseUp = () => {
        overlay.removeEventListener("mousemove", onMouseMove);
        overlay.removeEventListener("mouseup", onMouseUp);
        document.body.removeChild(overlay);
  
        const cropArea = {
          x: Math.min(startX, endX),
          y: Math.min(startY, endY),
          width: Math.abs(endX - startX),
          height: Math.abs(endY - startY)
        };
  
        chrome.runtime.sendMessage({ action: "captureCrop", area: cropArea });
      };
  
      overlay.addEventListener("mousemove", onMouseMove);
      overlay.addEventListener("mouseup", onMouseUp);
    });
  })();
  
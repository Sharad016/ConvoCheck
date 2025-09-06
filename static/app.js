async function analyze() {
  const text = document.getElementById("threadInput").value;

  const res = await fetch("/analyze", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ 
      thread_text: text, 
      comments: text.split("\n") // one comment per line 
    })
  });

  const data = await res.json();

  // Show Gemini summary
  document.getElementById("summary").textContent = data.analysis;

  // Show flagged comments with colors
  const flaggedDiv = document.getElementById("flaggedComments");
  flaggedDiv.innerHTML = "";

  data.flagged.forEach(item => {
    const p = document.createElement("p");
    p.textContent = item.comment;
    if (item.toxic) {
      p.style.color = "red";     // toxic → red
      p.style.fontWeight = "bold";
    } else {
      p.style.color = "black";   // safe → black
    }
    flaggedDiv.appendChild(p);
  });
}

from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from better_profanity import profanity

# Initialize Flask
app = Flask(__name__)

# 🔹 Configure Gemini API (replace with your key)
genai.configure(api_key="AIzaSyBzIsKbV3EURx5Un7fSmEeiM_uMqdd6p84")

# 🔹 Load profanity filter
profanity.load_censor_words()

@app.route("/")
def home():
    # Serve frontend
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    thread_text = data.get("thread_text", "")
    comments = data.get("comments", [])

    # Step 1: Local toxicity detection
    flagged_comments = []
    for comment in comments:
        if profanity.contains_profanity(comment):
            flagged_comments.append({"comment": comment, "toxic": True})
        else:
            flagged_comments.append({"comment": comment, "toxic": False})

    # Step 2: If everything toxic → skip Gemini
    if all(c["toxic"] for c in flagged_comments):
        return jsonify({
            "analysis": "⚠️ All comments flagged as toxic. Gemini not used.",
            "flagged": flagged_comments
        })

    # Step 3: Forward safe/mixed input to Gemini
    prompt = f"""
    Analyze this discussion thread:
    Thread: {thread_text}
    Comments: {comments}
    
    Provide:
    1. Summary (2–3 sentences)
    2. Sentiment (positive/negative/neutral)
    3. Highlight which comments may be toxic.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return jsonify({
        "analysis": response.text,
        "flagged": flagged_comments
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

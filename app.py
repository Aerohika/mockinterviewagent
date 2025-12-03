from flask import Flask, request, jsonify
import whisper
import tempfile
import os

app = Flask(__name__)

model = whisper.load_model("small")

@app.route("/", methods=["GET"])
def home():
    return "Interview Practice API is running!"

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        audio_file.save(temp.name)
        temp_path = temp.name

    try:
        result = model.transcribe(temp_path)
        text = result.get("text", "")

        return jsonify({
            "transcription": text
        })

    finally:
        os.remove(temp_path)

@app.route("/evaluate", methods=["POST"])
def evaluate_answer():
    data = request.json
    answer = data.get("answer", "")

    # TODO: add your evaluation logic here
    return jsonify({
        "evaluation": f"Your answer length is {len(answer)} characters."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

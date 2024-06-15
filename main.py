import logging
from flask import Flask, request, jsonify
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
import librosa

app = Flask(__name__)

# Load the model and processor from local files

# if local
# model_path = "./model/openai-whisper-base-en"
# model = WhisperForConditionalGeneration.from_pretrained(model_path)
# processor = WhisperProcessor.from_pretrained(model_path)

model_name = "openai/whisper-base.en"
model = WhisperForConditionalGeneration.from_pretrained(model_name)
processor = WhisperProcessor.from_pretrained(model_name)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        # Check if an audio file is included in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

        # Load the audio file
        audio, rate = librosa.load(file, sr=16000)

        # Process the audio file
        input_values = processor(audio, return_tensors="pt").input_features

        # Perform the transcription
        predicted_ids = model.generate(input_values)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        return jsonify({"transcription": transcription})
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
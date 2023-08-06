import io, os
import gherkan.utils.constants as c

### Here add the path to your generated json and project id (see gitlab wiki)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/gabi/factorio-nlptask/My First Project-f71f3f9fdb6b.json"
AUDIO_PATH = os.path.join(c.GHERKAN_ROOT_DIR, "data/audio", "cz_test.wav")
LANG = "cs-CZ"

def transcribe_file_with_auto_punctuation(path, lang):
    """Transcribe the given audio file with auto punctuation enabled."""
    # [START speech_transcribe_auto_punctuation]
    from google.cloud import speech
    client = speech.SpeechClient()

    # path = 'resources/commercial_mono.wav'
    with io.open(path, 'rb') as audio_file:
        content = audio_file.read()
    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=22050,
        language_code=lang,
        # Enable automatic punctuation
        enable_automatic_punctuation=True)
    response = client.recognize(config, audio)
    for i, result in enumerate(response.results):
        for j in range(len(result.alternatives)):
            alternative = result.alternatives[j]
            print('-' * 20)
            print('First alternative of result {}'.format(i))
            print('Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    transcribe_file_with_auto_punctuation(AUDIO_PATH, LANG)

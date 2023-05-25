import sounddevice as sd
import soundfile as sf

def record_audio(duration, output_file):
    # Set the sample rate and number of channels for recording
    sample_rate = 44100  # CD quality audio
    channels = 2  # Stereo audio

    # Start recording audio
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)

    print("Recording audio...")
    sd.wait()  # Wait until recording is finished

    # Save the recorded audio to a file
    sf.write(output_file, recording, sample_rate)

    print(f"Audio saved to: {output_file}")

# Example usage
duration = 5  # Recording duration in seconds
output_file = "Local_Storage/Audio/recorded_audio.wav"  # Output file name

record_audio(duration, output_file)

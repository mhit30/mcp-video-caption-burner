import os
from dotenv import load_dotenv
import ffmpeg
from openai import OpenAI

load_dotenv()


class VideoCaption:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def dec_to_time(self, s):
        return f"{int((s//3600)):02}:{int((s//60)):02}:{int(s):02},{int((s%1)*1000):03}"

    def extract_audio(self, video_file_path):
        if not video_file_path:
            return Exception("Video file must be provided.")
        my_input = ffmpeg.input(video_file_path)
        my_input_audio_stream = ffmpeg.output(my_input, "./videos/audio.mp3")
        ffmpeg.run(my_input_audio_stream)

    def transcribe_audio(self, audio_file_path):
        if not audio_file_path:
            return Exception("Audio file must be provided.")
        audio_file = open(audio_file_path, "rb")
        transcript = self.client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )

        with open("./videos/transcript.srt", "w") as file_object:
            my_str = ""
            i = 1
            for chunk in transcript.segments:
                text = chunk.text
                start = chunk.start
                end = chunk.end
                print(start, end)
                my_str += (
                    f"{i}"
                    + "\n"
                    + self.dec_to_time(start)
                    + "  -->  "
                    + self.dec_to_time(end)
                    + "\n"
                    + text
                    + "\n \n \n"
                )
                i += 1
            file_object.write(my_str)

    def burn_caption(self, subtitles_file_path, video_file_path):
        if not subtitles_file_path:
            return Exception("Subtitle file must be provided.")
        if not video_file_path:
            return Exception("Video file must be provided.")

        my_input = ffmpeg.input(video_file_path)
        video = my_input.video.filter("subtitles", subtitles_file_path)
        audio = my_input.audio
        stream = ffmpeg.output(video, audio, "./videos/captioned_output.mov")
        ffmpeg.run(stream)

from mcp.server.fastmcp import FastMCP
from ffmpeg_client import VideoCaption

# Create an MCP server
mcp = FastMCP("MCP Video Editor")

video_captioner = VideoCaption()


@mcp.tool()
def extract_audio(video_file_path: str) -> str:
    """
    Extracts the audio track from a given video file.
    Input: Path to a video file
    Returns: Path to a
    """
    video_captioner.extract_audio(video_file_path)
    return "./videos/audio.mp3"


@mcp.tool()
def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribes the audio into text.
    Input: Path to an audio file
    Output: Path to a srt caption file.
    """
    video_captioner.transcribe_audio(audio_file_path)
    return "./videos/transcript.srt"


@mcp.tool()
def burn_captions(srt_file_path: str, video_file_path: str) -> str:
    """
    Burns the srt caption file into the video file.
    Inputs: 1. Path to an srt file, 2. Path to a video file
    Output: Path to a captioned video file.
    """
    video_captioner.burn_caption(srt_file_path, video_file_path)
    return "./videos/captioned_output.mov"


if __name__ == "__main__":
    mcp.run()

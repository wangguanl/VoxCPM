"""Test mp3 reference-audio cloning after the ffmpeg fix."""
import sys
from gradio_client import Client, handle_file

URL = "http://localhost:8808/"
REF_MP3 = r"E:\AI\local-voice\VoxCPM\outputs\test_ref.mp3"  # 440Hz sine wave, valid mp3

client = Client(URL, verbose=False)
result = client.predict(
    "这是一段用于验证 mp3 参考音频解码的语音克隆测试。",
    "",                      # control_instruction
    handle_file(REF_MP3),    # ref_wav (mp3)
    False,                   # use_prompt_text
    "",                      # prompt_text_value
    2.0,                     # cfg_value
    True,                    # do_normalize
    False,                   # denoise
    10,                      # dit_steps
    42,                      # seed_value
    api_name="/generate",
)
print("Result:", result)
audio_path, seed = result[0], result[1]
import shutil, os
out = r"E:\AI\local-voice\VoxCPM\outputs\clone_test.wav"
shutil.copyfile(audio_path, out)
print(f"SUCCESS: saved {out} ({os.path.getsize(out)} bytes), seed={seed}")
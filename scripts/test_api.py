"""Test the running VoxCPM Gradio web demo end-to-end via its API."""
import sys
import time
import numpy as np
import soundfile as sf
from gradio_client import Client, handle_file

URL = "http://localhost:8808/"
OUT = r"E:\AI\local-voice\VoxCPM\outputs\api_test.wav"

client = Client(URL, verbose=False)

# Inspect the API to find the generate endpoint and its parameter names
api = client.view_api(return_format="dict")
print("=== API endpoints ===")
for fn_name, fn_info in api.get("named_endpoints", {}).items():
    params = [p["parameter_name"] for p in fn_info["parameters"]]
    print(f"{fn_name}({', '.join(params)})")

# Find the main generate function (the one with `text` param)
gen_name = "/generate"
print(f"\nUsing endpoint: {gen_name}")

# Build args positionally per the UI order: text, control_instruction, ref_wav,
# use_prompt_text, prompt_text_value, cfg_value, do_normalize, denoise, dit_steps, seed
result = client.predict(
    "欢迎使用 VoxCPM2，这是一段中文语音合成测试。",
    "",                       # control_instruction
    None,                     # ref_wav
    False,                    # use_prompt_text
    "",                       # prompt_text_value
    2.0,                      # cfg_value
    True,                     # do_normalize
    False,                    # denoise
    10,                       # dit_steps
    42,                       # seed
    api_name="/generate",
)

print(f"\nResult type: {type(result)}")
print(f"Result: {result}")

# Result is (audio_filepath, seed_used)
if isinstance(result, (list, tuple)) and len(result) >= 2:
    audio_path, seed_used = result[0], result[1]
    import shutil
    shutil.copyfile(audio_path, OUT)
    import os
    print(f"Saved -> {OUT}  ({os.path.getsize(OUT)} bytes)  seed={seed_used}")
else:
    print("Unexpected result format")

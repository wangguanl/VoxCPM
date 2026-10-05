import os

os.environ["MODELSCOPE_CACHE"] = r"E:\huggingface_cache\modelscope"

import torch
import soundfile as sf
from voxcpm import VoxCPM

print("Loading VoxCPM2 from local path...")
model = VoxCPM.from_pretrained(
    r"E:\huggingface_cache\modelscope\models\OpenBMB\VoxCPM2",
    load_denoiser=False,
    optimize=False,
    device="cuda",
)
print("Model loaded. Generating speech...")
wav = model.generate(
    text="欢迎使用 VoxCPM2，这是一段中文语音合成测试。",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
out = r"E:\AI\local-voice\VoxCPM\examples\test_output.wav"
sf.write(out, wav, model.tts_model.sample_rate)
print(f"Saved: {out}, sample_rate={model.tts_model.sample_rate}, duration={len(wav)/model.tts_model.sample_rate:.2f}s")
print("SUCCESS")

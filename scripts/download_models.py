import os

os.environ["MODELSCOPE_CACHE"] = r"E:\huggingface_cache\modelscope"

from modelscope import snapshot_download

print("=== Downloading OpenBMB/VoxCPM2 from ModelScope ===")
voxcpm_path = snapshot_download("OpenBMB/VoxCPM2")
print(f"VoxCPM2 -> {voxcpm_path}")

print("=== Downloading iic/SenseVoiceSmall from ModelScope ===")
asr_path = snapshot_download("iic/SenseVoiceSmall")
print(f"SenseVoiceSmall -> {asr_path}")

print("=== Downloading iic/speech_zipenhancer_ans_multiloss_16k_base from ModelScope ===")
denoiser_path = snapshot_download("iic/speech_zipenhancer_ans_multiloss_16k_base")
print(f"ZipEnhancer -> {denoiser_path}")

print("ALL DOWNLOADS COMPLETE")

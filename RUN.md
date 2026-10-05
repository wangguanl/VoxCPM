# 运行命令

- 项目：VoxCPM（OpenBMB）
- 生成时间：2026-09-09
- 运行方式：直接运行（`uv` / `.venv` + `app.py`）
- 硬件评估：**满足**（VoxCPM2 官方约 8GB；空卡 16GB 可跑）

## 环境准备

```powershell
$env:Path = "E:\Programs\ffmpeg-master-latest-win64-gpl\bin;" + $env:Path
$env:HF_ENDPOINT = "https://hf-mirror.com"
cd E:\AI\local-voice\VoxCPM
# 已有 .venv（torch CUDA + voxcpm）；若重建：
# uv sync --default-index "https://pypi.tuna.tsinghua.edu.cn/simple"
```

模型优先本地：`E:\huggingface_cache\modelscope\models\OpenBMB\VoxCPM2`。

## 启动

- 推荐：`pwsh -NoProfile -File .\start.ps1`
- 说明：单服务 webui；端口起点 8808，占用则顺延
- 等价手动命令：

```powershell
.\.venv\Scripts\python.exe -u .\app.py --model-id E:\huggingface_cache\modelscope\models\OpenBMB\VoxCPM2 --port 8808 --device auto
```

## 验证

- 浏览器打开提示地址，完成一次合成
- `nvidia-smi` 峰值约 8GB 量级

## 备注

- 镜像：HF=`hf-mirror.com`；PyPI 可用清华
- 旧脚本 `start_voxcpm.ps1` 仍可用；日常请用 `start.ps1`
- 本次未长时间启动 GPU 服务

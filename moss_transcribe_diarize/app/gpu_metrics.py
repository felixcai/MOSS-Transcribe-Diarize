from __future__ import annotations

from typing import Any


def read_gpu_metrics() -> dict[str, Any]:
    """读取 NVIDIA GPU 指标；不支持 NVML 时安全返回不可用状态。"""
    try:
        import pynvml
    except Exception:
        return {"available": False, "devices": []}

    initialized = False
    try:
        pynvml.nvmlInit()
        initialized = True
        devices = []
        for index in range(pynvml.nvmlDeviceGetCount()):
            handle = pynvml.nvmlDeviceGetHandleByIndex(index)
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode("utf-8", errors="replace")
            devices.append(
                {
                    "index": index,
                    "name": str(name),
                    "utilization_percent": int(utilization.gpu),
                    "memory_used_bytes": int(memory.used),
                    "memory_total_bytes": int(memory.total),
                }
            )
        return {"available": bool(devices), "devices": devices}
    except Exception:
        # Windows 核显、缺少 NVIDIA 驱动或 NVML 初始化失败时，不影响主服务。
        return {"available": False, "devices": []}
    finally:
        if initialized:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                pass

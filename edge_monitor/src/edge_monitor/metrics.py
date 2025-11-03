import psutil
from .logger_config import set_logging

try:
    from nvidia_smi import nvidia_smi
    nvsmi = nvidia_smi.getInstance()
except ImportError:
    nvsmi = None

logger = set_logging("metrics")

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    mem = psutil.virtual_memory()
    return {"total": mem.total, "used": mem.used, "percent": mem.percent}

def get_disk_usage():
    disk = psutil.disk_usage("/")
    return {"total": disk.total, "used": disk.used, "percent": disk.percent}

def get_boot_time():
    time = psutil.boot_time()
    return time

    


def get_gpu_usage():
    if not nvsmi:
        return None
    gpu_info = nvsmi.DeviceQuery("memory.used, utilization.gpu")
    return gpu_info


def get_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        
        # On many systems, 'coretemp' or 'cpu-thermal' is used
        for name, entries in temps.items():
            for entry in entries:
                if entry.current:
                    return round(entry.current, 1)
    except Exception as e:
        logger.warning(f"Temperature read error: {e}")
        return None
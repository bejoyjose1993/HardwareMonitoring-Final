import asyncio
from .metrics import get_cpu_usage, get_ram_usage, get_disk_usage, get_gpu_usage, get_temperature, get_boot_time
from .transport import file_transfer, http_transfer
from .transport.mqtt_transfer import MQTTPublisher
import os
from .logger_config import set_logging

from .utils import (
    print_metrics,
    register_signal_handlers,
    shutdown_event, 
    log_to_file,
    bytes_to_mb,
    bytes_to_gb,
    current_timestamp,
    get_system_running_time
)

logger = set_logging("EdgeMonitor")

class EdgeMonitor:
    def __init__(self, transport="http", interval=5, endpoint=None, broker=None, port=None):
        self.transport = transport or os.getenv("TRANSPORT", "mqtt")
        self.interval = interval or int(os.getenv("INTERVAL", 5))
        self.endpoint = endpoint or os.getenv("ENDPOINT")
        self.broker = broker or os.getenv("BROKER")
        self.port = port or int(os.getenv("PORT", 1883))
        self.mqtt_client = None

        logger.info(f"Initialized EdgeMonitor with transport={self.transport}, endpoint={self.endpoint}, interval={self.interval}")
        # if self.transport == "mqtt" and broker and port:
        #     self.mqtt_client = MQTTPublisher(broker, port, "edge/metrics")

        if self.transport == "http" and endpoint:
            self.http_endpoint = endpoint
            
    async def run(self, shutdown_event: asyncio.Event):
        logger.info("EdgeMonitor started...")
        while not shutdown_event.is_set():
            try:
                cpu = get_cpu_usage()
                ram = get_ram_usage()
                disk = get_disk_usage()
                gpu = get_gpu_usage()
                boot_time = get_system_running_time()
                

                temperature_celsius = get_temperature()

                data = {
                    "timestamp": current_timestamp(),
                    "total_system_runtime": boot_time,
                    "cpu_percent": cpu,
                    "ram": {"total_mb": bytes_to_mb(ram["total"]),
                            "used_mb": bytes_to_mb(ram["used"]),
                            "percent": ram["percent"]},
                    "disk": {"total_gb": bytes_to_gb(disk["total"]),
                            "used_gb": bytes_to_gb(disk["used"]),
                            "percent": disk["percent"]},
                    "gpu": gpu,
                    "temperature_celsius": temperature_celsius
                }

                logger.info(f"[INFO] System Boot Time {boot_time}")
                if self.transport == "file":
                    file_transfer.send(data)
                elif self.transport == "http":
                    try:
                        await http_transfer.send(self.endpoint, data)
                        logger.info(f"[INFO] Sent metrics successfully to {self.endpoint}")
                    except Exception as e:
                        logger.exception(f"[ERROR] HTTP send failed: {e}")

                await asyncio.sleep(self.interval)

            except asyncio.CancelledError as e:
                logger.exception(f"Error in EdgeMonitor loop: {e}")
                break

        logger.info("EdgeMonitor stopped.")
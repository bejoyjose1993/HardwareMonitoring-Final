import aiohttp
from ..logger_config import set_logging

logger = set_logging("http_transfer")

async def send(endpoint: str, data: dict):
    """
    Send metrics to an HTTP endpoint asynchronously.
    """
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(endpoint, json=data) as response:
                if response.status == 200:
                    logger.info(f"Successfully sent data to {endpoint}")
                else:
                    logger.warning(f"HTTP {response.status} when sending to {endpoint}")
        except Exception as e:
            logger.exception(f"HTTP send failed: {e}")
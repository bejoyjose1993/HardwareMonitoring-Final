# run_all.py
import asyncio
import os
from edge_monitor.edge_monitor import EdgeMonitor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import signal
from edge_monitor.logger_config import set_logging

logger = set_logging("run_all")

metrics_store = {}

# FastAPI server
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ingest")
async def ingest(data: dict):
    metrics_store.update(data)
    logger.info(f"Metrics received: {data}")
    return {"status": "ok"}

@app.get("/metrics")
async def get_metrics():
    return metrics_store

async def run_edge_monitor(shutdown_event: asyncio.Event):
    # 🔹 Read from environment variables (with defaults)
    transport = os.getenv("TRANSPORT", "http")
    endpoint = os.getenv("ENDPOINT", "http://localhost:8000/ingest")
    interval = int(os.getenv("INTERVAL", "5"))

    logger.info(f"Transport={transport}, Endpoint={endpoint}, Interval={interval}s")

    monitor = EdgeMonitor(transport=transport, endpoint=endpoint, interval=interval)
    await monitor.run(shutdown_event)

async def run_server(shutdown_event: asyncio.Event):
    port = int(os.getenv("SERVER_PORT", "8000"))
    
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    server_task = asyncio.create_task(server.serve())

    # Wait for shutdown
    await shutdown_event.wait()
    server.should_exit = True
    await server_task

async def main():
    shutdown_event = asyncio.Event()

    # Ctrl+C handler
    def stop_app(sig, frame):
        
        logger.info("Exiting...")
        shutdown_event.set()

    signal.signal(signal.SIGINT, stop_app)
    signal.signal(signal.SIGTERM, stop_app)

    # Run both tasks concurrently
    await asyncio.gather(
        run_server(shutdown_event),
        run_edge_monitor(shutdown_event)
    )

if __name__ == "__main__":
    asyncio.run(main())

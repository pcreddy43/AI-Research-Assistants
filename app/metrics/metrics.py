from prometheus_client import Counter, Histogram, Gauge, start_http_server
import psutil
import threading
import time

# Example metric: count agent requests
AGENT_REQUESTS = Counter("agent_requests_total", "Total requests handled by agents")
LLM_TIME = Histogram("llm_duration_seconds", "Time spent in LLM calls")
RAG_TIME = Histogram("rag_duration_seconds", "Time spent in RAG calls")
WEB_SEARCH_TIME = Histogram("web_search_duration_seconds", "Time spent in web_search calls")
CPU_USAGE = Gauge("cpu_usage_percent", "CPU usage percent")
MEMORY_USAGE = Gauge("memory_usage_mb", "Memory usage in MB")

# Monitor CPU and memory in a background thread
def monitor_system_metrics():
    while True:
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(psutil.virtual_memory().used / 1024 / 1024)
        time.sleep(5)

def start_metrics_server(port: int = 8002):
    start_http_server(port)
    print(f"Prometheus metrics server started on port {port}")
    threading.Thread(target=monitor_system_metrics, daemon=True).start()

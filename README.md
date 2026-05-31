# Distributed Linux Fleet Management

A bare-metal, low-latency observability stack designed for distributed Linux environments, featuring custom kernel-level telemetry and hardware-accelerated GPU monitoring. 

This project was developed for the **Zoho** program, focusing on high-performance infrastructure monitoring without relying on heavy, high-level abstractions.

## Architecture Highlights
* **Zero-Abstraction CPU/RAM Scraping:** Features a custom Python daemon (`agent.py`) that performs direct, memory-mapped reads of the `/proc` and `/sys` filesystems. It calculates CPU tick deltas and tracks network I/O drops directly from the kernel, bypassing heavy libraries like `psutil`.
* **Hardware Acceleration:** Native integration with the NVIDIA Container Toolkit to monitor Quadro RTX 5000 compute utilization and VRAM allocation via Docker.
* **Time-Series Pipeline:** Prometheus configured for high-resolution (1s) scraping to capture micro-bursts in system activity, visualized through a unified Grafana NOC dashboard.

## Infrastructure Stack
* **Agent:** Custom Python 3 (Kernel scraping)
* **Metrics & Storage:** Prometheus, Node Exporter, NVIDIA GPU Exporter
* **Visualization:** Grafana
* **Deployment:** Docker Compose

## Quick Start
```bash
# 1. Launch the custom kernel scraping daemon
python3 agent.py &

# 2. Spin up the distributed monitoring stack
sudo docker-compose up -d
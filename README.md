# Distributed Linux Fleet Management System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)

A bare-metal, low-latency observability stack designed for distributed Linux environments, featuring custom kernel-level telemetry and hardware-accelerated GPU monitoring. 

This architecture abandons heavy, high-level abstractions in favor of direct system reads, providing the microsecond-level precision required for High-Performance Computing (HPC) and quantitative finance workloads.

---

## Core Architecture & Highlights

Standard infrastructure monitoring tools often rely on bloated libraries (like `psutil`) that add unnecessary overhead. This project takes a **zero-abstraction** approach:

*  **Zero-Abstraction Telemetry:** A custom Python daemon (`agent.py`) performs direct, memory-mapped reads of the `/proc` and `/sys` virtual filesystems. It calculates CPU tick deltas and tracks network I/O drops natively from the Linux kernel.
*  **HFT-Grade Resolution:** Prometheus is configured with a hardcore **1-second scrape interval**, designed to capture micro-bursts in system activity that standard 15s/30s pollers miss.
*  **Hardware Acceleration:** Native integration with the NVIDIA Container Toolkit to monitor host-level Quadro RTX 5000 compute utilization, power draw, and VRAM allocation from within the containerized stack.
*  **NOC-Style Dashboarding:** A centralized Grafana Network Operations Center (NOC) dashboard providing real-time visualization of the fleet's data plane.

---

##  Tech Stack
* **Agent:** Custom Python 3 (Kernel `/proc` & `/sys` scraping)
* **Metrics Storage:** Prometheus (Time-Series DB)
* **Exporters:** Node Exporter, NVIDIA GPU Exporter (`utkuozdemir/nvidia_gpu_exporter`)
* **Visualization:** Grafana
* **Orchestration:** Docker Compose

---

##  Quick Start

Ensure you have Docker, Docker Compose, and the NVIDIA Container Toolkit installed on your host Linux machine.

**1. Clone the repository**
```bash
git clone [https://github.com/manmathbh/distributed-linux-fleet-management.git](https://github.com/manmathbh/distributed-linux-fleet-management.git)
cd distributed-linux-fleet-management
```

**2. Launch the bare-metal kernel scraping daemon**

```Bash
# Starts the custom Python agent on port 8000
python3 agent.py &
```

**3. Spin up the distributed monitoring stack**

```Bash
sudo docker-compose up -d
```

**4. Access the Dashboards**

Grafana: http://localhost:3030 (Default login: admin / admin)

Prometheus: http://localhost:9090

---

### Dashboard Telemetry (Live Previews)
Below are live captures of the Grafana NOC dashboard visualizing the real-time, zero-abstraction telemetry pulled directly from the Linux kernel and the host's Quadro RTX 5000 GPU.

**RTX 5000 Compute Utilization** <br>
**Custom Agent: Free Memory**<br>
**Custom Agent: CPU Utilization**<br>
**Custom Agent: Network Rx Bytes**

---

### Future Roadmap
**eBPF Integration:** Migrating from /proc scraping to Extended Berkeley Packet Filter (eBPF) for sandboxed, kernel-level event tracing.

**Alertmanager Pipeline:** Configuring Prometheus Alertmanager for automated incident response during thermal throttling or CPU saturation events.

**SSO Authentication:** Placing the Grafana instance behind an OAuth2 reverse proxy for secure, enterprise-grade access control.
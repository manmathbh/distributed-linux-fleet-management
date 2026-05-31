import time
import os
from prometheus_client import start_http_server, Gauge

# --- METRICS DEFINITIONS ---
CPU_USAGE = Gauge('node_custom_cpu_utilization_percent', 'CPU utilization percentage')
MEM_FREE = Gauge('node_custom_mem_free_bytes', 'Available memory in bytes')
MEM_TOTAL = Gauge('node_custom_mem_total_bytes', 'Total memory in bytes')
NET_RX = Gauge('node_custom_net_rx_bytes', 'Network bytes received', ['interface'])
NET_TX = Gauge('node_custom_net_tx_bytes', 'Network bytes transmitted', ['interface'])
NET_DROPS = Gauge('node_custom_net_drops', 'Network packets dropped', ['interface'])

class HFTNodeExporter:
    def __init__(self):
        self.prev_cpu_idle = 0
        self.prev_cpu_total = 0

    def get_cpu_utilization(self):
        """
        Parses /proc/stat to calculate CPU usage.
        Formula: (1 - (delta_idle / delta_total)) * 100
        """
        with open('/proc/stat', 'r') as f:
            line = f.readline() # Only the first line 'cpu'
        
        # Fields: user, nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice
        fields = [float(column) for column in line.split()[1:]]
        
        idle = fields[3] + fields[4] # idle + iowait
        total = sum(fields)
        
        # Calculate delta since last poll
        delta_idle = idle - self.prev_cpu_idle
        delta_total = total - self.prev_cpu_total
        
        self.prev_cpu_idle = idle
        self.prev_cpu_total = total
        
        if delta_total == 0:
            return 0.0
        
        return (1.0 - (delta_idle / delta_total)) * 100

    def get_memory_metrics(self):
        """Parses /proc/meminfo for precise memory tracking."""
        mem_info = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                parts = line.split(':')
                # Convert kB to bytes
                mem_info[parts[0]] = int(parts[1].split()[0]) * 1024
        
        MEM_TOTAL.set(mem_info.get('MemTotal', 0))
        MEM_FREE.set(mem_info.get('MemAvailable', 0))

    def get_network_metrics(self):
        """Parses /sys/class/net for interface-specific I/O."""
        base_path = '/sys/class/net/'
        interfaces = [d for d in os.listdir(base_path) if d != 'lo']
        
        for iface in interfaces:
            with open(f'{base_path}{iface}/statistics/rx_bytes', 'r') as f:
                NET_RX.labels(interface=iface).set(int(f.read().strip()))
            with open(f'{base_path}{iface}/statistics/tx_bytes', 'r') as f:
                NET_TX.labels(interface=iface).set(int(f.read().strip()))
            with open(f'{base_path}{iface}/statistics/rx_dropped', 'r') as f:
                NET_DROPS.labels(interface=iface).set(int(f.read().strip()))

    def run(self, interval=1):
        while True:
            try:
                CPU_USAGE.set(self.get_cpu_utilization())
                self.get_memory_metrics()
                self.get_network_metrics()
            except Exception as e:
                print(f"Error collecting metrics: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    # Start Prometheus HTTP server on port 8000
    start_http_server(8000)
    print("HFT Custom Agent listening on port 8000...")
    exporter = HFTNodeExporter()
    exporter.run()
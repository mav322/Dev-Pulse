from flask import Flask, jsonify, render_template
import psutil
import datetime
import platform
import logging

# ── Config ──────────────────────────────────────────────
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


# ── Routes ──────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/stats')
def get_stats():
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_cores   = psutil.cpu_percent(percpu=True)
        cpu_freq    = psutil.cpu_freq()
        mem         = psutil.virtual_memory()
        disk        = psutil.disk_usage('/')
        net         = psutil.net_io_counters()
        boot_time   = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime      = datetime.datetime.now() - boot_time

        # Top 5 processes by CPU
        processes = []
        for proc in sorted(
            psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
            key=lambda p: p.info.get('cpu_percent') or 0,
            reverse=True
        )[:5]:
            try:
                processes.append({
                    'pid':  proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu':  round(proc.info.get('cpu_percent') or 0, 1),
                    'mem':  round(proc.info.get('memory_percent') or 0, 1),
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return jsonify({
            'cpu': {
                'percent': cpu_percent,
                'cores':   cpu_cores,
                'count':   psutil.cpu_count(logical=True),
                'freq':    round(cpu_freq.current) if cpu_freq else 'N/A',
            },
            'memory': {
                'percent':      mem.percent,
                'used_gb':      round(mem.used      / (1024 ** 3), 2),
                'total_gb':     round(mem.total     / (1024 ** 3), 2),
                'available_gb': round(mem.available / (1024 ** 3), 2),
            },
            'disk': {
                'percent': disk.percent,
                'used_gb': round(disk.used  / (1024 ** 3), 1),
                'total_gb':round(disk.total / (1024 ** 3), 1),
                'free_gb': round(disk.free  / (1024 ** 3), 1),
            },
            'network': {
                'bytes_sent_mb': round(net.bytes_sent / (1024 ** 2), 2),
                'bytes_recv_mb': round(net.bytes_recv / (1024 ** 2), 2),
            },
            'system': {
                'os':       platform.system() + ' ' + platform.release(),
                'hostname': platform.node(),
                'uptime':   str(uptime).split('.')[0],
                'python':   platform.python_version(),
            },
            'processes': processes,
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
        })

    except Exception as e:
        logging.error(f'Error fetching stats: {e}')
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Simple health-check endpoint — useful for server deployments."""
    return jsonify({'status': 'ok', 'time': datetime.datetime.now().isoformat()})


# ── Entry point ─────────────────────────────────────────
if __name__ == '__main__':
    print("\n  DevPulse is running → http://localhost:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)

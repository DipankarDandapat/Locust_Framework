
import argparse
import os
import subprocess
import yaml
import time
from utils.report_generator import generate_report

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def parse_run_time(run_time_str):
    if not run_time_str:
        return 0
    
    total_seconds = 0
    # Simple parsing for now, can be extended for more complex formats
    if run_time_str.endswith('s'):
        total_seconds = int(run_time_str[:-1])
    elif run_time_str.endswith('m'):
        total_seconds = int(run_time_str[:-1]) * 60
    elif run_time_str.endswith('h'):
        total_seconds = int(run_time_str[:-1]) * 3600
    else:
        # Assume it's in seconds if no unit is specified
        total_seconds = int(run_time_str)
    return total_seconds

def run_locust():
    parser = argparse.ArgumentParser(description='Run Locust performance tests.')
    parser.add_argument('-f', '--locustfile', help='Path to the locustfile.py')
    parser.add_argument('--host', help='Host to test (e.g., http://localhost:8080)')
    parser.add_argument('-u', '--users', type=int, help='Number of concurrent users')
    parser.add_argument('-r', '--spawn-rate', type=int, help='Rate at which users are spawned')
    parser.add_argument('-t', '--run-time', help='Stop after the specified run time, e.g.: (300s, 20m, 3h, 1h30m)')
    parser.add_argument('--headless', action='store_true', help='Run Locust in headless mode (without web UI)')
    parser.add_argument('--csv', help='Store results in CSV format (specify base name)')
    parser.add_argument('--html', help='Store results in HTML format (specify file name)')
    parser.add_argument('--config', help='Path to the YAML configuration file')

    args = parser.parse_args()

    config = {}
    if args.config:
        config = load_config(args.config)

    # Override args with config values if present
    locustfile = args.locustfile or config.get('locustfile')
    host = args.host or config.get('host')
    users = args.users or config.get('users')
    spawn_rate = args.spawn_rate or config.get('spawn_rate')
    run_time = args.run_time or config.get('run_time')
    report_name = args.csv or config.get('report_name')

    if not locustfile:
        raise ValueError("Locustfile must be specified either via --locustfile or in the config file.")

    locust_command = [
        'locust',
        '-f', os.path.join('locust_files', locustfile)
    ]

    if host:
        locust_command.extend(['--host', host])
    if users:
        locust_command.extend(['-u', str(users)])
    if spawn_rate:
        locust_command.extend(['-r', str(spawn_rate)])
    if run_time:
        locust_command.extend(['-t', run_time])
    if args.headless:
        locust_command.append('--headless')
    
    if report_name:
        locust_command.extend(['--csv', os.path.join('reports', report_name)])
        locust_command.extend(['--html', os.path.join('reports', f'{report_name}.html')])

    print(f"Running command: {' '.join(locust_command)}")
    
    # Add a small delay to ensure dummy server is ready
    time.sleep(5)

    print(f"Using run_time: {run_time}")
    print(f"Timeout (with buffer): {parse_run_time(run_time) + 90}")
    timeout_seconds = parse_run_time(run_time) + 90 # Add a buffer


    try:
        result = subprocess.run(locust_command, cwd=os.getcwd(), check=True, capture_output=True, text=True, timeout=timeout_seconds)
        print("Locust stdout:", result.stdout)
        print("Locust stderr:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Locust command failed with error code {e.returncode}")
        print("Locust stdout:", e.stdout)
        print("Locust stderr:", e.stderr)
        return
    except subprocess.TimeoutExpired:
        print("Locust command timed out.")
        return

    # Generate custom reports after Locust run
    if report_name:
        print("Generating custom reports...")
        generate_report(report_name, output_dir='reports')

if __name__ == '__main__':
    run_locust()



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
    if run_time_str.endswith('s'):
        total_seconds = int(run_time_str[:-1])
    elif run_time_str.endswith('m'):
        total_seconds = int(run_time_str[:-1]) * 60
    elif run_time_str.endswith('h'):
        total_seconds = int(run_time_str[:-1]) * 3600
    else:
        try:
            total_seconds = int(run_time_str)
        except ValueError:
            print(f"Warning: Could not parse run_time '{run_time_str}'. Assuming 0 seconds.")
            total_seconds = 0
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

    time.sleep(2)

    if args.headless:
        timeout_seconds = parse_run_time(run_time) + 60  # Add a 60-second buffer
        try:
            result = subprocess.run(locust_command, cwd=os.getcwd(), check=True, capture_output=True, text=True,
                                    timeout=timeout_seconds)
            print("Locust stdout:", result.stdout)
            print("Locust stderr:", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Locust command failed with error code {e.returncode}")
            print("Locust stdout:", e.stdout)
            print("Locust stderr:", e.stderr)
            if report_name:
                print("Attempting to generate reports despite Locust failure...")
                generate_report(report_name, output_dir='reports')
            return
        except subprocess.TimeoutExpired:
            print("Locust command timed out.")
            if report_name:
                print("Attempting to generate reports despite timeout...")
                generate_report(report_name, output_dir='reports')
            return
    else:
        print("Locust UI will start. Please open your browser to http://localhost:8089 to view the UI.")
        print("IMPORTANT: You will need to manually click 'Start swarming' in the Locust UI to begin the test.")
        print(
            f"The test is configured to run for {run_time}. After this duration, or when you manually stop the test in the UI, reports will be generated.")
        process = subprocess.Popen(locust_command, cwd=os.getcwd())

        # Wait for the specified run_time for the test to execute, plus a buffer
        time.sleep(parse_run_time(run_time) + 30)

        print("Attempting to stop Locust process...")
        process.terminate()
        try:
            process.wait(timeout=10)  # Give it some time to terminate
        except subprocess.TimeoutExpired:
            print("Locust process did not terminate gracefully, killing it.")
            process.kill()

    if report_name:
        print("Generating custom reports...")
        generate_report(report_name, output_dir='reports')


if __name__ == '__main__':
    run_locust()


import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_report(csv_file_base_name, output_dir="."):
    # Construct full paths to CSV files
    stats_csv = os.path.join(output_dir, f"{csv_file_base_name}_stats.csv")
    failures_csv = os.path.join(output_dir, f"{csv_file_base_name}_failures.csv")
    stats_history_csv = os.path.join(output_dir, f"{csv_file_base_name}_stats_history.csv")

    # Check if CSV files exist
    if not os.path.exists(stats_csv):
        print(f"Error: {stats_csv} not found.")
        return
    if not os.path.exists(failures_csv):
        print(f"Error: {failures_csv} not found.")
        return
    if not os.path.exists(stats_history_csv):
        print(f"Error: {stats_history_csv} not found.")
        return

    # Load data
    try:
        stats_df = pd.read_csv(stats_csv)
        failures_df = pd.read_csv(failures_csv)
        stats_history_df = pd.read_csv(stats_history_csv)
    except Exception as e:
        print(f"Error loading CSV files: {e}")
        return

    # Basic Summary Report
    summary_report_path = os.path.join(output_dir, f"{csv_file_base_name}_summary.md")
    with open(summary_report_path, "w") as f:
        f.write(f"# Performance Test Report: {csv_file_base_name}\n\n")
        f.write("## Summary Statistics\n\n")
        f.write(stats_df.to_markdown(index=False))
        f.write("\n\n")
        f.write("## Failures\n\n")
        f.write(failures_df.to_markdown(index=False))
        f.write("\n\n")

    print(f"Summary report generated: {summary_report_path}")

    # Plotting Response Time Distribution (using stats_history for percentiles)
    if not stats_history_df.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(stats_history_df["Timestamp"], stats_history_df["50%"], label="50th Percentile")
        plt.plot(stats_history_df["Timestamp"], stats_history_df["95%"], label="95th Percentile")
        plt.xlabel("Time")
        plt.ylabel("Response Time (ms)")
        plt.title("Response Time Percentiles Over Time")
        plt.legend()
        plt.grid(True)
        plot_path = os.path.join(output_dir, f"{csv_file_base_name}_response_time_distribution.png")
        plt.savefig(plot_path)
        print(f"Response time distribution plot generated: {plot_path}")

if __name__ == "__main__":
    pass



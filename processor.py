import time


def process_massive_data(data_list: list):
    """
    High-speed data processing engine for security logs.
    """
    start_time = time.time()
    total_records = len(data_list)
    blocked_ips = []

    # Filtering logic for suspicious activity
    for record in data_list:
        # Threshold: More than 45 login attempts is considered a threat
        if record["attempts"] > 45:
            blocked_ips.append(record["ip"])

    end_time = time.time()
    duration = end_time - start_time

    return {
        "status": "Success",
        "processed_records": total_records,
        "execution_time_seconds": round(duration, 4),
        "threats_detected": len(blocked_ips),
    }

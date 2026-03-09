import time


def process_in_chunks(total_data: list, chunk_size: int = 10000):
    """
    Logic: Process massive data in small batches (chunks)
    to prevent memory overflow. Essential for AI Data Ingestion.
    """
    start_time = time.time()
    processed_count = 0
    threats_found = 0

    # Dividing the 1,000,000 records into chunks of 10,000
    for i in range(0, len(total_data), chunk_size):
        batch = total_data[i : i + chunk_size]

        # Internal logic for each batch
        for record in batch:
            if record["attempts"] > 45:
                threats_found += 1

        processed_count += len(batch)
        print(f"Progress: {processed_count} records analyzed...")

    duration = time.time() - start_time
    return {
        "total_processed": processed_count,
        "threats_detected": threats_found,
        "execution_time": round(duration, 2),
    }

# utils.py
import hashlib
import random
import logging

CHUNK_SIZE = 1024
ERROR_RATE = 0.1  # 10% of chunks will be corrupted

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

def calculate_checksum(data: bytes) -> str:
    checksum = hashlib.sha256(data).hexdigest()
    logger.debug(f"Calculated checksum: {checksum} (data length: {len(data)} bytes)")
    return checksum

def corrupt_chunk(chunk: bytes) -> bytes:
    if random.random() < ERROR_RATE:
        corrupted = bytearray(chunk)
        corrupted[0] ^= 0xFF  # flip first byte
        logger.info(f"Corrupted chunk (original size: {len(chunk)} bytes)")
        return bytes(corrupted)
    logger.debug(f"Passed through uncorrupted chunk (size: {len(chunk)} bytes)")
    return chunk
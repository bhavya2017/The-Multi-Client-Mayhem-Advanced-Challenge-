# client.py
import socket
from utils import calculate_checksum, CHUNK_SIZE
import re
import logging
import time
import os

HOST = 'localhost'
PORT = 5000

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

def parse_chunk(packet):
    try:
        header, payload = packet.split(b"::DATA::", 1)
        meta = header.decode().split("::")
        seq = int(meta[1])
        length = int(meta[3])
        client_id = int(meta[5])
        return seq, payload[:length], client_id
    except Exception as e:
        logger.warning(f"Failed to parse chunk: {str(e)}")
        return None, None, None

def main():
    file_path = input("Enter file path: ")
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    with open(file_path, "rb") as f:
        data = f.read()
    file_size = len(data)
    file_name = os.path.basename(file_path)
    logger.info(f"Preparing to upload {file_name} ({file_size} bytes)")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            logger.info(f"Connected to server at {HOST}:{PORT}")

            # Send filename
            s.sendall(file_name.encode())
            s.recv(3)  # handshake
            logger.info("Filename acknowledged by server")

            # Send file size
            s.sendall(str(file_size).encode())
            s.recv(3)
            logger.info("File size acknowledged by server")

            # Send file data
            start_time = time.time()
            for i in range(0, file_size, CHUNK_SIZE):
                s.sendall(data[i:i+CHUNK_SIZE])
            transfer_time = time.time() - start_time
            logger.info(f"Upload completed in {transfer_time:.2f}s")

            logger.info("[>] Waiting for file from server...")
            received_chunks = {}
            total_chunks = (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE
            missing = set(range(total_chunks))
            retry_count = 0

            while len(received_chunks) < total_chunks:
                try:
                    packet = s.recv(CHUNK_SIZE + 100)
                    seq, chunk, client_id = parse_chunk(packet)
                    if seq is not None and seq not in received_chunks:
                        received_chunks[seq] = chunk
                        missing.discard(seq)
                        logger.debug(f"Received chunk {seq} (size: {len(chunk)} bytes)")
                except Exception as e:
                    logger.warning(f"Error receiving chunk: {str(e)}")
                    continue

            # Retransmit if needed
            if missing:
                logger.warning(f"Missing chunks detected: {sorted(missing)}")
                s.sendall(f"RETRANSMIT:{','.join(map(str, sorted(missing)))}".encode())
                retry_count += 1
                logger.info(f"Requested retransmission of {len(missing)} chunks")
                
                for _ in range(len(missing)):
                    packet = s.recv(CHUNK_SIZE + 100)
                    seq, chunk, client_id = parse_chunk(packet)
                    if seq is not None:
                        received_chunks[seq] = chunk
                        logger.debug(f"Received retransmitted chunk {seq}")

            s.sendall(b"DONE")
            logger.info(f"Transfer completed with {retry_count} retransmissions")

            # Receive checksum
            server_checksum = s.recv(1024).decode().split("::")[1]
            logger.info(f"Received server checksum: {server_checksum}")

            # Reassemble file
            reassembled = b''.join([received_chunks[i] for i in sorted(received_chunks)])
            local_checksum = calculate_checksum(reassembled)
            logger.info(f"Calculated local checksum: {local_checksum}")

            # Verify checksum
            if local_checksum == server_checksum:
                output_path = "received_" + file_name
                with open(output_path, "wb") as f:
                    f.write(reassembled)
                logger.info(f"[✓] File verified and saved as {output_path}")
                logger.info(f"File size: {len(reassembled)} bytes")
            else:
                logger.error("[✗] Checksum mismatch! File may be corrupted.")

        except Exception as e:
            logger.error(f"Client error: {str(e)}", exc_info=True)
        finally:
            s.close()
            logger.info("Connection closed")

if __name__ == "__main__":
    main()
# server.py
import socket
import threading
import time
from utils import calculate_checksum, corrupt_chunk, CHUNK_SIZE
import logging
from datetime import datetime

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

def send_chunk(conn, client_id, seq, chunk):
    header = f"SEQ::{seq}::LEN::{len(chunk)}::CLIENT::{client_id}::DATA::".encode()
    data = header + corrupt_chunk(chunk)
    conn.sendall(data)
    logger.info(f"Sent chunk {seq} to client {client_id} (size: {len(chunk)} bytes)")

def handle_client(conn, addr):
    client_id = addr[1]
    logger.info(f"New connection from client {client_id} ({addr[0]})")

    try:
        # Receive filename
        filename = conn.recv(1024).decode()
        logger.info(f"Client {client_id} requested to upload file: {filename}")
        conn.sendall(b"ACK")  # handshake
        
        # Receive file size
        file_size = int(conn.recv(1024).decode())
        logger.info(f"Client {client_id} file size: {file_size} bytes")
        conn.sendall(b"ACK")

        # Receive file data
        data = b''
        start_time = time.time()
        while len(data) < file_size:
            chunk = conn.recv(CHUNK_SIZE)
            if not chunk:
                break
            data += chunk
        transfer_time = time.time() - start_time
        logger.info(f"Received full file from client {client_id} in {transfer_time:.2f}s ({len(data)} bytes)")

        # Calculate checksum and prepare chunks
        checksum = calculate_checksum(data)
        chunks = [data[i:i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
        logger.info(f"File split into {len(chunks)} chunks for client {client_id}")

        # Send file back (potentially corrupted)
        logger.info(f"Starting transmission back to client {client_id}")
        for seq, chunk in enumerate(chunks):
            send_chunk(conn, client_id, seq, chunk)
            time.sleep(0.01)  # simulate network delay

        # Retransmission loop
        retransmit_count = 0
        while True:
            conn.settimeout(5)
            try:
                msg = conn.recv(1024).decode()
                if msg.startswith("RETRANSMIT"):
                    seq_nums = list(map(int, msg.split(":")[1].split(",")))
                    logger.info(f"Client {client_id} requested retransmission of chunks: {seq_nums}")
                    for seq in seq_nums:
                        send_chunk(conn, client_id, seq, chunks[seq])
                        retransmit_count += 1
                elif msg == "DONE":
                    logger.info(f"Client {client_id} completed transfer with {retransmit_count} retransmissions")
                    break
            except socket.timeout:
                logger.warning(f"Timeout waiting for client {client_id}, ending session")
                break

        # Send final checksum
        conn.sendall(f"CHECKSUM::{checksum}".encode())
        logger.info(f"Sent checksum to client {client_id}: {checksum}")

    except Exception as e:
        logger.error(f"Error with client {client_id}: {str(e)}", exc_info=True)
    finally:
        conn.close()
        logger.info(f"Connection closed for client {client_id}")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    s.settimeout(1.0)  # timeout after 1 second to check for KeyboardInterrupt
    logger.info(f"Server started on {HOST}:{PORT}, waiting for connections...")

    try:
        while True:
            try:
                conn, addr = s.accept()
                logger.info(f"Accepted connection from {addr}")
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue  # check for KeyboardInterrupt every 1 second
    except KeyboardInterrupt:
        logger.info("Server shutting down gracefully...")
    finally:
        s.close()
        logger.info("Server socket closed")

if __name__ == "__main__":
    main()
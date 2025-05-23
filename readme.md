# 📁 Multi-Client Mayhem — Real-Time File Transfer and Verification System

## 🧠 Overview

This project is a **robust, real-time, multi-client file transfer system** using TCP sockets. It supports:

- ✅ Concurrent file uploads from multiple clients
- ✅ Server re-transmits the file back to clients in chunks
- ✅ SHA-256 checksum verification
- ✅ Simulated packet drops and corruption
- ✅ Retransmission and out-of-order packet handling
- ✅ Graceful shutdown of the server using `Ctrl+C`

---

## ⚙️ Features

- **TCP-Based Communication** for reliable transport
- **Multithreaded Server** to handle multiple clients independently
- **Fixed-Size Chunking** (default: 1024 bytes)
- **Checksum Validation** using SHA-256
- **Simulated Network Errors** for testing robustness
- **Client-Side File Reassembly and Error Detection**
- **Automatic Retransmission** for missing or corrupted chunks

---


## 🚀 How to Run

### 1. Start the Server

```bash
python server.py
```
### 2. run clients
```bash
python client.py path/to/data1.txt
python client.py path/to/data2.txt
```

Each client:
- **Uploads the file**
- **Receives it back chunk-by-chunk (with simulated corruption)**
- **Reassembles and validates using checksum**
- **Prints Transfer Successful or Transfer Failed**

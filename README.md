# The-Multi-Client-Mayhem-Advanced-Challenge-
This project implements a robust real-time client-server file transfer system that supports multiple clients concurrently uploading and downloading files. Each client's file is sent to the server, split into fixed-size chunks, and then transmitted back with simulated network errors such as packet drops and corruption. 


```markdown
# The Multi-Client Mayhem - Advanced Challenge

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A robust real-time client-server file transfer system that supports multiple concurrent clients with simulated network errors and automatic retransmission.

## Features

- 🚀 Multi-client concurrent file transfers
- 🔄 Automatic chunk retransmission
- 🛡️ Checksum verification (SHA-256)
- 💥 Simulated network errors (10% corruption rate)
- 📊 Detailed logging for debugging
- ⏱️ Performance metrics tracking

## Prerequisites

- Python 3.7+
- Basic network connectivity (localhost)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bhavya2017/The-Multi-Client-Mayhem-Advanced-Challenge.git
cd The-Multi-Client-Mayhem-Advanced-Challenge
```

2. No additional dependencies required (uses standard Python libraries)

## Usage

### Starting the Server
```bash
python server.py
```

### Running Clients
In separate terminal windows:
```bash
python client.py
```
When prompted, enter the path to your test file (e.g., `data1.txt` or `data2.txt`)

### Sample Test Files
The repository includes:
- `data1.txt` - 5KB sample file
- `data2.txt` - 8KB sample file

## Workflow Explanation

1. Client uploads file to server
2. Server:
   - Splits file into chunks (1024 bytes each)
   - Simulates network errors (10% corruption)
   - Sends chunks back to client
3. Client:
   - Reassembles file from chunks
   - Requests retransmission of corrupted/missing chunks
   - Verifies file integrity using checksum
   - Saves received file as `received_<filename>`

## Monitoring

Both server and client display real-time logs showing:
- Connection events
- File transfer progress
- Chunk transmission details
- Retransmission requests
- Checksum verification results

## Testing

Try these scenarios:
1. Single client transfer
2. Multiple concurrent clients
3. Large file transfers (>1MB)
4. Network interruption simulation

## File Structure

```
.
├── client.py            # Client implementation
├── server.py            # Server implementation
├── utils.py             # Shared utilities
├── data1.txt            # Sample test file (5KB)
├── data2.txt            # Sample test file (8KB)
├── received_data1.txt   # Example received file
├── received_data2.txt   # Example received file
└── README.md            # This file
```

## Customization

You can adjust these parameters in `utils.py`:
- `CHUNK_SIZE` - Change chunk size (default: 1024 bytes)
- `ERROR_RATE` - Adjust corruption probability (default: 0.1 = 10%)

## Troubleshooting

Common issues:
- Port 5000 already in use: Change `PORT` in both files
- File not found: Use absolute paths or place files in project directory
- Connection refused: Ensure server is running first



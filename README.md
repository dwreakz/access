# RFID Access Control System

This is an RFID-based access control system designed for Raspberry Pi 
that allows you to manage multiple doors using RFID tags for authentication.

## Features

- Control multiple doors with RFID authentication
- User-friendly GUI interface with status display
- Enrollment mode for adding/removing RFID tags
- Command-line options for quick deployment 
- Configuration stored in JSON format

## System Components

1. **RFID Reader**: Interfaces with PN532 RFID reader via I2C
2. **Hardware Control**: Manages door relays and button inputs via GPIO
3. **GUI**: Simple fullscreen interface showing system status
4. **State Machine**: Handles access control logic and enrollment process
5. **Configuration**: Stores door settings and authorized tags

## Installation

1. Clone the repository
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure `config.json` with your door settings and master tag
4. Connect the hardware according to the pin configuration

## Hardware Requirements

- Raspberry Pi
- PN532 RFID reader (I2C interface)
- Relay modules for door control
- Buttons for enrollment mode
- Display for GUI (optional)

## Usage

### Normal Operation

Run the system with:

python main.py

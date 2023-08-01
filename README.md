![GREENMONITOR](https://github.com/rokkino/ESP32-Green-Monitor-Webserver/assets/109034293/c332f3c1-494c-4c57-9602-2fb6828d9ec6)
# WebServer for ESP32 in MicroPython

***At the moment working only with ESP32 with additional SPIRAM (due to high heap memory requirement), you can butch the code to try make it fit, i will work on this issue***

This repository contains the code for an Internet of Things (IoT) web server implemented in MicroPython for ESP32 devices. The web server allows you to connect your ESP32 to your network and control its ports, enabling automation and remote control capabilities.

# Showcase
Here you can have a look of the functionalities:

Overview:
![Screenshot_20230731_101142_Chrome](https://github.com/rokkino/ESP32-Green-Monitor-Webserver/assets/109034293/49fe882c-121d-4cbc-9487-74b763f87cbb)

Functions:
![Screenshot_20230731_101202_Chrome](https://github.com/rokkino/ESP32-Green-Monitor-Webserver/assets/109034293/b2a492f2-1914-42b6-9707-3f5058370b3e)

Settings:
![Screenshot_20230731_101217_Chrome](https://github.com/rokkino/ESP32-Green-Monitor-Webserver/assets/109034293/a59bb843-1253-47ba-82f9-6a5762b081de)

## Installation

### Prerequisites

Before installing and running the web server, please make sure you have the following dependencies installed on your system:

1. **rshell** - A remote shell tool for MicroPython devices.
2. **rsync** - A fast and versatile file synchronization tool.
3. **esptool** - A utility for erasing and flashing MicroPython firmware onto ESP32 devices.

#### Windows

1. **rshell**: Install rshell using pip by running the following command in your command prompt or PowerShell:

   ```shell
   pip install rshell
   ```

2. **rsync**: Download and install cwRsync from [cwRsync Downloads](https://www.itefix.net/cwrsync) to get rsync on your Windows machine.

3. **esptool**: Install esptool using pip by running the following command:

   ```shell
   pip install esptool
   ```

#### Linux

1. **rshell**: Install rshell using pip by running the following command in your terminal:

   ```shell
   pip install rshell
   ```

2. **rsync**: Install rsync using the package manager specific to your Linux distribution. For example, on Debian-based systems, run:

   ```shell
   sudo apt-get install rsync
   ```

3. **esptool**: Install esptool using pip by running the following command:

   ```shell
   pip install esptool
   ```

#### macOS

1. **rshell**: Install rshell using pip by running the following command in your terminal:

   ```shell
   pip install rshell
   ```

2. **rsync**: Install rsync using Homebrew by running the following command:

   ```shell
   brew install rsync
   ```

3. **esptool**: Install esptool using pip by running the following command:

   ```shell
   pip install esptool
   ```

### Flashing MicroPython Firmware

To install the latest version of MicroPython on your ESP32 device, follow these steps:

1. Connect your ESP32 device to your computer via USB.

2. Open a terminal or command prompt.

3. Erase the flash memory of the ESP32 by running the following command:

   ```shell
   esptool.py --port /dev/ttyUSB0 erase_flash
   ```

   Note: Replace `/dev/ttyUSB0` with the appropriate port identifier for your ESP32 device.

4. Download the latest MicroPython firmware for ESP32 from the [MicroPython Downloads](https://micropython.org/download/#esp32) page. Make sure to select the `.bin` file for the ESP32.

5. Install the downloaded firmware onto the ESP32 device by running the following command:

   ```shell
   esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin
   ```

   Note: Again, replace `/dev/ttyUSB0` with the appropriate port identifier for your ESP32 device, and `esp32-20230426-v1.20.0.bin` with the name of the downloaded firmware file.

### Uploading WebServer Files

To upload the web server files to your ESP32 device, follow these steps:

1. Open a terminal or command prompt.

2. Change your current directory to the location where you have the web server files.

3. Run the following command to start the rshell shell:

   ```shell
   rshell --buffer-size=30 -p /dev/ttyUSB0 -a -e nano
   ```

   Note: Replace `/dev/ttyUSB0` with the appropriate port identifier for your ESP32 device.

4. Once inside the rshell shell, run the following command to synchronize the files with the ESP32:

   ```shell
   rsync . /pyboard
   ```

   This command will copy all the files from the current directory to the `/pyboard` directory on the ESP32.

5. After uploading the files to the ESP32 using rsync, you can access the ESP32's REPL (Read-Eval-Print Loop) to interact with the microcontroller and debug the data. Here's how you can do it:

   ```shell
   repl
   ```
   Then press Ctrl + D to reboot the microcontroller and debug the data. 

## Usage

After successfully uploading the web server files to your ESP32, you can now access the web server and control the ESP32's ports. Connect your ESP32 to your network, and then open a web browser and enter the IP address assigned to the ESP32. You will be presented with a user interface where you can interact with the ports and automate their functionality.

Feel free to explore and customize the web server code according to your specific requirements.

## License

This project is licensed under the  Apache-2.0 license.

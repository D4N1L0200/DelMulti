# DelMulti

This project is a simple Server-Client system developed in Python using sockets and Pygame. It enables multiple clients to connect to a server and interact with each other by controlling movable squares on a shared canvas. The primary focus of the project is to provide a multiplayer framework, with each player represented as a square that can be moved using the WASD keys. While the core functionality centers around movable squares, additional features can be added to enhance gameplay.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Changelog and Roadmap](#changelog-and-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

You have two options for installing and running DelMulti:

### Option 1: Using Pre-built Executables (Recommended)

1. Visit the [Releases](https://github.com/D4N1L0200/DelMulti/releases) page on GitHub.
2. Download the latest release, which includes pre-built executables for both the client and server.
3. Run `server.exe` to start the server.
4. Run `client.exe` to start a client.
5. Clients can connect to the server by specifying the server's IP address.

### Option 2: Building from Source

If you prefer to build the project from source code, follow these steps:

1. Clone the repository: `git clone https://github.com/D4N1L0200/DelMulti.git`
2. Navigate to the project directory: `cd DelMulti`
3. Install dependencies: `pip install pygame`
4. Build the executables? `build.bat`
5. Start the server: `.\dist\server.exe`
6. Run clients: `.\dist\client.exe`

## Usage

- **Starting the Server**: Run `server.exe` to start the server. By default, it will listen on `localhost` (127.0.0.1) on port 8080.
  - If you want the server to be accessible from other devices or through a VPN, type the desired IP address (e.g., the IP address of your VPN connection) when prompted and press Enter.

- **Running Clients**: Execute `client.exe` to start a client. When starting a client, you must specify the IP address of the server you want to connect to interactively in the terminal as follows:
  - When prompted, type the IP address of the server (e.g., the IP address of the server where `server.py` is running) and press Enter.

- **Playing the Game**: Each player is represented by a movable square on the game canvas. Use the WASD keys to move your square around the canvas. The squares of all connected players will be displayed.

## <a id="changelog-and-roadmap"></a> Changelog and Roadmap

- For a detailed list of changes, updates, planned features and bugfixes, please refer to the [Changelog and Roadmap](CHANGELOG-ROADMAP.md).

## Contributing

Contributions to this project are welcome! If you'd like to contribute, please follow these guidelines:

- Check the issue tracker for open issues or create a new one if you identify a problem or have an enhancement idea.
- Fork the repository and create a new branch for your feature or bug fix.
- Ensure your code adheres to Python's PEP 8 style guide.
- Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the Python community for their contributions to the Python language, and to the Pygame library for enabling the creation of the graphical interface in this project.

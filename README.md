# Minecraft Mod Dependency Checker

## Version: 1.1.0

### Description

This tool reads the manifests in your mod folders .jar files and extracts information about the mandatory dependencies that each mod requires.
This helps to determine what libraries your mods in your installation or modpack require to function.
(For example, I created this tool to figure out what libraries I no longer needed after removing some mods from my modpack.)

### Prerequisites

- Python 3.x
- Required Python modules: `rich`, `prettytable`

### Installation

1. Download and install Python from [python.org](https://www.python.org/).
2. Clone this project to your machine
3. (Recommended) Make a venv
   ```sh
   python -m venv .venv
   source .venv/bin/activate # for UNIX systems
   ```
4. Install the required Python modules:
   ```sh
   pip install -r requirements.txt
   ```

### Usage

1. Find the path of the folder containing all your mods
2. Run the script:
   ```sh
   python run.py "<path_to_mod_folder>"
   ```
3. Respond to the prompts from the program to get information about the mods

### License

This project is licensed under the MIT License.

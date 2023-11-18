# Python Scripting

The project is a software utility designed to streamline the compilation process for game code written in the Go (Golang) programming language. Additionally, it generates metadata for the compiled games. The script is specifically tailored for projects structured with directories named according to a predefined pattern.

Key Features:
Finding Game Paths:

Recursively searches for directories with names containing the "game" pattern within the specified source directory.
Compiling Game Code:

Identifies Go code files (with the ".go" extension) within each game directory and compiles them using the "go build" command.
Copying and Overwriting:

Copies the compiled game and its entire directory structure to the target directory, overwriting any existing content.
Metadata Generation:

Creates a JSON metadata file, named "metadata.json," in the target directory. This file contains information about the compiled games, including their names and the total number of games.
Use Case:
This utility is useful for developers working on multiple game projects structured with a specific directory pattern, automating the compilation and organization of game code.

## Installation

To use this project, follow the installation steps:

1. **Clone this repository:**
    ```bash
    git clone https://github.com/user/project-name.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd project-name
    ```

3. **Other installation steps if needed.**

## Usage

Explain how to use the project. It may include code examples or screenshots.

```python
# Code example
print("Hello, world!")

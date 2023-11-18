import os
import json
import shutil  # allow to copy and overwrite operations
from subprocess import PIPE, run  # allow us to run every terminal command
import sys  # access to the command line arguments
from contextlib import contextmanager  # context manager with a decorator

GAME_DIR_PATTERN = "game"  # we where looking for this in every directory
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]


def find_all_game_paths(source):
    game_paths = []

    for root, dirs, files in os.walk(
        source
    ):  # we walk recursively true directories and get us file, dir, path
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)  # return all path
                game_paths.append(path)
        break

    return game_paths


def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)  # Give us the las part of the directory
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)  # recursive delete
    shutil.copytree(source, dest)


def compile_game_code(path):
    # locate the name of the file to compile .go
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):  # .go
                code_file_name = file
                break

        break

    if code_file_name is None:
        return

    command = GAME_COMPILE_COMMAND + [
        code_file_name
    ]  # make the command be go build filename
    run_command(command, path)


# We'll change the directory where the go file is run and then go back to the python file directory
def run_command(command, path):
    cwd = os.getcwd()  # get the current directory
    os.chdir(path)

    # stdout, stdin the location where the command accepts input and output, PIPE bridge between python and process to run this
    results = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print(results)

    os.chdir(cwd)  # change back into the previous to avoid errors


def make_json_metadata_file(path, game_dirs):
    data = {"gameNames": game_dirs, "numberOfGames": len(game_dirs)}

    # Context Manager
    @contextmanager
    def file(filename, method):
        file = open(filename, method)
        yield file
        file.close()

    with file(path, "w") as f:
        json.dump(data, f)  # save data in a file


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(
        cwd, source
    )  # join the path on whatever system operation you are
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "_game")

    create_dir(target_path)

    # Example for zip():
    # [1, 2, 3]
    # ["a", "b", "c"]
    # => [(1, "a"), (2, "b"), (3, "c")]

    # zip() take matching elements from two arrays and combine them into a tuple

    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)

    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only.")

    source, target = args[1:]
    main(source, target)

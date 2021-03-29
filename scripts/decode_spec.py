# Script to decode the project specification
# Ümit Kaan Usta
# u.kaanusta@gmail.com
import os
from base64 import b64decode


def read_binary(filename):
    with open(f"./kartaca/{filename}", "r") as f:
        content = f.read()
    return "".join([chr(int(c, 2)) for c in content.split()])


def read_binaries(_files):
    return "".join([read_binary(file) for file in _files])


def read_filenames(_files):
    return [int(b64decode(file.encode("ascii")).decode("ascii")) for file in _files]


def filenames_list():
    return os.listdir("./kartaca")


def main():
    files = filenames_list()
    files_dict = dict(zip(files, read_filenames(files)))
    sorted_dict = sorted(files_dict.items(), key=lambda x: x[1])
    sorted_filenames = [pair[0] for pair in sorted_dict]
    content = read_binaries(sorted_filenames)
    with open("project_spec.txt", "w") as f:
        f.write(content)


if __name__ == '__main__':
    main()

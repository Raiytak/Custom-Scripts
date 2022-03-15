from typing import Union
from pathlib import Path
import eyed3
import argparse

MP3_EXTENSION = ".mp3"
STRANGE_FILES = []


def changeAllFilesOfDirectoryRecursively(
    directory_path: Path,
    album_name: Union[str, None],
    extension: str,
    endpoint_only: bool,
):
    unmodified_files = []
    list_files = directory_path.iterdir()
    for curr_file in list_files:
        modifications_allowed = (
            checkIsEndpoint(directory_path) if endpoint_only else True
        )
        if curr_file.is_file() and curr_file.suffix == extension:
            unmodified = []
            if modifications_allowed:
                unmodified = changeAlbumTagOfFile(curr_file, album_name)
        else:
            try:
                unmodified = changeAllFilesOfDirectoryRecursively(
                    curr_file, album_name, extension, endpoint_only
                )
            except NotADirectoryError:
                STRANGE_FILES.append([directory_path, curr_file])
        unmodified_files += unmodified
    return unmodified_files


def changeAlbumTagOfFile(path_file: Path, album_name: Union[str, None]):
    audiofile = eyed3.load(str(path_file))
    if audiofile is None:
        print(
            "The file '{}' could not be loaded using eyed3\n{}".format(
                path_file.stem, str(path_file)
            )
        )
        return [str(path_file)]

    if album_name is None:
        album_name = str(path_file.parent.stem)
    audiofile.tag.album = album_name
    audiofile.tag.save()
    print("Modified '{}' album's name to '{}'".format(path_file.stem, album_name))
    return []


def askPathDirectory(endpoint_only: bool, recursively: bool) -> Path:
    is_good_dir = False
    while not is_good_dir:
        path_dir = Path(str(input("Directory path (none=realtive) = ")))
        if path_dir.is_dir():
            if not recursively:
                if endpoint_only:
                    is_good_dir = checkIsEndpoint(path_dir)
                    if not is_good_dir:
                        print("The path provided does not contains only files")
                else:
                    is_good_dir = True
            else:
                is_good_dir = True
        else:
            print("The path provided is not a directory")
    return path_dir


def checkIsEndpoint(folder_path: Path):
    """Returns True if all files within the directory are of the expected extension"""
    list_files = folder_path.iterdir()
    if all([file.is_file() for file in list_files]):
        return True
    return False


def askAlbumName():
    bool_satisfied = False
    while bool_satisfied != True:
        album_name = str(input("Album name: "))
        if album_name != "":
            bool_satisfied = True
    return album_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Alterate album's name of '.mp3' files."
    )
    parser.add_argument(
        "-p",
        "--path",
        help="Path to the directory containing the '.mp3' files to modify",
        type=str,
    )
    parser.add_argument(
        "-n",
        "--album-name",
        help="Path to the directory containing the '.mp3' files to modify",
        type=str,
    )
    parser.add_argument(
        "--recursively",
        help="If set, modifies recursively all the '.mp3' files for the given path",
        action="store_true",
    )
    parser.add_argument(
        "--endpoint-only",
        help="Modifies folders contaigning only '.mp3' files",
        action="store_true",
    )
    args = parser.parse_args()

    endpoint_only = args.endpoint_only
    if not args.path:
        user_path = askPathDirectory(endpoint_only, args.recursively)
    else:
        user_path = Path(args.path)

    album_name = None
    if args.album_name:
        album_name = args.album_name
    else:
        if not args.recursively:
            album_name = askAlbumName()

    if not args.recursively:
        if endpoint_only:
            is_ok = checkIsEndpoint(user_path)
            if not is_ok:
                raise AttributeError(
                    "The given directory does not contains only {} files".format(
                        MP3_EXTENSION
                    )
                )
        list_files = [
            x for x in user_path.iterdir() if x.is_file() and x.suffix == MP3_EXTENSION
        ]
        for file in list_files:
            unmodified_files = changeAlbumTagOfFile(file, album_name)
    else:
        unmodified_files = changeAllFilesOfDirectoryRecursively(
            user_path, album_name, MP3_EXTENSION, endpoint_only
        )
    if unmodified_files != []:
        print("\n## The following files could not be loaded using eyed3: ##")
        print("\n".join(unmodified_files))

    if STRANGE_FILES != []:
        print(
            "\n".join(
                [
                    "**A strange file has been detected inside '{}' named '{}'**".format(
                        directory_path, curr_file.stem
                    )
                    for directory_path, curr_file in STRANGE_FILES
                ]
            )
        )

    print("The operation is a success!")

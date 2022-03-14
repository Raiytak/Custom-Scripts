from pathlib import Path
import eyed3
import argparse

MP3_EXTENSION = ".mp3"


def introduction():
    print(
        "To modify your .mp3 files, the path of the DIRECTORY \n",
        "that contains the .mp3, and the is needed and\n",
        "NAME of the album that you want to give \n",
    )


def changeAllFilesOfDirectoryRecursively(directory_path: Path):
    unmodified_files = []
    list_files = directory_path.iterdir()
    for curr_file in list_files:
        if curr_file.is_file():
            unmodified = changeAlbumTagOfFile(curr_file, directory_path.stem)
        else:
            unmodified = changeAllFilesOfDirectoryRecursively(curr_file)
        unmodified_files += unmodified
    return unmodified_files


def changeAlbumTagOfFile(path_file: Path, album_name: str):
    audiofile = eyed3.load(str(path_file))
    if audiofile is None:
        print(
            "The file '{}' could not be loaded using eyed3\n{}".format(
                path_file.stem, str(path_file)
            )
        )
        return [str(path_file)]

    audiofile.tag.album = album_name
    audiofile.tag.save()
    print("Modified '{}' album's name to '{}'".format(path_file.stem, album_name))
    return []


def getAllFileWithExtension(folder_path: Path, extension: str) -> list:
    return [x for x in folder_path.iterdir() if x.is_file() and x.suffix == extension]


def askPathDirectory(needs_to_be_endpoint: bool) -> Path:
    is_good_dir = False
    while not is_good_dir:
        path_dir = Path(str(input("Directory path (none=realtive) = ")))
        if path_dir.is_dir():
            if needs_to_be_endpoint:
                is_good_dir = checkIsEndpoint(path_dir, MP3_EXTENSION)
            else:
                is_good_dir = True
        else:
            print("The path provided is not a directory")
    return path_dir


def checkIsEndpoint(folder_path: Path, extension: str):
    list_files = getAllFileWithExtension(folder_path, extension)
    # Assert that all files within the directory are of the expected extension
    if all([file.stem == extension for file in list_files]):
        return True
    else:
        print(f"The directory given does not contains {extension} file")
    return False


def askAlbumName():
    bool_satisfied = False
    while bool_satisfied != True:
        album_name = str(input("Album name: "))
        if album_name != "":
            bool_satisfied = True
    return album_name


if __name__ == "__main__":
    introduction()

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
        "--all",
        help="If set, modifies recursively all the '.mp3' files for the given path, set every file's album's name to their directory's name",
        nargs="?",
    )
    parser.add_argument(
        "--endpoints-only",
        help="Modifies the folders contaigning only '.mp3' files",
        nargs="?",
    )
    args = parser.parse_args()

    needs_to_be_endpoint = args.endpoints_only is not None
    if not args.path:
        user_path = askPathDirectory(needs_to_be_endpoint)
    else:
        user_path = Path(args.path)
        if needs_to_be_endpoint:
            checkIsEndpoint(user_path, MP3_EXTENSION)

    if args.all is None:
        album_name = askAlbumName()
        list_files = getAllFileWithExtension(user_path, MP3_EXTENSION)
        for name_mp3 in list_files:
            unmodified_files = changeAlbumTagOfFile(name_mp3, album_name)
    else:
        unmodified_files = changeAllFilesOfDirectoryRecursively(user_path)
    if unmodified_files != []:
        print("\n## The following files could not be loaded using eyed3: ##")
        print("\n".join(unmodified_files))

    print("The operation is a success!")


# /home/mathieu/Music/Anime

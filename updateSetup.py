import argparse
import json

version_modifiers = [
    "major",
    "minor",
    "patch"
]
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI setup.json updater"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store",
        dest="version",
        help="Updates the version. Either a version modifier or a version string."
    )
    args = parser.parse_args()
    with open("setup.json", "r+") as setup:
        setupJSON = json.loads(setup.read())
        version = setupJSON["version"]
        parts = list(
            map(
                lambda s: int(s),
                version.split(".")
            )
        )
        delVersion = args.version
        if delVersion in version_modifiers:
            index = version_modifiers.index(delVersion)
            parts[index] = parts[index] + 1
            setupJSON["version"] = ".".join(list(
                map(
                    lambda i: str(i),
                    parts
                )
            ))
        else:
            setupJSON["version"] = delVersion
    with open("setup.json", "w") as setup:
        json.dump(setupJSON, setup, indent=4)
        print("{0} updated to {1}".format(version, setupJSON["version"]))

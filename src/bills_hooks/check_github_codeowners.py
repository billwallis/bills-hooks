import argparse
import dataclasses
import glob
import logging
import pathlib
from collections.abc import Generator, Sequence

SUCCESS = 0
FAILURE = 1
ROOT = "."  # Is there a "better" way to always get the dir under test?

GREY = "\033[38;5;240m"
RESET = "\033[0m"

logger = logging.getLogger(__file__)
logging.basicConfig(
    level=logging.INFO,
    format=f"{GREY}%(asctime)s{RESET}  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclasses.dataclass
class PatternOwners:
    line_number: int
    pattern: str
    owners: list[str]

    @classmethod
    def from_line(cls, line_number: int, line: str) -> PatternOwners:
        parts = line.split(" ")
        return cls(
            line_number=line_number,
            pattern=parts[0],
            owners=parts[1:],
        )


def parse_codeowners(contents: str) -> list[PatternOwners]:
    def _parse(lines: list[str]) -> Generator[PatternOwners]:
        for line_number, line in enumerate(lines):
            # ignore comments
            if line.lstrip().startswith("#"):
                continue

            # else parse line
            yield PatternOwners.from_line(line_number=line_number, line=line)

    return list(_parse(contents.splitlines()))


def validate_pattern(pattern: str, line_number: int) -> Exception | None:
    # https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners#codeowners-syntax
    logger.debug(f"validating pattern '{pattern}'")

    if pattern == "*":
        return None

    if pattern.startswith("/") and "*" not in pattern:
        path = pathlib.Path(f"{ROOT}/{pattern.lstrip('/')}")
        if path.exists():
            return None
        else:
            return FileNotFoundError(
                f"line {line_number}: pattern {pattern} is invalid: no such path ({path})"
            )

    # if starts with `/`, then pattern is relative to the root
    # else can match anywhere in the repo
    if pattern.startswith("/"):
        found_files = glob.glob(f"{ROOT}{pattern}", recursive=True)
    else:
        found_files = glob.glob(f"{ROOT}/**/{pattern}", recursive=True)

    if found_files:
        return None
    else:
        return FileNotFoundError(
            f"line {line_number}: pattern '{pattern}' is invalid: no files match this pattern"
        )


def validate_owners(owners: list[str], line_number: int) -> list[Exception]:
    logger.debug(f"validating owners '{owners}'")
    if not owners:
        return []

    exceptions = []
    for owner in owners:
        if not owner.startswith("@"):
            exceptions.append(
                ValueError(f"line {line_number}: owner '{owner}' is invalid: does not start with @")
            )

    return exceptions


def validate_path_owners(path_owners: list[PatternOwners]) -> list[Exception]:
    exceptions = []
    for path_owner in path_owners:
        if path_result := validate_pattern(path_owner.pattern, path_owner.line_number):
            exceptions.append(path_result)
        if owners_result := validate_owners(path_owner.owners, path_owner.line_number):
            exceptions.extend(owners_result)

    return exceptions


def check_github_codeowners(filename: str) -> int:
    """
    Validate the GitHub CODEOWNERS file.
    """

    logger.debug(f"running with root: '{ROOT}'")

    filepath = pathlib.Path(filename)
    path_owners = parse_codeowners(filepath.read_text(encoding="utf-8"))
    exceptions = validate_path_owners(path_owners)
    if exceptions:
        for exception in exceptions:
            logging.error(f"error: {exception}")
        return FAILURE

    return SUCCESS


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the hook.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    outcome = SUCCESS
    for filename in args.filenames:
        outcome |= check_github_codeowners(filename)
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover

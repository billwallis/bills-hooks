import argparse
import ast
from collections.abc import Sequence

SUCCESS = 0
FAILURE = 1
RED = "\033[1;31m"
RESET = "\033[0m"


def _node_has__pytest_raises_match(node: ast.AST) -> bool:
    if isinstance(node, ast.Call):
        func_attr = getattr(node.func, "attr", "")
        func_name = getattr(node.func, "value", None)
        if (
            func_attr == "raises"
            and func_name is not None
            and func_name.id == "pytest"
            and any(kw.arg == "match" for kw in node.keywords)
        ):
            return True
    return False


def check_banned_python_code(filename: str, args: argparse.Namespace) -> int:
    """
    Check for "banned" Python code.
    """

    with open(filename, encoding="utf-8") as f:
        content = f.read()

    try:
        parsed = ast.parse(content)
    except SyntaxError:
        # If we can't parse it, we don't know if it has the comment, so
        # we can't correctly fail
        return SUCCESS

    for node in ast.walk(parsed):
        if _node_has__pytest_raises_match(node):
            assert isinstance(node, ast.Call)  # noqa: S101
            print(
                f"{RED}Use of `pytest.raises(..., match='')` detected{RESET}: {filename}:{node.lineno}:{node.col_offset}"
            )
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
        outcome |= check_banned_python_code(filename, args)
    return outcome


if __name__ == "__main__":
    raise SystemExit(main([__file__]))  # pragma: no cover

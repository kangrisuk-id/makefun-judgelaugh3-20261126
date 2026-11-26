"""Make the Judge Laugh in One Line — entry program.

Writes exactly one funny line (94 characters, inside the 1-200 gate) to
entry.txt in the output directory. Pure standard library, fully
deterministic: the same bytes on every run.
"""

import os

# The winning line, picked from 40 candidates by an ordered-criteria
# knockout against the judge brief (see candidates.md). No trailing
# newline is added by this program beyond what write_text is given:
# the line itself is the whole artifact.
LINE = (
    "I taught my parrot to say 'allegedly,' and now every statement "
    "in this house is legally safer."
)


def candidate_paths():
    """Yield output paths in priority order.

    The grader's MAKEFUN_OUTPUT_DIR comes first, then the harness's
    conventional /output, then a local ./output for manual runs.
    """
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        yield os.path.join(env_dir, "entry.txt")
    yield os.path.join("/output", "entry.txt")
    yield os.path.join(os.getcwd(), "output", "entry.txt")


def write_entry():
    """Write LINE to the first writable candidate path.

    Each path is tried in order; an OSError on one path (missing
    directory, read-only mount, permission) is caught per path and
    the next candidate is tried. Parent directories are created when
    needed. Permissions of existing folders/files are never changed.
    Returns the path written, or raises the last OSError if every
    candidate failed.
    """
    last_error = None
    for path in candidate_paths():
        try:
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(LINE)
            return path
        except OSError as error:
            last_error = error
    if last_error is not None:
        raise last_error
    raise OSError("no candidate output path available")


if __name__ == "__main__":
    write_entry()


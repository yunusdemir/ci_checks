import check50
import check50.internal
import re
import nbformat


@check50.check()
def exists():
    """Notebook "module 1.ipynb" exists"""
    check50.include("check_jupyter.py", "data")


# TODO: move this into check_jupyter.py
def get_test_ids(notebook_path):
    """
    Get all test ids from a notebook
    A test is marked by an nbgrader id with 'test_' as prefix
    """
    # Open and parse the notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    # Grab all test cells
    test_cells = []
    for cell in nb.cells:
        cell_id = cell.metadata.get("nbgrader", {}).get("grade_id", "")

        if cell_id.startswith("test_"):
            test_cells.append(cell_id)

    return test_cells


def init():
    # Grab the last test id
    last_test_id = get_test_ids("module 1.ipynb")[-1]

    # Create a check running all cells up to last test id
    def check():
        check_jupyter = check50.internal.import_file("check_jupyter", "check_jupyter.py")
        cells = check_jupyter.cells_up_to("module 1.ipynb", last_test_id)
        check_jupyter.execute(cells)

    # Name and document the check
    check.__name__ = last_test_id
    check.__doc__ = f"All tests pass"

    # Register the check with check50
    check = check50.check(dependency=exists)(check)

    # Add the check to global module scope
    globals()[last_test_id] = check

init()

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
    # Keep track of dependencies
    last_check = exists

    for test_id in get_test_ids("module 1.ipynb"):
        def create_check(test_id):
            def check():
                check_jupyter = check50.internal.import_file("check_jupyter", "check_jupyter.py")
                cells = check_jupyter.cells_up_to("module 1.ipynb", test_id)
                check_jupyter.execute(cells)

            check.__name__ = test_id
            check.__doc__ = f"Test: {test_id} passes"
            return check

        # Create a new check
        check = create_check(test_id)

        # Register the check with check50
        check = check50.check(dependency=last_check)(check)

        # Keep track of dependencies
        last_check = check

        # Add the check to global module scope
        globals()[test_id] = check

init()

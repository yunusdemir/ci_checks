import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def execute_up_to(notebook_path, cell_id):
    # Open and parse the notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    # Grab all code cells up to cell_id
    cells = []
    for cell in nb.cells:
        if cell.cell_type == "code":
            cells.append(cell)

        if cell.metadata.get("nbgrader", {}).get("grade_id") == cell_id:
            break
    else:
        raise Exception(f"Cell with ID:{cell_id} not found.")

    # Start an ExecutePreprocessor: https://nbconvert.readthedocs.io/en/latest/execute_api.html
    # https://github.com/jupyter/nbconvert/blob/master/nbconvert/preprocessors/execute.py
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

    results = []

    # Start a Kernel Manager
    with ep.setup_preprocessor(None, {}):
        for index, cell in enumerate(cells):
            result = ep.preprocess_cell(cell, {}, index)
            results.append(result)

    return results


def output_from_cell(cell):
    output_data = cell[0]["outputs"][0]

    if output_data["output_type"] == "stream":
        return output_data["text"]

    if output_data["output_type"] == "display_data":
        return output_data["data"]["text/plain"]

    raise Exception("Unknown output format")


"""
nbgrader generate_assignment --CourseDirectory.source_directory=. --CourseDirectory.release_directory=release/. --assignment=.
"""

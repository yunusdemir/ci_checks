import check50
import check50.internal
import re

@check50.check()
def exists():
    """Notebook "module 1.ipynb" exists"""
    check50.include("check_jupyter.py", "data")

@check50.check(exists)
def test1():
    """Correcte antwoord bij vraag 1"""
    check_jupyter = check50.internal.import_file("check_jupyter", "check_jupyter.py")
    cells = check_jupyter.cells_up_to("module 1.ipynb", "vraag1")
    results = check_jupyter.execute(cells)
    output = check_jupyter.output_from_cell(results[-1])

    for type, val in [("sales", 39041), ("ads", 8702), ("subscriptions", 13200), ("donations", 292)]:
        regex = re.compile(f"({type}[\\s]*{val})", re.MULTILINE)
        if not re.search(regex, output):
            raise check50.Failure(f"Did not find {type} {val} in output:\n{output}")

@check50.check(exists)
def test2():
    """Correcte antwoord bij vraag 2"""
    check_jupyter = check50.internal.import_file("check_jupyter", "check_jupyter.py")
    cells = check_jupyter.cells_up_to("module 1.ipynb", "vraag2")
    results = check_jupyter.execute(cells)
    output = check_jupyter.output_from_cell(results[-1])

    answer = 28938
    regex = re.compile(str(answer), re.MULTILINE)
    if not re.search(regex, output):
        raise check50.Failure(f"Did not find {answer} in output:\n{output}")

@check50.check(exists)
def test3():
    """Check of een variabele (a) de waarde 'b' bevat"""
    # TODO remove (just import check_jupyter)
    check_jupyter = check50.internal.import_file("check_jupyter", "check_jupyter.py")

    # Grab all cells upto vraag2
    cells = check_jupyter.cells_up_to("module 1.ipynb", "vraag2")

    # Create a cell to perform an assertion
    check_cell = check_jupyter.create_cell("assert a == 'b'")

    # Execute all cells + our assertion
    with check_jupyter.executor() as execute:
        execute(cells)
        result_cell = execute(check_cell)

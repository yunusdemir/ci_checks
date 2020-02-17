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
    results = check_jupyter.execute_up_to("module 1.ipynb", "vraag1")
    output = check_jupyter.output_from_cell(results[-1])

    for type, val in [("sales", 39041), ("ads", 8702), ("subscriptions", 13200), ("donations", 292)]:
        regex = re.compile(f"({type}[\\s]*{val})", re.MULTILINE)
        if not re.search(regex, output):
            raise check50.Failure(f"Did not find {type} {val} in output:\n{output}")


@check50.check(exists)
def test2():
    """Correcte antwoord bij vraag 2"""
    check_jupyter = check50.internal.import_file("check_jupyter", "check_jupyter.py")
    results = check_jupyter.execute_up_to("module 1.ipynb", "vraag2")
    output = check_jupyter.output_from_cell(results[-1])

    answer = 28938
    regex = re.compile(str(answer), re.MULTILINE)
    if not re.search(regex, output):
        raise check50.Failure("Did not find {answer} in output:\n{output")

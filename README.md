# How to write CI assignments/checks

First:

```
pip install jupyter
pip install pandas
pip install nbgrader
```

Then install nbgrader notebook plugins:

```
jupyter nbextension install --user --py nbgrader --overwrite
jupyter nbextension enable --user --py nbgrader
jupyter serverextension enable --user --py nbgrader
```

Create the assignment as normal by creating a notebook and through using the nbgrader plugin. Remember to lock the cells you don't want students to change by marking them as read-only. Mark every cell that students write in as an "Autograded answer" and give those cells a recognizable ID. check50 can then look for these IDs.

You can make use of the nbgrader feature to hide solutions by surrounding these with `### BEGIN SOLUTION` and `### END SOLUTION`. Just remember to run the command below to generate the student version without the solutions:

```
nbgrader generate_assignment --CourseDirectory.source_directory=. --CourseDirectory.release_directory=release/. --assignment=.
```

This will take the assignment in the current directory and generate the student version in a folder called ```release```. You do not need to setup an nbgrader environment! :)

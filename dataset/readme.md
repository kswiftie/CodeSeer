# About dataset

The dataset contains solutions for problems with leetcode.

### Dataset structure

```
dataset/
├── name_of_the_task/
│   ├── original/
│   │   └── main.py
│   ├── non-plagiarized/
│   │   ├── 01.py
│   │   ├── 02.py
│   │   └── 03.py
│   └── plagiarized/
│       └── main.py
```

- original/main.py a solution with leetcode for this task.
- plagiarized/main.py a solution rewritten from original/main.py.
- non-plagiarized/01(or 02/03).py other solutions with leetcode for this task.

### How the plagiarized solution was created
#### The following criteria were met for this purpose:
1. Inserting and/or deleting spaces and comments
2. Renaming identifiers (for example, variables)
3. Changing the order of instructions
4. Replacing controls (for example, for, while, if)
5. Inserting insignificant code (code that does not affect the functionality of the program, but is noticeable and may well distract attention from the fact that it is plagiarism, including useless imports).
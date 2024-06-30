# File Selector for LLM Context Generation

## Overview

This tool is a command-line utility that provides an ncurses-based interface for navigating directories, selecting files, and generating formatted output. It was specifically created to ease the process of generating context for code-based tasks in Large Language Model (LLM) User Interfaces.

## Features

- Ncurses-based two-panel interface similar to Midnight Commander
- Directory navigation with sorted file listings (folders first)
- File selection and deselection
- Generation of formatted output containing file paths and contents
- Ability to copy selected file contents to clipboard

## Requirements

- Python 3.x
- ncurses library (usually comes pre-installed with Python)
- xclip (for clipboard functionality on Linux systems)

On Debian-based systems, you can install xclip with:

```
sudo apt-get install xclip
```

## Usage

1. Clone the repository:
```
git clone https://github.com/mkeyran/llm_context_selector.git
cd file-selector-llm-context
```

2. Run the script:
```
python file_selector.py
```

3. Use the following controls:
- Up/Down arrows: Navigate through files and directories
- Page Up/Page Down: Move cursor by one page up or down
- Enter: 
  - For directories: Enter the directory
  - For files: Toggle selection (select if not selected, deselect if already selected)
  - For "..": Go to parent directory
- 'g': Generate output file
- 'c': Copy selected files' contents to clipboard
- 'q': Quit the program

4. After selecting files, press 'g' to generate an output file or 'c' to copy the formatted content to your clipboard.

## Output Format

The generated output (both file and clipboard) will have the following format:

```
#<File1 Path>
<File1 Contents>
---

#<File2 Path>
<File2 Contents>
...
```

This format is designed to be easily parsed and used as context for code-based tasks in LLM UIs.

## Use Case for LLM Context Generation

When working with Large Language Models for code-related tasks, it's often necessary to provide context about multiple files or parts of a project. This tool simplifies the process of selecting relevant files and formatting their contents in a way that can be easily input into an LLM UI.

By using this tool, you can quickly navigate your project structure, select the files that are relevant to your task, and generate a formatted output that includes both file paths and contents. This formatted output can then be pasted directly into the LLM UI, providing the model with the necessary context to assist with your code-related queries or tasks.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/mkeyran/llm_context_selector/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
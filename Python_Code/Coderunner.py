import subprocess

# List of Python files to run in serial
file_paths = [
    r"Python_Code\\PyqSorter.py",
    r"Python_Code\\Notes_summariser.py",
    r"Python_Code\\Notes_summariser.py",
    r"Python_Code\summarizer_for_GPT.py",
    r"Python_Code\\Notes_Analyser.py"
    ]

# Run the files in serial
for file_path in file_paths:
    subprocess.run(["python", file_path])

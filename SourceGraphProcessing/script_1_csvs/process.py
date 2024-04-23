import os

files_in_dir = [f for f in os.listdir("script_1_csvs") if ".csv" in f]

for file in files_in_dir:
    write_file = open(f"processed/{file}", "w", encoding="utf-8", errors='ignore')
    files = []
    with open(f"{file}", "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "-/blob/" in line:
                line = line.replace("(https://sourcegraph.com/", "")
                line = line.replace(")", "")
                line = line.replace("-/blob/", "")
                write_file.write(line)
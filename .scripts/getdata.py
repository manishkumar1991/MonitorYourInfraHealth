import sys

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    print(f"Content of {file_path}:\n{content}")

if __name__ == "__main__":
    file_path = sys.argv[1]
    read_file(file_path)

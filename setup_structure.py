import os

def create_structure():
    # Define the directory structure
    directories = [
        "ml_auditor/checkers",
        "ml_auditor/llm",
        "tests/sample_notebooks",
        ".github/workflows"
    ]
    
    # Create directories
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

    # Create __init__.py files for packages
    init_paths = [
        "ml_auditor/__init__.py",
        "ml_auditor/checkers/__init__.py",
        "ml_auditor/llm/__init__.py"
    ]
    
    for file_path in init_paths:
        with open(file_path, 'w') as f:
            f.write("# This file makes the directory a Python package\n")
        print(f"Created file: {file_path}")

    # Create .env file
    with open(".env", 'w') as f:
        f.write("OPENAI_API_KEY=your_key_here\n")
    print("Created .env file")

    print("\nProject structure created successfully!")

if __name__ == "__main__":
    create_structure()
    
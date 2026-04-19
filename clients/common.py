from pathlib import Path

def create_incremental_file(file_name):
    path = Path(file_name)
    if not path.exists():
        path.touch()
        return path

    # If exists, start incrementing
    stem = path.stem
    suffix = path.suffix
    counter = 1

    while path.exists():
        path = path.with_name(f"{stem}_{counter}{suffix}")
        counter += 1

    path.touch()
    return path

def open_prompt_file(file_path='./prompts/prompt1.md'):
    return Path(file_path).read_text(encoding='utf-8')

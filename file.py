def create_file(name):
    """Create a file if it doesn't exist"""
    open(name, "w")


def append_to_file(name, content):
    """Append a line to a file"""
    with open(name, "a") as file:
        file.write(content + "\n")


def clear_file(name):
    """Reset a file"""
    with open(name, "w") as file:
        file.write("")

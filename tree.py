import os
import sys

def display_directory_tree(start_path, show_hidden=False, indent=''):
    if not os.path.isdir(start_path):
        print(f"Error: '{start_path}' is not a valid directory.")
        return

    html_output = ""
    if indent == '':
        html_output += f"{indent}<strong>{os.path.basename(start_path)}/</strong><br>"

    with os.scandir(start_path) as entries:
        entries = sorted(entries, key=lambda entry: entry.name.lower())  # Sort entries alphabetically

        for index, entry in enumerate(entries):
            if entry.name.startswith('.') and not show_hidden:
                continue  # Skip hidden folders and files if not requested

            is_last = index == len(entries) - 1
            branch = '└── ' if is_last else '├── '
            sub_indent = '    ' if is_last else '│   '

            if entry.is_dir():
                html_output += f"{indent}{branch}<strong>{entry.name}/</strong><br>"
                sub_path = os.path.join(start_path, entry.name)
                html_output += display_directory_tree(sub_path, show_hidden, indent + sub_indent)
            elif entry.is_file():
                file_path = os.path.join(start_path, entry.name)
                html_output += f"{indent}{branch}<a href='{file_path}' target='_blank'>{entry.name}</a><br>"

    return html_output


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python tree.py [--show-hidden] <directory_path>")
    else:
        directory_path = sys.argv[-1]
        show_hidden = '--show-hidden' in sys.argv

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Directory Tree</title>
            <style>
                body {{
                    font-family: monospace;
                    white-space: pre;
                }}
            </style>
        </head>
        <body>{display_directory_tree(directory_path, show_hidden)}</body>
        </html>
        """

        print(html)

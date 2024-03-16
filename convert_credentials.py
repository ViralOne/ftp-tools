import os
import json

def parse_file_entries(file_path):
    entries = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        entry = {}
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith('ftp://'):
                if entry:
                    entries.append(entry)
                    entry = {}
                entry['host'] = line[6:]
            elif line.startswith('Username'):
                entry['username'] = lines[i + 1].strip()
            elif line.startswith('Password'):
                entry['password'] = lines[i + 1].strip()
        if entry:
            entries.append(entry)
    return entries

def load_existing_entries(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return []

def export_entries(entries):
    export_string = ""
    for index, entry in enumerate(entries):
        export_string += json.dumps(entry)
        if index < len(entries) - 1:
            export_string += ",\n"
    return export_string

def update_ftp_servers(file_path, new_entries):
    existing_entries = load_existing_entries(file_path)
    updated_entries = existing_entries + new_entries
    unique_entries = []
    seen = set()
    for entry in updated_entries:
        entry_key = (entry['host'], entry['username'], entry['password'])
        if entry_key not in seen:
            unique_entries.append(entry)
            seen.add(entry_key)
    with open(file_path, 'w') as file:
        file.write("[\n")
        file.write(export_entries(unique_entries))
        file.write("\n]")

if __name__ == "__main__":
    file_path = "credentials.txt"  # Path to the file containing FTP entries
    new_entries = parse_file_entries(file_path)
    update_ftp_servers("servers.json", new_entries)

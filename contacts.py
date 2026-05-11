from jinja2 import Environment, FileSystemLoader
from pathlib import Path

page = {
    "title": "Contact Directory",
    "header": "Anaesthetist Contact List",
    "footer": "Last Updated May 2026",
}

contacts_file = "contacts.txt"
template_file = "contacts_template.html"
output_file = "contacts.html"


def parse_contacts(text):
    text = text.replace("\r\n", "\n")
    contacts = []
    for block in text.strip().split("\n\n"):
        contact = {}
        for line in block.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                contact[key.strip().lower()] = value.strip()
        if contact:
            contacts.append(contact)
    return contacts


def main():
    raw_text = Path(contacts_file).read_text()
    contacts = parse_contacts(raw_text)

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_file)
    output = template.render(page=page, contacts=contacts)

    Path(output_file).write_text(output)
    print(f"HTML file created: {output_file}")


if __name__ == "__main__":
    main()

import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Define the paths
yaml_file = "contacts.yaml"
template_dir = "templates"
template_file = "contacts_template.html"
output_file = "contacts.html"

# Ensure the template directory exists
Path(template_dir).mkdir(exist_ok=True)

# Load the YAML data
with open(yaml_file, "r") as file:
    data = yaml.safe_load(file)

# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader(template_dir))

# Create the template file if it doesn't exist
template_path = Path(template_dir) / template_file

# Get the template
template = env.get_template(template_file)

# Render the template with the data
output = template.render(page=data["page"], contacts=data["contacts"])

# Write the output to a file
with open(output_file, "w") as file:
    file.write(output)

print(f"HTML file created: {output_file}")

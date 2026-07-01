import os

from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# ") or line.startswith("#\t"):
            return line[2:]
    raise Exception("No h1 header found.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from %s to %s using %s", from_path, dest_path, template_path)
    with open(from_path) as f:
        md = f.read()
    f.close()

    with open(template_path) as g:
        tmp = g.read()
    g.close()

    new_node = markdown_to_html_node(md)
    html_str = new_node.to_html()

    title = extract_title(md)

    tmp = tmp.replace("{{ Title }}", title)
    tmp = tmp.replace("{{ Content }}", html_str)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    new_file = open(dest_path, "w")
    new_file.write(tmp)
    new_file.close()

def generate_pages_recursive(content_dir, template_path, public_dir):
    for item in os.listdir(content_dir):
        source_path = os.path.join(content_dir, item)
        dest_path = os.path.join(public_dir, item)

        if os.path.isdir(source_path):
            generate_pages_recursive(source_path, template_path, dest_path)

        elif source_path.endswith(".md"):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(source_path, template_path, dest_path)
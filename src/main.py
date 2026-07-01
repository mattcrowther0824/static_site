import sys

from copystatic import copy_files_recursive, clear_dest_dir
from gencontent import generate_page, generate_pages_recursive
from textnode import TextNode, TextType


def main():
    if len(sys.argv) > 1:
      basepath = sys.argv[1]
    else:
      basepath = "/"
    clear_dest_dir("./public")
    copy_files_recursive("./static", "./public")

    generate_pages_recursive("content", "template.html", "./docs", basepath)

main()
from enum import Enum

from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
  PARAGRAPH = 1
  HEADING = 2
  CODE = 3
  QUOTE = 4
  UNORDERED_LIST = 5
  ORDERED_LIST = 6

def markdown_to_blocks(markdown):
  blocks = markdown.split('\n\n')
  filtered_blocks = []
  for block in blocks:
    block = block.strip()
    if block != "":
      filtered_blocks.append(block)
  return filtered_blocks

def block_to_block_type(block):
  lines = block.split("\n")
  i = 1
  if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
    return BlockType.HEADING
  if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
    if len(lines) >= 3:
      return BlockType.CODE
  if block.startswith(">"):
    for line in lines:
      if not line.startswith(">"):
        return BlockType.PARAGRAPH
    return BlockType.QUOTE
  if block.startswith(("- ", "* ", "+ ")):
    for line in lines:
      if not line.startswith(("- ", "* ", "+ ")):
        return BlockType.PARAGRAPH
    return BlockType.UNORDERED_LIST
  if block.startswith(f"{i}. "):
    for line in lines:
      if not line.startswith(f"{i}. "):
        return BlockType.PARAGRAPH
      i += 1
    return BlockType.ORDERED_LIST
  return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
  html_nodes = []
  blocks = markdown_to_blocks(markdown)
  for block in blocks:
    block_type = block_to_block_type(block)
    match (block_type):
      case BlockType.PARAGRAPH:
        lines = block.split("\n")
        text = " ".join(lines)
        children = text_to_children(text)
        html_nodes.append(ParentNode("p", children))
      case BlockType.HEADING:
        level = 0
        for char in block:
          if char == "#":
            level += 1
          else:
            break
        if level + 1 >= len(block):
          raise ValueError(f"invalid heading level: {level}")
        text = block[level + 1 :]
        children = text_to_children(text)
        html_nodes.append(ParentNode(f"h{level}", children))
      case BlockType.CODE:
        if not block.startswith("```") or not block.endswith("```"):
          raise ValueError("invalid code block")
        text = block[4:-3]
        text_node = TextNode(text, TextType.TEXT)
        child = text_node_to_html_node(text_node)
        code = ParentNode("code", [child])
        html_nodes.append(ParentNode("pre", [code])) 
      case BlockType.QUOTE:
        lines = block.split("\n")
        new_lines = []
        for line in lines:
          if not line.startswith(">"):
            raise ValueError("invalid quote block")
          new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        html_nodes.append(ParentNode("blockquote", children))
      case BlockType.UNORDERED_LIST:
        items = block.split("\n")
        html_items = []
        for item in items:
          text = item[2:]
          children = text_to_children(text)
          html_items.append(ParentNode("li", children))
        html_nodes.append(ParentNode("ul", html_items))
      case BlockType.ORDERED_LIST:
        items = block.split("\n")
        html_items = []
        for item in items:
          parts = item.split(". ", 1)
          text = parts[1]
          children = text_to_children(text)
          html_items.append(ParentNode("li", children))
        html_nodes.append(ParentNode("ol", html_items))
  return ParentNode("div", html_nodes)

def text_to_children(text):
  text_nodes = text_to_textnodes(text)
  children = []
  for text_node in text_nodes:
    html_node = text_node_to_html_node(text_node)
    children.append(html_node)
  return children
import unittest

from htmlnode import LeafNode, HTMLNode, ParentNode


class TestHTMLNode(unittest.TestCase):
  def test_props_none(self):
    node = HTMLNode(props=None)
    self.assertEqual(node.props_to_html(), "")

  def test_props_empty(self):
    node = HTMLNode(props={})
    self.assertEqual(node.props_to_html(), "")

  def test_props_single(self):
    node = HTMLNode(props={"href": "https://www.boot.dev"})
    self.assertTrue(len([key for key in node.props]) == 1)

  def test_props_multi(self):
    node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
    self.assertTrue(len([key for key in node.props]) > 1)

  def test_to_html(self):
    node = HTMLNode()
    with self.assertRaises(NotImplementedError):
      node.to_html()

  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_props(self):
    node = LeafNode("a", "OK", {"href": "https://www.boot.dev"})
    self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">OK</a>')

  def test_leaf_no_tag(self):
    node = LeafNode(None, "https://www.boot.dev")
    self.assertEqual(node.to_html(), "https://www.boot.dev")

  def test_leaf_no_value(self):
    node = LeafNode(None, None)
    with self.assertRaises(ValueError):
      node.to_html()

  def test_leaf_repr(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.__repr__(), "p Hello, world! None")

  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

  def test_parent_no_children(self):
    node = ParentNode("p", None)
    with self.assertRaises(ValueError):
      node.to_html()

  def test_parent_no_tag(self):
    node = ParentNode(None, "child")
    with self.assertRaises(ValueError):
      node.to_html()

  def test_parent_empty_childten(self):
    node = ParentNode("div", [])
    self.assertEqual(node.to_html(), "<div></div>")

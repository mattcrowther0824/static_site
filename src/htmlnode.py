class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError()

  def props_to_html(self):
    if self.props == None:
      return ""

    prop_string = ""
    for k, v in self.props.items():
      prop_string += f' {k}="{self.props[k]}"'
    return prop_string

  def __repr__(self):
    return f"{self.tag} {self.value} {self.children} {self.props}"

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      print("BAD LEAF:", self)
      raise ValueError("invalid HTML: no value")
    # if not self.value:
    #   raise ValueError()
    if not self.tag:
      return f"{self.value}"
    return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

  def __repr__(self):
    return f"{self.tag} {self.value} {self.props}"

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag == None:
      raise ValueError("Missing tag(s)")
    if self.children == None:
      raise ValueError("Missing child(ren) value(s)")
    children_string = ""
    for child in self.children:
      children_string += child.to_html()
    return f"<{self.tag}>{children_string}</{self.tag}>"

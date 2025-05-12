class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props



    def to_html(self):
        raise NotImplementedError("Override this funcion inside HTMLNode's children.")



    def props_to_html(self):
        text = ""

        if self.props == None: return ""

        for key, value in self.props.items():
                text += f' {key}="{value}"'

        return text



    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props_to_html()}, {self.children})"





class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    # Override
    def to_html(self):
        if self.value == None or self.value == '':
            raise ValueError("LeafNode has to have a value.")
        
        if self.tag == None:
            return self.value

        text = ""
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

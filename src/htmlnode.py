

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props



    def to_html(self):
        raise NotImplementedError("Override this funcion inside HTMLNode's children")



    def props_to_html(self):
        text = ""

        if len(self.props) == 0: return ""

        for key, value in self.props.items():
                text += f'{key}="{value}" '

        return text.rstrip()



    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props_to_html()}, {self.children})"


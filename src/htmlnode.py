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
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props and self.children == other.children





class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    # Override
    def to_html(self):
        if self.value == None:# or self.value == '':
            self.value=''
            #raise ValueError("LeafNode has to have a value.")
        
        if self.tag == None or self.tag == '':
            return self.value
        
        out = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return out
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value})"





class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    # Override
    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode has to have a tag.")

        if self.children == None or len(self.children) == 0:
            raise ValueError("ParentNode has to have at leat one child.")

        children_val = ""
        for child in self.children:
            #if (child.value == None or child.value == '') and (child.tag == None or child.tag == ''):
            children_val += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_val}</{self.tag}>"
    

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children})"

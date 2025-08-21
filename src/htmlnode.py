class HTMLNode:
    def __init__(
        self,
        tag: str = "",
        value: str = "",
        childen: list["HTMLNode"] = [],
        props: dict[str, str] = {},
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = childen
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        html = ""

        if self.props is not None:
            for key in self.props:
                html += f' {key}="{self.props[key]}"'

        return html

    def tag_to_html(self, close: bool = False) -> str:
        html = ""

        if self.tag != "":
            if close:
                html = f"</{self.tag}>"
            else:
                html = f"<{self.tag}{self.props_to_html()}>"

        # print(f'\nTag: {self.tag}\nClose: {close}\nHTML: {html}')

        return html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = {}) -> None:
        if value is None:
            raise ValueError("Value can't be None")

        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError(self)
        if self.tag is None:
            return self.value

        return f"{self.tag_to_html()}{self.value}{self.tag_to_html(True)}"


class ImageLeafNode(LeafNode):
    def __init__(self, props: dict[str, str] = {}) -> None:
        super().__init__("img", "", props)

    def to_html(self):
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}/>"


class YoutubeLeafNode(LeafNode):
    def __init__(self, props: dict[str, str] = {}) -> None:
        super().__init__("iframe", "", props)

    def to_html(self):
        if self.tag is None:
            return self.value

        if "src" in self.props:
            link_id = self.props["src"].replace("watch?v=", "embed/")
            self.props["src"] = link_id

        return f"<iframe{self.props_to_html()} allowfullscreen></iframe>"


class HorizontalLineLeafNode(LeafNode):
    def __init__(self) -> None:
        super().__init__(value="\0", tag="hr")

    def to_html(self):
        return "<hr>"

class PassthroughLeafNode(LeafNode):
    def __init__(self, value: str) -> None:
        super().__init__('', value, {})

    def to_html(self):
        return self.value

class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, childen: list[HTMLNode], props: dict[str, str] = {}
    ) -> None:
        super().__init__(tag, "", childen, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node missing tag")
        if self.children is None:
            raise ValueError("Parent node's children list is None'")

        html = self.tag_to_html()
        for child in self.children:
            html += child.to_html()
        html += self.tag_to_html(True)

        # print(f"\n{self}\nHTML: {html}")

        return html

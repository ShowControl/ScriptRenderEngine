"""Render Engine, takes a populated structure and displays it."""
__author__ = 'bapril'
__version__ = '0.0.4'
import Tkinter as tk
import tkFont

class ScriptRenderEngine(object):
    """Render Engine Class"""
    def __init__(self, target, source):
        """Takes a target (Text) and source (Parse Engine)"""
        self.source = source
        self.target = target
        self.input = ""
        self.tag = None

        self.setup_styles()

        self.tag_map = {}
        self.load_tag_map()

    def setup_styles(self):
        """Establish the apporpriate style elements"""
        self.style_title_font = tkFont.Font(family="Helvetica", size=24, weight=tkFont.BOLD)
        self.style_copyright_font = tkFont.Font(family="Helvetica", size=12, slant=tkFont.ITALIC)
        self.style_subtitle_font = tkFont.Font(family="Helvetica", size=20, weight=tkFont.BOLD)
        self.style_page_font = tkFont.Font(family="Helvetica", size=8, weight=tkFont.BOLD)

        self.target.tag_configure("copyright", font=self.style_copyright_font)
        self.target.tag_configure("title", justify='center', font=self.style_title_font)
        self.target.tag_configure("subtitle", justify='center', font=self.style_subtitle_font)
        self.target.tag_configure("page", justify='right', font=self.style_page_font)

    def load_tag_map(self):
        """Create a map that maps tags to render fucntions"""
        self.tag_map['title'] = self.render_tk_title
        self.tag_map['subtitle'] = self.render_tk_subtitle
        self.tag_map['copyright'] = self.render_tk_copyright
        self.tag_map['page'] = self.render_tk_page

    def render_tk_title(self):
        """Generate a title"""
        self.render_tk_style(self.tag['text']+"\n", "title")

    def render_tk_subtitle(self):
        """Generate a subtitle"""
        self.render_tk_style(self.tag['text']+"\n", "subtitle")

    def render_tk_copyright(self):
        """Generate a copyright"""
        self.render_tk_style(self.tag['text']+"\n", "copyright")

    def render_tk_page(self):
        """Tag a page"""
        self.render_tk_style(self.tag['text']+"\n", "page")

    def render_tk_style(self, text, style):
        """Generic Style application function"""
        begin = self.target.index(tk.INSERT)
        self.target.insert(tk.END, text)
        end = self.target.index(tk.INSERT)
        self.target.tag_add(style, begin, end)

    def update(self):
        """generate the output"""
        #TODO Reflection on source and target should drive action.
        #erase what we have there
        self.input = self.source.update()
        self.target.config(state=tk.NORMAL)
        self.target.delete('1.0', tk.END)
        self.render_to_tk_text()
        self.target.config(state=tk.DISABLED)

    def render_to_tk_text(self):
        """Update a Text Entity"""
        for tag in self.input:
            self.tag = tag
            if 'name' in tag.keys():
                self.render_tag()
            else:
                self.target.insert(tk.END, tag['text'])

    def render_tag(self):
        """Render a tag"""
        self.tag_map[self.tag['name']]()

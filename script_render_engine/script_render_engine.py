__author__ = 'bapril'
__version__ = '0.0.4'
import Tkinter as tk
import tkFont
import re

class ScriptRenderEngine(object):
    def __init__(self,target,source):
        self.source = source
        self.target = target
        self.input = ""

        self.setup_styles()

        self.tag_map={}
        self.load_tag_map()

    def setup_styles(self):
        self.style_title_font = tkFont.Font(family="Helvetica", size=24, weight=tkFont.BOLD)
        self.style_copyright_font = tkFont.Font(family="Helvetica", size=12, slant=tkFont.ITALIC)
        self.style_subtitle_font = tkFont.Font(family="Helvetica", size=20, weight=tkFont.BOLD)

        self.target.tag_configure("copyright", font=self.style_copyright_font)
        self.target.tag_configure("title", justify='center', font=self.style_title_font)
        self.target.tag_configure("subtitle", justify='center', font=self.style_subtitle_font)

    def load_tag_map(self):
        self.tag_map['title'] = self.render_tk_title
        self.tag_map['subtitle'] = self.render_tk_subtitle
        self.tag_map['copyright'] = self.render_tk_copyright

    def render_tk_title(self):
        self.render_tk_style(self.tag['text']+"\n","title")

    def render_tk_subtitle(self):
        self.render_tk_style(self.tag['text']+"\n","subtitle")

    def render_tk_copyright(self):
        self.render_tk_style(self.tag['text']+"\n","copyright")

    def render_tk_style(self,text,style):
        begin = self.target.index(tk.INSERT)
        self.target.insert(tk.END,text)
        end = self.target.index(tk.INSERT)
        self.target.tag_add(style, begin, end)

    def update(self):
        #TODO Reflection on source and target should drive action.
        #erase what we have there
        self.input = self.source.update()
        self.target.config(state=tk.NORMAL)
        self.target.delete('1.0', tk.END)
        self.render_to_tk_text()
        self.target.config(state=tk.DISABLED)

    def render_to_tk_text(self):
        for tag in self.input:
            self.tag = tag
            if 'name' in tag.keys():
                self.render_tag()
            else:
                self.target.insert(tk.END,tag['text'])

    def render_tag(self):
        self.tag_map[self.tag['name']]()

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
        style_title_font = tkFont.Font(family="Helvetica", size=24, weight=tkFont.BOLD)
        style_copyright_font = tkFont.Font(family="Helvetica", size=12, slant=tkFont.ITALIC)
        style_subtitle_font = tkFont.Font(family="Helvetica", size=20, weight=tkFont.BOLD)
        style_page_font = tkFont.Font(family="Helvetica", size=8, weight=tkFont.BOLD)
        style_dp_char_font = tkFont.Font(family="Helvetica", size=12, weight=tkFont.BOLD)
        style_dp_descr_font = tkFont.Font(family="Helvetica", size=12)

        self.target.tag_configure("copyright", font=style_copyright_font)
        self.target.tag_configure("title", justify='center', font=style_title_font)
        self.target.tag_configure("subtitle", justify='center', font=style_subtitle_font)
        self.target.tag_configure("page", justify='right', font=style_page_font)
        self.target.tag_configure("invalid", justify='left', background="red", foreground="yellow")
        self.target.tag_configure("dp_char", justify='left', \
            font=style_dp_char_font, background="black", foreground="white")
        self.target.tag_configure("dp_descr", justify='left', \
            font=style_dp_descr_font, background="white", foreground="black")
        self.target.tag_configure("location", justify='center', font=style_copyright_font)
        self.target.tag_configure("enter", background="green", foreground="white")
        self.target.tag_configure("exit", background="red", foreground="white")
        self.target.tag_configure("act", justify='center', font=style_title_font)
        self.target.tag_configure("scene", justify='center', font=style_subtitle_font)

    def load_tag_map(self):
        """Create a map that maps tags to render fucntions"""
        self.tag_map['title'] = self.render_tk_title
        self.tag_map['subtitle'] = self.render_tk_subtitle
        self.tag_map['copyright'] = self.render_tk_copyright
        self.tag_map['page'] = self.render_tk_page
        self.tag_map['author'] = self.render_tk_author
        self.tag_map['invalid'] = self.render_tk_invalid
        self.tag_map['dp'] = self.render_dp
        self.tag_map['location'] = self.render_location
        self.tag_map['char'] = self.render_char
        self.tag_map['enter'] = self.render_enter
        self.tag_map['exit'] = self.render_exit
        self.tag_map['exeunt'] = self.render_exeunt
        self.tag_map['sd'] = self.render_location
        self.tag_map['act'] = self.render_act
        self.tag_map['scene'] = self.render_scene

    def render_act(self):
        """Render ACT"""
        self.render_tk_style("Act "+self.tag['text'], "act")

    def render_scene(self):
        """Render Scene"""
        self.render_tk_style("Scene "+self.tag['text'], "scene")

    def render_exeunt(self):
        """Render Exeunit (all cast exit)"""
        self.render_tk_style("All Exit", "exit")

    def render_enter(self):
        """Generate an enter tag"""
        self.render_tk_style("Enter: "+self.tag['text'], "enter")

    def render_exit(self):
        """Generate an exit tag"""
        self.render_tk_style("Exit: "+self.tag['text'], "exit")

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

    def render_tk_author(self):
        """Parse an Author JSON tag and render it"""
        if self.tag['role'] == 'author':
            self.render_tk_style("By: "+self.tag['name']+"\n", "subtitle")
        else:
            self.render_tk_style(self.tag['role']+" by: "+self.tag['name']+"\n", "subtitle")

    def render_dp(self):
        """Render a Dramatis Personae Entry """
        self.render_tk_style(self.tag['name'], "dp_char")
        self.render_tk_style(" - "+self.tag['description'], "dp_descr")

    def render_location(self):
        """Render a setting tag"""
        self.render_tk_style("["+self.tag['text']+"]", "copyright")

    def render_char(self):
        """Render the start of dialog tag for a character"""
        self.target.insert(tk.END, "                    ")
        self.render_tk_style(" "+self.tag['text']+" ", "dp_char")

    def render_tk_invalid(self):
        """Display an entry for an invalid tag"""
        self.render_tk_style("ERROR: "+self.tag['error']+ "("+self.tag['text']+")\n", "invalid")

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
            if 'type' in tag.keys():
                self.render_tag()
            else:
                self.target.insert(tk.END, tag['text'])

    def render_tag(self):
        """Render a tag"""
        try:
            self.tag_map[self.tag['type']]()
        except:
            tag_type = self.tag['type']
            text = str(self.tag)
            self.tag['type'] = "invalid"
            self.tag['text'] = text
            self.tag['error'] = "No Render engine for tag type:"+tag_type

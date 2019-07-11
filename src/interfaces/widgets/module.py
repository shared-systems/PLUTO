"""
 
    This module generate serveral combination frame based object.
 
"""

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt

from .frame import Frame
from .label import Label
from .layout import HorizontalLayout
from .lineedit import LineEdit
from .spacer import HorizontalSpacer

class BaseTwoLabelFrame(Frame):
  
    label_one : Label = None
    label_two : Label = None

    def __init__(self, widget, **kwargs):
        super(BaseTwoLabelFrame, self).__init__(widget, **kwargs)

        kwargs.pop('name', None)
        get_param = lambda x : kwargs.get(x)

        label_one_name = get_param("label_one_name")
        label_two_name = get_param("label_two_name")

        label_one_text = get_param("label_one_text")
        label_two_text = get_param("label_two_text")

        layout = HorizontalLayout(self)

        self.label_one = Label(self, name=label_one_name, **kwargs)
        self.set_label_one_text(label_one_text)
        layout.addWidget(self.label_one)

        spacer = HorizontalSpacer()
        layout.addItem(spacer)

        self.label_two = Label(self, name=label_two_name, **kwargs)
        self.set_label_two_text(label_two_text)
        layout.addWidget(self.label_two)

    def set_label_one_text(self, text:str):
        self.label_one.setText(text)
    
    def set_label_two_text(self, text:str):
        self.label_two.setText(text)
    
    def get_label_one(self):
        return self.label_one
    
    def get_label_two(self):
        return self.label_two


class SectionTitleFrame(BaseTwoLabelFrame):
    
    def __init__(self, widget, **kwargs):
        super(SectionTitleFrame, self).__init__(widget, align=Qt.AlignVCenter, **kwargs)

        get_param = lambda x : kwargs.get(x)




class ConfigFrame(BaseTwoLabelFrame):

    def __init__(self, widget, **kwargs):
        super(ConfigFrame, self).__init__(widget, width=200, l_m=11, r_m=11,
                                          align=Qt.AlignVCenter, **kwargs)


class BaseInputFrame(Frame):
  
    title       : Label = None
    input_field : QLineEdit = None

    def __init__(self, widget, **kwargs):

        super(BaseInputFrame, self).__init__(widget, **kwargs)

        # Lambda func grab input args
        get_num = lambda x : kwargs.get(x, 0)
        get_param = lambda x : kwargs.get(x)

        height = get_num("height")
        width = get_num("width")
        name = get_param("name")

        title_width = get_num("title_width")
        title = get_param("title")
        align = get_param("align")
        title_name = get_param("title_name")

        input_width = get_num("input_width")
        hint = get_param("hint")
        echo = get_param("echo")
        input_name = get_param("input_name")
        input_stylesheet = get_param("input_stylesheet")

        # set layout
        layout = HorizontalLayout(self, **kwargs)

        # title
        self.title = Label(self, height=height, width=title_width, 
                            text=title, align=align, name=title_name)
        layout.addWidget(self.title)

        # input
        self.input_field = LineEdit(self, height=height, width=input_width, 
                                    hint=hint, echo=echo, name=input_name, 
                                    stylesheet=input_stylesheet)
        layout.addWidget(self.input_field)

    def get_input(self):
        return self.input_field


class LoginInputFrame(BaseInputFrame):

    def __init__(self, widget, **kwargs):
        super(LoginInputFrame, self).__init__(widget, l_m=30, r_m=30, space=9, height=52,
                                            name="Login_input_box",
                                            title_name="Login_input_title",
                                            input_name="Login_input_input",
                                            **kwargs)

        # set default title width if not given
        get_num = lambda x : kwargs.get(x, 0)
        title_width = get_num("title_width")
        not title_width and self.title.setFixedWidth(160)


class TabsInputFrame(BaseInputFrame):

    def __init__(self, widget, **kwargs):
        super(TabsInputFrame, self).__init__(widget, height=30,
                                            title_name="Page_input_title",
                                            align=(Qt.AlignRight | Qt.AlignVCenter),
                                            **kwargs)

        # set default frame width if given
        get_num = lambda x : kwargs.get(x, 0)
        get_param = lambda x : kwargs.get(x)

        fix_width = get_param("fix_width")
        width = get_num("width")

        if fix_width is True:
            if not width:
                self.setFixedWidth(258)
            else:
                self.setFixedWidth(width)
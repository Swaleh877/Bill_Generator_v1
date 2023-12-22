from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang.builder import Builder
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivy.utils import platform
from math import ceil
from fpdf import FPDF
from kivy.core.window import Window

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"


class PDF(FPDF):
    def header(self):
        self.image("Letterhead_H.jpg", 10, 8, 192)
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.image("Letterhead_F.jpg", 10, self.get_y() - 15, 192)


def Create_pdf(data, billing_data, note, adv_tup,svr_chg_tup,tot_amount_tup):
    headers = ("S.No", "Room", "Product", "Hgt", "Wgt", "Qty", "Area", "Price")
    billing_data.insert(0,headers)
    billing_data.append(adv_tup)
    billing_data.append(svr_chg_tup)
    billing_data.append(tot_amount_tup)
    note_list = note.split("\n")
    pdf = PDF("P", "mm", "A4")
    pdf.t_margin = pdf.t_margin * 3.0
    pdf.font_size = 8
    pdf.set_auto_page_break(auto=True, margin=30)
    pdf.add_page()
    pdf.set_font("helvetica", "", 15)
    pdf.cell(140, 10, f"Customer Name: {data[0]}")
    pdf.cell(80, 10, f"Date: {data[2]}", ln=True)
    pdf.cell(120, 10, f"Customer Address/Building: {data[1]}", ln=True)
    pdf.set_font("helvetica", "", 10)
    line_height = pdf.font_size * 2.5
    for row in billing_data:
        for header,datum in zip(headers,row):
            if datum in headers:
                pdf.set_fill_color(52,235,235)
                fill_cell = True
            else:
                fill_cell = False
            if header == 'S.No' :
                pdf.cell(9, line_height, datum,border=1,ln=0,align='C',fill=fill_cell)
            elif header == 'Hgt' or header =='Wgt':
                pdf.cell(14, line_height, datum,border=1,ln=0,align='C',fill=fill_cell)
            elif  header == 'Qty':
                pdf.cell(11, line_height, datum,border=1,ln=0,align='C',fill=fill_cell) 
            elif header == 'Area' or header == 'Price':
                pdf.cell(25, line_height,datum,border=1,ln=0,align='C',fill=fill_cell)
            elif header == 'Product':
                pdf.cell(62, line_height, datum,border=1,ln=0,align='C',fill=fill_cell)
            elif header == 'Room':
                pdf.cell(35, line_height, datum,border=1,ln=0,align='C',fill=fill_cell)
        pdf.ln(line_height)
    pdf.set_font("helvetica", "", 15)
    pdf.cell(120, 10,"Note:", ln=True)
    for i in note_list:
        pdf.cell(140, 6, f'  {i}', ln=True)
    if platform == 'android':
        pdf.output(f"/storage/emulated/0/Download/{data[0]}_{data[2]}.pdf","F")
    else:
        pdf.output(f"C:\\Users\\Swaleh\\Downloads\\temp\\{data[0]}_{data[2]}.pdf","F")

helper = """
ScreenManager:
    InputScreen:
    TableScreen:

<InputScreen>:
    name: 'input'
    ScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            spacing: '50dp'
            padding: '20dp'
            adaptive_height: True
            MDTopAppBar:
                title: 'Bill APP'
            MDLabel:
                id: first_label
                text: 'Customer Information'
                theme_text_color: 'Custom'
                text_color: (52/255.0, 235/255.0, 235/255.0, 1)
                halign: 'center'
                adaptive_size: True
                allow_selection: True
            MDTextField:
                id: c_name
                hint_text: 'Enter Customer Name'
                helper_text: 'Name required'
                helper_text_mode: "on_error"
                icon_right: 'rename-box'
                on_focus: root.string_check()
                color_mode: 'custom'
                line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                pos_hint: {'center_x':0.5,'center_y':0.1}
                size_hint_x: None
                width: 800
            MDTextField:
                id: c_address
                hint_text: 'Enter Customer Address'
                helper_text: 'Address required'
                color_mode: 'custom'
                line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                helper_text_mode: "on_error"
                on_focus: root.string_check_add()
                icon_right: 'home'
                pos_hint: {'center_x':0.5,'center_y':0.1}
                size_hint_x: None
                width: 800
            MDTextField:
                id: set_date
                hint_text: 'Pick a Date'
                helper_text: 'Select correct date'
                helper_text_mode: 'on_error'
                color_mode: 'custom'
                line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                icon_right: 'calendar'
                write_tab: False
                searchable: False
                on_focus: root.setDate()
                pos_hint: {'center_x':0.5,'center_y':0.1}
                size_hint_x: None
                width: 800
            MDLabel:
                id: second_label
                text: 'Billing Information'
                theme_text_color: 'Custom'
                text_color: (52/255.0, 235/255.0, 235/255.0, 1)
                halign: 'center'
                adaptive_size: True
                allow_selection: True
            MDTextField:
                id: room
                hint_text: 'Enter Room'
                helper_text: 'required'
                helper_text_mode: 'on_error'
                color_mode: 'custom'
                line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                icon_right: 'room-service'
                pos_hint: {'center_x':0.5,'center_y':0.1}
                size_hint_x: None
                width: 800
            MDTextField:
                id: product_menu
                hint_text: 'Select a Product'
                helper_text: 'Please select a valid product'
                helper_text_mode: 'on_error'
                icon_right: 'apps-box'
                searchable: False
                color_mode: 'custom'
                line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                write_text: False
                on_focus: root.drpdown()
                pos_hint: {'center_x':0.5,'center_y':0.1}
                size_hint_x: None
                width: 800
            MDBoxLayout:
                orientation: 'horizontal'
                padding: ('21dp','10dp')
                spacing: '10dp'
                adaptive_height: True
                MDTextField:
                    id: height
                    hint_text: 'Enter height'
                    helper_text: 'please enter a number'
                    helper_text_mode: "on_error"
                    color_mode: 'custom'
                    line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                    icon_right: 'human-male-height'
                    pos_hint: {'center_x':0.5,'center_y':0.5}
                    size_hint_x: None
                    width: 400
                MDTextField:
                    id: unit_h
                    hint_text: 'Select a unit'
                    helper_text: 'Please make a valid selection'
                    helper_text_mode: 'on_error'
                    color_mode: 'custom'
                    line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                    icon_right: 'altimeter'
                    write_tab: False
                    on_focus: root.unitdrpdown()
                    pos_hint: {'center_x':0.5,'center_y':0.5}
                    size_hint_x: None
                    width: 400
            MDBoxLayout:
                orientation: 'horizontal'
                padding: ('21dp','10dp')
                spacing: '10dp'
                adaptive_size: True
                MDTextField:
                    id: width
                    hint_text: 'Enter width'
                    helper_text: 'please enter a number'
                    helper_text_mode: "on_error"
                    color_mode: 'custom'
                    line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                    icon_right: 'weight'
                    pos_hint: {'center_x':0.5,'center_y':0.5}
                    size_hint_x: None
                    width: 400
                MDTextField:
                    id: unit_w
                    hint_text: 'Select a unit'
                    helper_text: 'Please make a valid selection'
                    helper_text_mode: 'on_error'
                    color_mode: 'custom'
                    line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                    icon_right: 'altimeter'
                    write_tab: False
                    on_focus: root.unitdrpdown()
                    pos_hint: {'center_x':0.5,'center_y':0.5}
                    size_hint_x: None
                    width: 400
            MDTextField:
                id: quantity
                hint_text: 'Enter Quantity'
                helper_text: 'required/Please enter a number'
                helper_text_mode: "on_error"
                color_mode: 'custom'
                line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                icon_right: 'beaker'
                pos_hint: {'center_x':0.5,'center_y':0.1}
                size_hint_x: None
                width: 800
            MDTextField:
                id: Amt_per_feet
                hint_text: 'Enter Amount per Feet'
                helper_text: 'required/Please enter a number'
                helper_text_mode: "on_error"
                color_mode: 'custom'
                line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                icon_right: 'cash'
                pos_hint: {'center_x':0.5,'center_y':0.1}
                size_hint_x: None
                width: 800
            MDTextField:
                id: advance
                hint_text: 'Enter Advance amount'
                helper_text: 'required/Please enter a number'
                helper_text_mode: "on_error"
                color_mode: 'custom'
                line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                icon_right: 'cash-check'
                pos_hint: {'center_x':0.5,'center_y':0.1}
                size_hint_x: None
                width: 800
            MDTextField:
                id: FHT_charge
                hint_text: 'Enter Fitting/Handling Charge'
                helper_text: 'required/Please enter a number'
                helper_text_mode: "on_error"
                color_mode: 'custom'
                line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                icon_right: 'truck-delivery'
                pos_hint: {'center_x':0.5,'center_y':0.1}
                size_hint_x: None
                width: 800
            MDLabel:
                id: third_label
                text: 'Others'
                theme_text_color: 'Custom'
                text_color: (52/255.0, 235/255.0, 235/255.0, 1)
                halign: 'center'
                adaptive_size: True
                allow_selection: True
            MDTextField:
                id: note
                hint_text: 'Notes'
                color_mode: 'custom'
                multiline: True
                line_color_focus: (52/255.0, 235/255.0, 235/255.0, 1)
                icon_right: 'note'
                pos_hint: {'center_x':0.5,'center_y':0.1}
                size_hint_x: None
                width: 800
            MDBoxLayout:
                orientation: 'horizontal'
                spacing:'20dp'
                padding: ('30dp','5dp')
                MDRectangleFlatButton:
                    text: 'Preview'
                    on_press: root.manager.current = 'tabel'
                MDRectangleFlatButton:
                    text: 'Add Entry'
                    on_press: root.add_entry()
<TableScreen>:
    name:'tabel'
    MDBoxLayout:
        orientation: 'horizontal'
        padding: ('50dp','10dp')
        spacing: '10dp'
        adaptive_height: True
        MDRectangleFlatButton:
            text: 'Edit'
            on_press: root.edit_row()
            pos_hint: {'center_x':0.5,'center_y':0.5}
        MDRectangleFlatButton:
            text: 'Generate Bill'
            on_press:root.gen_bill()
            pos_hint: {'center_x':0.5,'center_y':0.5}
"""


class InputScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.cust_data = []
        self.billing_data = []
        self.extra_vals = []
        self.w_sr_no = 1
        self.d_sr_no = 1
        self.p_sr_no = 1

    def string_check(self):
        if self.manager.get_screen("input").ids.c_name.text == "":
            self.manager.get_screen("input").ids.c_name.error = True

    def string_check_add(self):
        if self.manager.get_screen("input").ids.c_address.text == "":
            self.manager.get_screen("input").ids.c_address.error = True

    def add_cust_data(self, name, addr, date, amt_per_feet):
        self.cust_data.append((name, addr, date, amt_per_feet))
        print(self.cust_data)

    def check_dups(self):
        temp_list = self.manager.get_screen("input").ids.room.text
        same_flg = 0
        idxex = 0
        if len(self.billing_data) != 0:
            for idx, old_values in enumerate(self.billing_data):
                print(temp_list == old_values[1])
                if temp_list == old_values[1]:
                    same_flg = 1
                    idxex = idx
        if same_flg == 1:
            height_feet, width_feet = self.convert_height_width(
                self.manager.get_screen("input").ids.height.text,
                self.manager.get_screen("input").ids.width.text,
            )
            if self.manager.get_screen("input").ids.product_menu.text in [
                "Mosquito Net",
                "Invisible Grill",
                "Sliding Windows",
                "UPVC Windows",
                "Aluminum Mosquito Net",
                "Openable Window",
                "Pegion Net",
            ]:
                sr_no = "W" + self.manager.get_screen("tabel").row[0][1:]
            elif self.manager.get_screen("input").ids.product_menu.text in [
                "Aluminum Door",
                "UPVC Door",
            ]:
                sr_no = "D" + self.manager.get_screen("tabel").row[0][1:]
            else:
                sr_no = "P" + self.manager.get_screen("tabel").row[0][1:]
            new_row = (
                sr_no,
                self.manager.get_screen("input").ids.room.text,
                self.manager.get_screen("input").ids.product_menu.text,
                str(height_feet),
                str(width_feet),
                self.manager.get_screen("input").ids.quantity.text,
                str(round((float(height_feet)
                            * float(width_feet)
                            * float(self.manager.get_screen("input").ids.quantity.text)
                        ),2,
                    )
                ),
                str(
                    round(
                        (
                            (
                                (
                                    float(height_feet)
                                    * float(width_feet)
                                    * float(
                                        self.manager.get_screen(
                                            "input"
                                        ).ids.quantity.text
                                    )
                                )
                                * float(
                                    self.manager.get_screen(
                                        "input"
                                    ).ids.Amt_per_feet.text
                                )
                            )
                            - float(self.manager.get_screen("input").ids.advance.text)
                        )
                        + float(self.manager.get_screen("input").ids.FHT_charge.text),
                        2,
                    ),
                ),
            )
            self.billing_data[idxex] = new_row
        return same_flg

    def convert_height_width(self, height, width):
        try:
            if self.manager.get_screen("input").ids.unit_h.text == "mm":
                return round(float(height) * 0.0032808399, 2), round(
                    float(width) * 0.0032808399, 2
                )
            elif self.manager.get_screen("input").ids.unit_h.text == "cm":
                return round(float(height) * 0.032808399, 2), round(
                    float(width) * 0.032808399, 2
                )
            elif self.manager.get_screen("input").ids.unit_h.text == "m":
                return round(float(height) * 3.280839895, 2), round(
                    float(width) * 3.280839895, 2
                )
            elif self.manager.get_screen("input").ids.unit_h.text == "inches":
                return round(float(height) / 12, 2), round(float(width) / 12, 2)
            elif self.manager.get_screen("input").ids.unit_h.text == "feet":
                return height, width
            else:
                ok_btn = MDFlatButton(text="OK", on_press=self.close_dialog)
                self.dialog = MDDialog(
                    title="Please select correct unit",
                    text="Please select correct unit if you have not select any please make at least one selection",
                    buttons=[ok_btn],
                )
                self.dialog.open()
        except:
            ok_btn = MDFlatButton(text="OK", on_press=self.close_dialog)
            self.dialog = MDDialog(
                title="Please enter correct height and width values",
                text="Please enter correct height/width values, The values should be decimal/integer",
                buttons=[ok_btn],
            )
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def add_entry(self):
        if (
            self.manager.get_screen("input").ids.c_name.text == ""
            or self.manager.get_screen("input").ids.c_address.text == ""
            or self.manager.get_screen("input").ids.set_date.text == ""
            or self.manager.get_screen("input").ids.room.text == ""
            or self.manager.get_screen("input").ids.product_menu.text == ""
            or self.manager.get_screen("input").ids.height.text == ""
            or self.manager.get_screen("input").ids.width.text == " "
            or self.manager.get_screen("input").ids.quantity.text == ""
            or self.manager.get_screen("input").ids.Amt_per_feet.text == ""
            or self.manager.get_screen("input").ids.advance.text == ""
            or self.manager.get_screen("input").ids.FHT_charge.text == ""
        ):
            ok_btn = MDFlatButton(text="OK", on_press=self.close_dialog)
            self.dialog = MDDialog(
                title="Error",
                text="Please check if you have entered all the values correctly",
                buttons=[ok_btn],
            )
            self.dialog.open()
        else:
            cust_name = self.manager.get_screen("input").ids.c_name.text
            cust_address = self.manager.get_screen("input").ids.c_address.text
            quote_date = self.manager.get_screen("input").ids.set_date.text
            amt_per_feet = self.manager.get_screen("input").ids.Amt_per_feet.text
            self.add_cust_data(cust_name, cust_address, quote_date, amt_per_feet)
            try:
                height_feet, width_feet = self.convert_height_width(
                    self.manager.get_screen("input").ids.height.text,
                    self.manager.get_screen("input").ids.width.text,
                )
                self.area = (
                    float(self.manager.get_screen("input").ids.quantity.text)
                    * float(height_feet)
                    * float(width_feet)
                )
                self.tot_amt = self.area * float(
                    self.manager.get_screen("input").ids.Amt_per_feet.text
                )
                flag = self.check_dups()
                if flag == 0:
                    if self.manager.get_screen("input").ids.product_menu.text in [
                        "Mosquito Net",
                        "Invisible Grill",
                        "Sliding Windows",
                        "UPVC Windows",
                        "Aluminum Mosquito Net",
                        "Openable Window",
                        "Pegion Net",
                    ]:
                        self.billing_data.append(
                            (
                                "W" + str(self.w_sr_no),
                                self.manager.get_screen("input").ids.room.text,
                                self.manager.get_screen("input").ids.product_menu.text,
                                str(height_feet),
                                str(width_feet),
                                self.manager.get_screen("input").ids.quantity.text,
                                str(round(self.area, 2)),
                                str(round(self.tot_amt, 2)),
                            )
                        )
                        self.w_sr_no += 1
                    elif self.manager.get_screen("input").ids.product_menu.text in [
                        "Aluminum Door",
                        "UPVC Door",
                    ]:
                        self.billing_data.append(
                            (
                                "D" + str(self.d_sr_no),
                                self.manager.get_screen("input").ids.room.text,
                                self.manager.get_screen("input").ids.product_menu.text,
                                str(height_feet),
                                str(width_feet),
                                self.manager.get_screen("input").ids.quantity.text,
                                str(round(self.area, 2)),
                                str(round(self.tot_amt, 2)),
                            )
                        )
                        self.d_sr_no += 1
                    elif (
                        self.manager.get_screen("input").ids.product_menu.text
                        == "Extra Pipe"
                    ):
                        self.billing_data.append(
                            (
                                "P" + str(self.p_sr_no),
                                self.manager.get_screen("input").ids.room.text,
                                self.manager.get_screen("input").ids.product_menu.text,
                                str(height_feet),
                                "-",
                                self.manager.get_screen("input").ids.quantity.text,
                                "-",
                                str(round(height_feet*amt_per_feet, 2)),
                            )
                        )
                        self.p_sr_no += 1
            except TypeError as ve:
                ok_btn = MDFlatButton(text="OK", on_press=self.close_dialog)
                self.dialog = MDDialog(
                    title="Error",
                    text="Please Enter Correct height and width values",
                    buttons=[ok_btn],
                )
                self.dialog.open()
            except ValueError as ve:
                ok_btn = MDFlatButton(text="OK", on_press=self.close_dialog)
                self.dialog = MDDialog(
                    title="Error",
                    text="Please enter all the values correctly",
                    buttons=[ok_btn],
                )
                self.dialog.open()
            except Exception as e:
                ok_btn = MDFlatButton(text="OK", on_press=self.close_dialog)
                self.dialog = MDDialog(
                    title="Error",
                    text="Please check all the entered values once",
                    buttons=[ok_btn],
                )
                self.dialog.open()
            self.manager.get_screen("input").ids.room.text = ""
            self.manager.get_screen("input").ids.product_menu.text = ""
            self.manager.get_screen("input").ids.height.text = ""
            self.manager.get_screen("input").ids.width.text = ""
            self.manager.get_screen("input").ids.quantity.text = ""
            self.manager.get_screen("input").ids.Amt_per_feet.text = ""

    def drpdown(self):
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "Mosquito Net",
                "on_release": lambda x="Mosquito Net": self.selected_product(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Invisible Grill",
                "on_release": lambda x="Invisible Grill": self.selected_product(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Sliding Windows",
                "on_release": lambda x="Sliding Windows": self.selected_product(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "UPVC Windows",
                "on_release": lambda x="UPVC Windows": self.selected_product(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Aluminum Door",
                "on_release": lambda x="Aluminum Door": self.selected_product(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Openable Window",
                "on_release": lambda x="Openable Window": self.selected_product(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Aluminum Mosquito Net",
                "on_release": lambda x="Aluminum Mosquito Net": self.selected_product(
                    x
                ),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Pegion Net",
                "on_release": lambda x="Pegion Net": self.selected_product(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "UPVC Door",
                "on_release": lambda x="UPVC Door": self.selected_product(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Extra Pipe",
                "on_release": lambda x="Extra Pipe": self.selected_product(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.product_menu,
            items=self.menu_list,
            width_mult=6,
            max_height=500,
        )
        self.menu.open()

    def selected_product(self, value):
        self.manager.get_screen("input").ids.product_menu.text = value
        self.menu.dismiss()

    def unitdrpdown(self):
        self.menu_list_unit = [
            {
                "viewclass": "OneLineListItem",
                "text": "mm",
                "on_release": lambda x="mm": self.selected_unit(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "cm",
                "on_release": lambda x="cm": self.selected_unit(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "m",
                "on_release": lambda x="m": self.selected_unit(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "inches",
                "on_release": lambda x="inches": self.selected_unit(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "feet",
                "on_release": lambda x="feet": self.selected_unit(x),
            },
        ]
        self.menu_unit = MDDropdownMenu(
            caller=self.ids.unit_h,
            items=self.menu_list_unit,
            width_mult=6,
            max_height=500,
        )
        self.menu_unit.open()

    def selected_unit(self, value):
        self.manager.get_screen("input").ids.unit_h.text = value
        self.manager.get_screen("input").ids.unit_w.text = value
        self.menu_unit.dismiss()

    def on_save(self, instance, value, date_range):
        self.manager.get_screen("input").ids.set_date.text = str(value)

    def on_cancel(self, instance, value):
        if self.manager.get_screen("input").ids.set_date.text == "Pick a Date":
            self.manager.get_screen("input").ids.set_date.text = "Pick a Valid Date"

    def setDate(self):
        date_picker = MDDatePicker()
        # self.manager.get_screen("input").ids.set_date.disabled = True
        date_picker.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_picker.open()


class TableScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.row = []
        self.rows = []

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def load_tabel(self):
        self.rows = self.manager.get_screen("input").billing_data
        self.data_tabel = MDDataTable(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.9, 0.6),
            check=True,
            column_data=[
                ("Sr No", dp(20)),
                ("Room", dp(35)),
                ("Product", dp(35)),
                ("Height(in feet)", dp(25)),
                ("Width(in feet)", dp(25)),
                ("Quantity", dp(20)),
                ("Area", dp(30)),
                ("Amount", dp(30)),
            ],
            row_data=self.rows,
        )
        self.data_tabel.bind(on_check_press=self.check_press)
        self.add_widget(self.data_tabel)

    def on_enter(self):
        self.load_tabel()

    def check_press(self, instance_table, current_row):
        self.row = current_row

    def edit_row(self):
        if self.row != []:
            self.manager.get_screen("input").ids.room.text = self.row[1]
            self.manager.get_screen("input").ids.product_menu.text = self.row[2]
            self.manager.get_screen("input").ids.height.text = self.row[3]
            self.manager.get_screen("input").ids.width.text = self.row[4]
            self.manager.get_screen("input").ids.unit_h.text = "feet"
            self.manager.get_screen("input").ids.unit_w.text = "feet"
            self.manager.get_screen("input").ids.quantity.text = str(
                ceil(float(self.row[6]) / (float(self.row[3]) * float(self.row[4])))
            )
            self.manager.get_screen("input").ids.Amt_per_feet.text = ""
            self.manager.get_screen("input").ids.advance.text = ""
            self.manager.get_screen("input").ids.FHT_charge.text = ""
        self.manager.current = "input"

    def gen_bill(self):
        if self.rows != []:
            tot_amount = (
                sum([round(float(i[-1]), 2) for i in self.rows])
                + float(self.manager.get_screen("input").ids.FHT_charge.text)
            ) - float(self.manager.get_screen("input").ids.advance.text)
            adv_tup = (
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "Adv(-)",
                    self.manager.get_screen("input").ids.advance.text,
                )
            
            svr_chg_tup = (
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "Srv chg",
                    self.manager.get_screen("input").ids.FHT_charge.text,
                )
            
            tot_amount_tup = ("", "", "", "", "", "", "Total Amount", str(tot_amount))
            print(self.rows, self.manager.get_screen("input").cust_data[0])
            Create_pdf(
                self.manager.get_screen("input").cust_data[0],
                self.rows.copy(),
                self.manager.get_screen("input").ids.note.text,
                adv_tup,
                svr_chg_tup,
                tot_amount_tup
            )
        else:
            ok_btn = MDFlatButton(text="OK", on_press=self.close_dialog)
            self.dialog = MDDialog(
                title="INFO",
                text="Please add data to generate pdf",
                buttons=[ok_btn],
            )
            self.dialog.open()


sm = ScreenManager()
sm.add_widget(InputScreen(name="input"))
sm.add_widget(TableScreen(name="table"))


class BillGeneratorApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "LightGreen"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "400"
        builder = Builder.load_string(helper)
        return builder


BillGeneratorApp().run()

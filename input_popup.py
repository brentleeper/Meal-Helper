from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta

class Input_Popup:
    def __init__(self, type, parent=None, data=None):
        #type options: new_meal, new_ingredient, new_instruction, edit_meal, edit_ingredient, edit_instruction

        self.done = False

        self.rv_data = {}

        self.type = type

        self.popup_window = top = Toplevel(parent)
        self.popup_window.transient(parent)

        if self.type == "new_meal":
            self.label = Label(top, text="Enter New Meal Name")
            self.label.pack()
            self.entry = Entry(top)
            self.entry.pack()
            self.button = Button(top, text="Add Meal", command=self.close_window)
            self.button.pack()
            self.entry.focus()

        elif self.type == "new_ingredient":
            self.label = Label(top, text="Select ingredient")
            self.label.pack()
            self.ingredient_combo = ttk.Combobox(top, state="Normal", values=["Ingredient Name", ""] + data["ingredients"])
            self.ingredient_combo.current(0)
            self.ingredient_combo.pack()
            self.unit_type_combo = ttk.Combobox(top, state="Normal", values=["Unit Type", ""]+data["unit_types"])
            self.unit_type_combo.current(0)
            self.unit_type_combo.pack()
            self.quantity_combo = ttk.Combobox(top, state="Normal", values=["Quantity",""]+data["quantities"])
            self.quantity_combo.current(0)
            self.quantity_combo.pack()
            self.button = Button(top, text="Add Ingredient", command=self.close_window)
            self.button.pack()
            self.ingredient_combo.focus()

        elif self.type == "new_instruction":
            self.label = Label(top, text="Add instruction")
            self.label.pack()
            self.entry = Entry(top)
            self.entry.pack()
            self.button = Button(top, text="Add Instruction", command=self.close_window)
            self.button.pack()
            self.entry.focus()

        elif self.type == "edit_meal":
            self.label = Label(top, text="Edit Meal Name")
            self.label.pack()
            self.entry = Entry(top)
            self.entry.insert(END, data["meal_name"])
            self.entry.pack()
            self.button = Button(top, text="Ok", command=self.close_window)
            self.button.pack()
            self.entry.focus()

        elif self.type == "edit_ingredient":
            self.label = Label(top, text=f"Edit ingredient: {data['ingredient']}")
            self.label.pack()
            self.unit_type_combo = ttk.Combobox(top, state="Normal", values=[data["unit"], ""] + data["unit_types"])
            self.unit_type_combo.current(0)
            self.unit_type_combo.pack()
            self.quantity_combo = ttk.Combobox(top, state="Normal", values=[data["quantity"], ""] + data["quantities"])
            self.quantity_combo.current(0)
            self.quantity_combo.pack()
            self.button = Button(top, text="Update Ingredient", command=self.close_window)
            self.button.pack()
            self.unit_type_combo.focus()

        elif self.type == "edit_instruction":
            self.label = Label(top, text="Edit instruction")
            self.label.pack()
            self.entry = Entry(top)
            self.entry.insert(END, data["current_instruction"])
            self.entry.pack()
            self.button = Button(top, text="Ok", command=self.close_window)
            self.button.pack()
            self.entry.focus()

        elif self.type == "custom_meal_plan":
            self.label_packs = []
            self.combos = []

            start_date = datetime.strptime(data["start_date"], "%m/%d/%y")
            weeks = data["weeks"]
            days_needed = data["days_needed"]

            total_days = weeks * 7

            meal_names = [meal.meal_name for meal in data["meals"]]

            self.meal_data = {}

            for meal in data["meals"]:
                self.meal_data.update({
                    meal.meal_name: meal
                })

            for i in range(total_days):
                cur_date = start_date + timedelta(days=i)
                cur_date_str = f"{cur_date.strftime('%m/%d/%y')} -  {cur_date.strftime('%A')}"
                cur_label = Label(top, text=cur_date_str)
                cur_label.pack()
                cur_label_pack = (cur_date_str, cur_label)
                self.label_packs.append(cur_label_pack)
                cur_combo = ttk.Combobox(top, state="readonly", values=[""]+meal_names)
                cur_combo.pack()
                self.combos.append(cur_combo)

        if "edit" not in self.type:
            self.done_button = Button(top, text="Done", command=self.set_done_true)
            self.done_button.pack()

        if data and "position" in data:
            self.popup_window.geometry(data["position"])
        else:
            self.popup_window.geometry("+%d+%d" % (parent.winfo_rootx()+(parent.winfo_reqwidth()/2)-(self.popup_window.winfo_reqwidth()/2),parent.winfo_rooty()))

        self.popup_window.bind("<Return>", self.close_window)

    def close_window(self, junk=None):
        if self.type == "new_meal" or self.type == "edit_meal":
            pass
            self.rv_data = {"name": self.entry.get().strip()}
        elif self.type == "new_ingredient" or self.type == "edit_ingredient":
            pass
            if self.type == "new_ingredient":
                ingredient = self.ingredient_combo.get()
            else:
                ingredient = None
            self.rv_data = {
                "ingredient": ingredient,
                "unit_type": self.unit_type_combo.get(),
                "quantity": self.quantity_combo.get()
            }
        elif self.type == "new_instruction" or self.type == "edit_instruction":
            pass
            self.rv_data = {
                "instruction": self.entry.get().strip()
            }
        elif self.type == "custom_meal_plan":
            meal_dates = []

            for i, label_pack in enumerate(self.label_packs):
                cur_date_str = label_pack[0].split("-")[0].strip()
                cur_meal = self.combos[i].get()
                if not cur_meal:
                    continue
                meal_dates.append((f'{datetime.strptime(cur_date_str, "%m/%d/%y").strftime("%Y-%m-%d")} 23:00:00', self.meal_data[cur_meal]))

            self.rv_data = {
                'meal_dates': meal_dates
            }


        if "edit" in self.type:
            self.done = True

        self.rv_data.update({
            'done': self.done,
            'position': self.popup_window.geometry()
        })

        self.popup_window.destroy()

    def set_done_true(self):
        self.done = True
        self.close_window()

    def get_ui(self):
        return self.popup_window

    def get_rv_data(self):
        for item in self.rv_data:
            if isinstance(self.rv_data[item], str):
                try:
                    self.rv_data.update({item: self.rv_data.title()})
                except:
                    pass
        return self.rv_data

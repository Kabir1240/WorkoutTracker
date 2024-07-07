from tkinter import *
from tkinter import messagebox
from tkinter_widgets import TkinterWidgets
from update_workouts import update_workouts, get_workouts
from typing import Dict

FONT = ("Arial", 8, "bold")


class UserInterface:
    def __init__(self):
        # inform user that their account is being created
        messagebox.showinfo(title="Workouts", message="Enter your workout details for today.")

        # create window
        self.window = Tk()
        self.window.title("Update Workouts")
        self.window.config(padx=15, pady=15)

        # create widgets and widget data struct
        self.widgets = TkinterWidgets()
        self.create_entries()
        self.create_buttons()
        self.create_listboxes()

        # main loop for window
        self.window.mainloop()

    def create_entries(self) -> None:
        """
        Creates an entry and stores it in widgets
        :return: None
        """

        # create and align entry
        entry_1 = Entry(width=70)
        entry_1.grid(row=0, column=0, columnspan=5)

        # store in widgets
        self.widgets.add_entry(key="workout", entry=entry_1)

    def create_buttons(self) -> None:
        """
        creates buttons, stores it in widgets
        :return: None
        """

        # create and align buttons
        button_1 = Button(text="Post", font=FONT, width=5, command=self.post)
        button_2 = Button(text="Update", font=FONT, command=self.update)
        button_1.grid(row=0, column=4, pady=5)
        button_2.grid(row=2, column=1)

        # store in widgets
        button_dict = \
            {
                "post":button_1,
                "update":button_1,
            }
            
        self.widgets.add_button_dict(button_dict=button_dict)

    def create_listboxes(self) -> None:
        """
        creates list boxes, stores it in widgets
        :return: None
        """

        # create and align listboxes
        listbox_1 = Listbox()
        listbox_2 = Listbox()
        listbox_3 = Listbox()
        listbox_4 = Listbox()
        listbox_5 = Listbox()

        listbox_1.grid(row=1, column=0)
        listbox_2.grid(row=1, column=1)
        listbox_3.grid(row=1, column=2)
        listbox_4.grid(row=1, column=3)
        listbox_5.grid(row=1, column=4)
        
        # store list boxes in widgets
        listbox_dict = \
            {
                'date':listbox_1,
                'time':listbox_2,
                'exercise':listbox_3,
                'duration':listbox_4,
                'calories':listbox_5,
            }

        self.widgets.add_listbox_dict(listbox_dict=listbox_dict)
    
    def post(self) -> None:
        """takes user input from entry and posts it to google sheets, informs user
        """

        workout_entry = self.widgets.get_entries("workout")
        workout_text = workout_entry.get()
        
        update_workouts(workout_text)
        self.update()
        messagebox.showinfo(title="Workouts", message="Workout details updated")
    
    def update(self) -> None:
        """updates listboxes from user entries retrieved from google sheets
        """

        workouts = get_workouts()['workouts']
        listbox_dict = self.widgets.get_listboxes()
        self.clear_listboxes(listbox_dict, len(workouts))
        
        for index in range(0, len(workouts)):
            listbox_dict['date'].insert(1, workouts[index]['date'])
            listbox_dict['time'].insert(1, workouts[index]['time'])
            listbox_dict['exercise'].insert(1, workouts[index]['exercise'])
            listbox_dict['duration'].insert(1, workouts[index]['duration'])
            listbox_dict['calories'].insert(1, workouts[index]['calories'])
    
    def clear_listboxes(self, listbox_dict:Dict[str,Listbox], number_of_elements) -> None:
        """clears previous data in listboxes

        Args:
            listbox_dict (Dict[str,Listbox]): dictionary of listboxes
            number_of_elements (_type_): number of elements to erase
        """
        for key, value in listbox_dict.items():
            value.delete(0, number_of_elements)

import tkinter as tk
from datetime import timedelta, time
from typing import List, Tuple
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasAgg, NavigationToolbar2Tk, FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler

from matplotlib.figure import Figure

from timeparser import *


class TimetablePlanner:
    def __init__(self, master):
        self.master = master

        # construct the task manager
        self.task_frame = tk.LabelFrame(self.master, text="Tasks")
        self.task_frame.grid(rowspan=3, sticky=tk.W, padx=3, pady=3)
        self.task_manager = TaskManager(self.task_frame)

        # construct the time manager
        self.time_frame = tk.LabelFrame(self.master, text="Schedule")
        self.time_frame.grid(row=3, columnspan=4)
        self.time_manager = TimeManager(self.time_frame)

        # construct the table manager
        self.table_frame = tk.Frame(self.master)
        self.table_frame.grid(column=1, rowspan=3, columnspan=3)
        self.table_manager = TableManager(self.table_frame)


class TableManager:
    """
    Synthesises information from the schedule and the tasks to construct a schedule
    """

    def __init__(self, master):
        self.master = master
        self.master.config(bg="red")


class TimeManager:
    """
    Keeps track of the time schedule
    """

    def __init__(self, master):
        # configure the data variables
        self.work_length = timedelta(minutes=30)
        self.start_time = time(hour=6, minute=30)
        self.break_durations = []

        self.master = master

        # configure the modifcation panel
        self.schedule_panel = tk.LabelFrame(master, text="Breaks")
        self.schedule_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.configure_work_length_panel()
        self.configure_start_time_panel()

        self.configure_breaks_list()

        self.configure_update_break_panel()

        self.configure_create_break_panel()

        self.configure_schedule_visualization(master)

    def configure_create_break_panel(self):
        self.create_break_frame = tk.LabelFrame(self.schedule_panel, text="Create Break", relief='flat')
        self.create_break_frame.pack(fill=tk.X)
        self.create_break_value = tk.StringVar()
        self.create_break_value.trace_add("write", self.create_break_edit_callback)
        self.create_break_entry = tk.Entry(self.create_break_frame, textvariable=self.create_break_value)
        self.create_break_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.create_break_button = tk.Button(self.create_break_frame, text="Add Break",
                                             command=self.create_break_callback, state=tk.DISABLED)
        self.create_break_button.pack(side=tk.LEFT,expand=True, fill=tk.X)

    def create_break_edit_callback(self):
        pass

    def create_break_callback(self):
        pass

    def configure_update_break_panel(self):
        self.update_break_frame = tk.LabelFrame(self.schedule_panel, text="Update Break", relief='flat')
        self.update_break_frame.pack(fill=tk.X)

        self.update_break_value = tk.StringVar()
        self.update_break_original = None
        self.update_break_value.trace_add("write", self.update_break_edit_callback)

        self.update_break_entry = tk.Entry(self.update_break_frame, textvariable=self.update_break_value, state=tk.DISABLED)
        self.update_break_entry.pack(fill=tk.X)

        self.update_break_panel = tk.Frame(self.update_break_frame)
        self.update_break_panel.pack(fill=tk.X, expand=True)

        self.update_break_update_button = tk.Button(self.update_break_panel, text="Update Break", state=tk.DISABLED,
                                                    command=self.update_break_update_callback)
        self.update_break_update_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.update_break_remove_button = tk.Button(self.update_break_panel, text="Delete Break", state=tk.DISABLED,
                                                    command=self.update_break_delete_callback)
        self.update_break_remove_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def update_break_edit_callback(self):
        pass

    def update_break_update_callback(self):
        pass

    def update_break_delete_callback(self):
        pass

    def configure_breaks_list(self):
        self.breaks_list = tk.Listbox(self.schedule_panel)
        self.breaks_list.pack(fill=tk.X)
        self.breaks_list.bind('<<ListboxSelect>>', self.breaks_list_callback)

    def breaks_list_callback(self):
        pass

    def configure_schedule_visualization(self, master):
        self.schedule_graph = tk.LabelFrame(master, text="Schedule Visualization")
        self.schedule_graph.pack(side=tk.LEFT, expand=True)

        self.schedule_figure = Figure(figsize=(5, 4), dpi=100)

        self.schedule_canvas = FigureCanvasTkAgg(self.schedule_figure, master=self.schedule_graph)
        self.schedule_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.schedule_toolbar = NavigationToolbar2Tk(self.schedule_canvas, self.schedule_graph)
        self.schedule_toolbar.update()
        self.schedule_canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        def on_key_event(event):
            key_press_handler(event, self.schedule_canvas, self.schedule_toolbar)

        self.schedule_canvas.mpl_connect('key_press_event', on_key_event)

    def configure_work_length_panel(self):
        self.work_length_panel = \
            tk.LabelFrame(self.schedule_panel, text="Work Interval Duration", relief='flat')
        self.work_length_panel.pack(side=tk.TOP,fill=tk.X)

        self.work_length_duration_value = tk.StringVar()
        self.work_length_duration_value.set(timedelta_to_str(self.work_length))
        self.work_length_duration_value.trace_add("write", self.work_length_duration_callback)
        self.work_length_duration_entry = \
            tk.Entry(self.work_length_panel, textvariable=self.work_length_duration_value)
        self.work_length_duration_entry.pack(side=tk.LEFT)

        self.work_length_duration_update_button = \
            tk.Button(self.work_length_panel,
                      text="Update Interval",
                      command=self.work_length_duration_update_callback,
                      state=tk.DISABLED)
        self.work_length_duration_update_button.pack(side=tk.LEFT)

        self.work_length_duration_reset_button = \
            tk.Button(self.work_length_panel,
                      text="Reset Field",
                      command=self.work_length_duration_reset_callback,
                      state=tk.DISABLED)
        self.work_length_duration_reset_button.pack(side=tk.LEFT)

    def parameters_updated(self):
        pass

    def work_length_duration_callback(self, *args):
        duration = self.work_length_duration_value.get()
        duration = parse_duration(duration)
        if duration is not None and duration != self.work_length:
            self.work_length_duration_update_button.configure(state=tk.NORMAL)
            self.work_length_duration_reset_button.configure(state=tk.NORMAL)
        elif duration is not None and duration == self.work_length:
            self.work_length_duration_update_button.configure(state=tk.DISABLED)
            self.work_length_duration_reset_button.configure(state=tk.DISABLED)
        else:
            self.work_length_duration_update_button.configure(state=tk.DISABLED)
            self.work_length_duration_reset_button.configure(state=tk.NORMAL)


    def work_length_duration_update_callback(self):
        duration = self.work_length_duration_value.get()
        duration = parse_duration(duration)
        if duration is not None and duration != self.work_length:
            self.work_length = duration
            self.parameters_updated()

        self.work_length_duration_callback()

    def work_length_duration_reset_callback(self):
        self.work_length_duration_value.set(timedelta_to_str(self.work_length))

        self.work_length_duration_callback()

    def configure_start_time_panel(self):
        self.start_time_panel = \
            tk.LabelFrame(self.schedule_panel, text="Start Time", relief='flat')
        self.start_time_panel.pack(side=tk.TOP, fill=tk.X)

        self.start_time_value = tk.StringVar()
        self.start_time_value.set(time_to_str(self.start_time))
        self.start_time_value.trace_add("write", self.start_time_callback)
        self.start_time_entry = \
            tk.Entry(self.start_time_panel, textvariable=self.start_time_value)
        self.start_time_entry.pack(side=tk.LEFT,expand=True, fill=tk.X)

        self.start_time_update_button = \
            tk.Button(self.start_time_panel,
                      text="Update Time",
                      command=self.start_time_update_callback,
                      state=tk.DISABLED)
        self.start_time_update_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.start_time_reset_button = \
            tk.Button(self.start_time_panel,
                      text="Reset Field",
                      command=self.start_time_reset_callback,
                      state=tk.DISABLED)
        self.start_time_reset_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

    def start_time_callback(self, *args):
        time_value = self.start_time_value.get()
        time_value = parse_time(time_value)
        if time_value is not None and time_value != self.start_time:
            self.start_time_update_button.configure(state=tk.NORMAL)
            self.start_time_reset_button.configure(state=tk.NORMAL)
        elif time_value is not None and time_value == self.start_time:
            self.start_time_update_button.configure(state=tk.DISABLED)
            self.start_time_reset_button.configure(state=tk.DISABLED)
        else:
            self.start_time_update_button.configure(state=tk.DISABLED)
            self.start_time_reset_button.configure(state=tk.NORMAL)



    def start_time_update_callback(self):
        time_value = self.start_time_value.get()
        time_value = parse_time(time_value)
        if time_value is not None and time_value != self.start_time:
            self.start_time = time_value
            self.parameters_updated()

        self.start_time_callback()


    def start_time_reset_callback(self):
        self.start_time_value.set(time_to_str(self.start_time))

        self.start_time_callback()


class TaskManager:
    """
        Keeps track of the current types of tasks and their importance
    """

    def __init__(self, master):
        self.padding_options = {'padx': 5, 'pady': 5}
        self.master = master
        self.tasks: List[Tuple[str, float]] = []

        self.listbox = tk.Listbox(self.master)
        self.listbox.pack(fill=tk.X, **self.padding_options)
        self.listbox.bind('<<ListboxSelect>>', self.task_list_callback)

        self.modify_entries_parent = tk.LabelFrame(self.master, text="Modify Task", relief='flat')
        self.modify_entries_parent.pack(fill=tk.X, **self.padding_options)

        self.modify_entries = tk.Frame(self.modify_entries_parent)
        self.modify_entries.pack(fill=tk.X, pady=5)

        self.modify_index = None
        self.modify_name_value = tk.StringVar()
        self.modify_score_value = tk.StringVar()
        self.modify_name_original = None
        self.modify_score_original = None

        tk.Label(self.modify_entries, text="Name:").pack(side=tk.LEFT, padx=2)
        self.modify_name = tk.Entry(
            self.modify_entries,
            textvariable=self.modify_name_value,
            state=tk.DISABLED
        )
        self.modify_name.pack(side=tk.LEFT)
        tk.Label(self.modify_entries, text="Weight:").pack(side=tk.LEFT, padx=2)
        self.modify_score = tk.Entry(
            self.modify_entries,
            textvariable=self.modify_score_value,
            state=tk.DISABLED
        )
        self.modify_score.pack(side=tk.LEFT)
        self.modify_name_value.trace_add("write", self.modify_name_callback)
        self.modify_score_value.trace_add("write", self.modify_score_callback)

        self.modify_update_button = tk.Button(
            self.modify_entries_parent,
            text="Update Task",
            state=tk.DISABLED,
            command=self.modify_update_callback
        )
        self.modify_update_button.pack(fill=tk.X, pady=2)
        self.modify_delete_button = tk.Button(
            self.modify_entries_parent,
            text="Delete Task",
            state=tk.DISABLED,
            command=self.modify_delete_callback
        )
        self.modify_delete_button.pack(fill=tk.X, pady=2)

        self.create_entries_parent = tk.LabelFrame(self.master, text="Create Task", relief='flat')
        self.create_entries_parent.pack(fill=tk.X, **self.padding_options)
        self.create_entries = tk.Frame(self.create_entries_parent)
        self.create_entries.pack(fill=tk.X, pady=5)

        tk.Label(self.create_entries, text="Name:").pack(side=tk.LEFT, padx=2)
        self.create_name_value = tk.StringVar()
        self.create_name = tk.Entry(self.create_entries, textvariable=self.create_name_value)
        self.create_name.pack(side=tk.LEFT)

        tk.Label(self.create_entries, text="Weight:").pack(side=tk.LEFT, padx=2)
        self.create_score_value = tk.StringVar()
        self.create_score = tk.Entry(self.create_entries, textvariable=self.create_score_value)
        self.create_score.pack(side=tk.LEFT)

        self.create_name_value.trace_add("write", self.create_name_callback)
        self.create_score_value.trace_add("write", self.create_score_callback)

        self.create_button = tk.Button(
            self.create_entries_parent,
            text="Create Task",
            state=tk.DISABLED,
            command=self.create_task_callback
        )
        self.create_button.pack(fill=tk.X, pady=2)

    def modify_delete_callback(self):
        if self.modify_index is not None:
            index = self.modify_index
            del self.tasks[index]
            self.listbox.delete(index)
            self.modify_index = None

        self.update_modify_components_state()

    def modify_update_callback(self):
        update = self.retrieve_modify_values()
        if self.modify_index is not None and update is not None:
            new_name, new_score = update
            index = self.modify_index
            del self.tasks[index]
            self.listbox.delete(index)
            self.tasks.insert(index, (new_name, new_score))
            self.listbox.insert(index, "%s : %s" % (new_name, new_score))
            self.modify_score_original = new_score
            self.modify_name_original = new_name

        self.update_modify_components_state()

    def task_list_callback(self, evt):
        if evt.widget is self.listbox:
            selection = evt.widget.curselection()
            index = None
            if len(selection) > 0:
                index = int(selection[0])
            else:
                return

            self.configure_entry_for_modification(index)

    def configure_entry_for_modification(self, index):
        if index is not None and index < len(self.tasks):
            self.modify_index = index
            self.modify_name_original = self.tasks[index][0]
            self.modify_score_original = self.tasks[index][1]
            self.modify_name_value.set(self.modify_name_original)
            self.modify_score_value.set(self.modify_score_original)
        else:
            self.modify_index = None

        self.update_modify_components_state()

    def modify_name_callback(self, *args):
        """
         Callback which updates the state of the modify entry components when the
        fields are changed
        :param args:  required to match the signature of the callback
        """
        self.update_modify_components_state()

    def modify_score_callback(self, *args):
        """
         Callback which updates the state of the modify entry components when the
        fields are changed
        :param args:  required to match the signature of the callback
        """
        self.update_modify_components_state()

    def update_modify_components_state(self):
        """
        Updates the states of all the components for modifing entries
        :return:
        """
        if self.modify_index is None:
            self.modify_name.configure(state=tk.DISABLED)
            self.modify_score.configure(state=tk.DISABLED)
            self.modify_update_button.configure(state=tk.DISABLED)
            self.modify_delete_button.configure(state=tk.DISABLED)

            self.modify_name_value.set("")
            self.modify_score_value.set("")
            self.modify_name_original = None
            self.modify_score_original = None

        elif self.retrieve_modify_values() is None:
            self.modify_name.configure(state=tk.NORMAL)
            self.modify_score.configure(state=tk.NORMAL)
            self.modify_update_button.configure(state=tk.DISABLED)
            self.modify_delete_button.configure(state=tk.NORMAL)
        else:
            self.modify_name.configure(state=tk.NORMAL)
            self.modify_score.configure(state=tk.NORMAL)
            self.modify_update_button.configure(state=tk.NORMAL)
            self.modify_delete_button.configure(state=tk.NORMAL)

    def retrieve_modify_values(self):
        """
        Retrieves the current values in the modify boxes if they are valid
        :return: (str,float) if the values are valid
        """
        name = self.modify_name_value.get()
        score = self.modify_score_value.get()

        try:
            score = float(score)
        except ValueError:
            score = None

        if score is None:
            return None
        if name == self.modify_name_original and score == self.modify_score_original:
            return None

        duplicated_name = any(x for x in self.tasks if x[0] == name)
        modified_name = name != self.modify_name_original

        if duplicated_name and modified_name:
            return None
        else:
            return (name, score)

    def create_task_callback(self):
        values = self.retrieve_create_values()
        if values is not None:
            name, score = values
            self.tasks.append((name, score))
            self.listbox.insert(tk.END, "%s : %s" % (name, score))
            self.clear_create_entries()

    def create_name_callback(self, *args):
        """
         Callback which updates the state of the create entry components when the
        fields are changed
        :param args:  required to match the signature of the callback
        """
        self.update_create_button_state()

    def create_score_callback(self, *args):
        """
        Callback which updates the state of the create entry components when the
        fields are changed
        :param args:  required to match the signature of the callback
        """
        self.update_create_button_state()

    def retrieve_create_values(self):
        """
        Retrieves the current values in the create boxes if they are valid
        :return: (str,float) if the values are valid
        """
        name = self.create_name_value.get()
        score = self.create_score_value.get()
        try:
            score = float(score)
        except ValueError:
            score = None
        if any(x for x in self.tasks if x[0] == name) or score is None:
            return None
        else:
            return (name, score)

    def update_create_button_state(self):
        """
        Enables or disables the create entry button based on whether the values in the
        corresponding fields are valid
        """
        if self.retrieve_create_values() is not None:
            self.create_button.configure(state=tk.NORMAL)
        else:
            self.create_button.configure(state=tk.DISABLED)

    def clear_create_entries(self):
        """
        Clears the corresponding add entry fields and updates the corresponding button states
        """
        self.create_name_value.set("")
        self.create_score_value.set("")
        self.update_create_button_state()


def main():
    root = tk.Tk()
    app = TimetablePlanner(root)
    root.mainloop()


main()

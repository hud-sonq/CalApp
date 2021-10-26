from datetime import date
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRoundFlatButton, MDFlatButton, MDRectangleFlatButton, MDRaisedButton, MDIconButton, \
    MDRoundFlatIconButton, MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.card import MDCard, MDSeparator
from kivy.core.window import Window
import time
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList, IRightBodyTouch, ThreeLineListItem, OneLineListItem, \
    OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.selectioncontrol import MDSwitch
from datetime import date as d, timedelta, datetime
import calendar
import json

time_column_width = 150


class CircularButton(ButtonBehavior, Label):
    pass

class MyToggleButton(MDFillRoundFlatButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_down = (0,0,0,.4)
        if self.state == 'down':
            self.md_bg_color = (0,0,0,.4)
    line_color = (0, 0, 0, 1)
    text_color = (0, 0, 0, 1)
Window.size = (335,660)
#Window.size = (700,660)


# support for exceptions that modify the actualized event without having to change the parent
# such as, if on tuesdays discourse on the porch is shorter than usual, for example

class LineButtonItem(IRightBodyTouch, MDRectangleFlatButton):
    line_color = (0, 0, 0, 1)
    text_color = (0, 0, 0, 1)

class LineIconButtonItem(IRightBodyTouch, MDIconButton):
    pass


class LineTextInputItem(IRightBodyTouch, TextInput):
    text_color = (0, 0, 0, .8)
    hint_text_color = (0,0,0,1)
    background_color=(0, 0, 0, 0)

    pass

# calendar & calendar generation related functions


color_name_rgba= {
    "red": (1,0,0,.2),
    "dark blue": (.1,0,1,.5),
    "dark grey": (0,0,0,.4),
    "purple": (.5,0,.5,.2),
    "orange": (1,.4,0,.4)
}


def date_string_to_tuple(string):
    string_list = string.split('-')
    int_list = []
    for value in string_list:
        int_list.append(value)
    year = int(int_list[0])
    month = int(int_list[1])
    day = int(int_list[2])
    output = d(year, month, day)
    return output

def date_string_pretty(string):
    date = date_string_to_tuple(string)
    month = date.strftime('%b')
    day = date.day
    year = date.strftime('%Y')
    pretty_date = f'{month} {day}, {year}'
    return pretty_date


def pretty_date_range_string(date1, date2):
    date1 = date_string_to_tuple(date1)
    date2 = date_string_to_tuple(date2)

    if date1.year == date2.year:
        if date1.month == date2.month:
            pretty_range = f"{date1.strftime('%b')} {date1.day}—{date2.day}, {date2.strftime('%Y')}"
        else:
            pretty_range = f"{date1.strftime('%b')} {date1.day} — {date2.strftime('%b')} {date2.day}, {date2.strftime('%Y')}"
    else:
        pretty_range = f"{date1.strftime('%b')} {date1.day}, {date1.strftime('%Y')} — {date2.strftime('%b')} {date2.day}, {date2.strftime('%Y')}"
    return pretty_range



def pretty_datetime_range_string(date1, date2):
    datetime_list1 = date1.split(' ')
    datetime_list2 = date2.split(' ')

    time1 = datetime_list1[1]
    time2 = datetime_list2[1]

    date1 = date_string_to_tuple(datetime_list1[0])
    date2 = date_string_to_tuple(datetime_list2[0])

    if date1 == date2:
        pretty_range = f"{date1.strftime('%b')} {date1.day}, {date1.strftime('%Y')}, {time1}-{time2}"
    else:
        pretty_range = f"{date1.strftime('%b')} {date1.day}, {time1} - {date2.strftime('%b')} {date2.day}, {time2}, {date1.strftime('%Y')}"

    return pretty_range


def time_string_to_minutes(string):
    string_list = string.split(':')
    int_list = []
    for value in string_list:
        int_list.append(value)
    hour = int(int_list[0])
    minute = int(int_list[1])
    output = 60*hour + minute
    return output

def order_events_by_date(unsorted_events):
    sorted_event_keys = sorted(unsorted_events,
                               key=lambda x: (datetime.strptime(unsorted_events[x]["start time"], "%Y-%m-%d %H:%M")))

    sorted_events = {}
    for key in sorted_event_keys:
        value = unsorted_events[key]
        sorted_events[key] = value

    return sorted_events

def all_weekday_between(start_date, end_date, weekdays):
    if weekdays == "everyday" or weekdays == "daily":
        weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    date_range = end_date - start_date
    output = []
    for date in range(date_range.days + 1):
        day = start_date + timedelta(days=date)
        if calendar.day_name[day.weekday()] in weekdays:
            output.append(day)
    return output

def open_json_file(filename):
    with open(filename) as json_file:
        output = json.load(json_file)
    return output






with open('parent_kinds.json') as json_file:
    kinds_file = json.load(json_file)




def render_actual_events():
    print('RENDERING EVENTS')

    parent_file = open_json_file('event_parents.json')
    parent_events = {}
    for parent_entry in parent_file:

        parent = parent_file[parent_entry]

        name = parent_entry
        start_date = date_string_to_tuple(parent["parent start date"])
        end_date = date_string_to_tuple(parent["parent end date"])


        weekdays = parent["repeats"]
        kind = parent["kind"]
        exceptions = parent["exceptions"]


        parent_dates = all_weekday_between(start_date, end_date, weekdays)

        for count, date in enumerate(parent_dates):
            if time_string_to_minutes(parent["event start time"]) <= time_string_to_minutes(parent["event end time"]):
                event_end_date = str(date)
            else:
                event_end_date = str((date + timedelta(days=1)))
            date = str(date)

            event_id = f"{name}_%d" % count


            parent_events[event_id] = {
                "parent": parent_entry,
                "summary": name,
                "start time": date + " " + parent["event start time"],
                "end time": event_end_date + " " + parent["event end time"],
                "kind": kind,
                "sub kind": parent["sub kind"],
                "movable": kinds_file[kind]["movable"],
                "squishable": kinds_file[kind]["squishable"],
            }
            if "minimum duration" in parent:
                parent_events[event_id]["minimum duration"] = parent["minimum duration"]
            if "early bound" in parent:
                parent_events[event_id]["early bound"] = parent["early bound"]
            if "late bound" in parent:
                parent_events[event_id]["late bound"] = parent["late bound"]
            parent_events[event_id]["description"] = ""
            parent_events[event_id]["tags"] = parent["tags"]

    sorted_events = order_events_by_date(parent_events)
    with open('events_example.json', 'w') as outfile:
        json.dump(sorted_events, outfile, indent=4)

    print(len(open_json_file('events_example.json')))


def time_to_string(time):
    if time.minute == 0:
        str_early_bound_minute = str(time.minute) + '0'
    else:
        str_early_bound_minute = str(time.minute)
    output = str(time.hour) + ':' + str_early_bound_minute
    return output

def string_to_datetime(string):
    output = datetime.strptime(string, "%Y-%m-%d %H:%M")
    return output

def string_to_time(string):
    output = datetime.strptime(string,'%H:%M')
    return output


def get_current_event():
    now = datetime.now()
    with open('events_example.json') as json_file:
        events = json.load(json_file)
        print(events)
    for event in events:
        start_time = string_to_datetime(events[event]["start time"])
        end_time = string_to_datetime(events[event]["end time"])
        if start_time < now < end_time:
            print(event)
            return event
            pass
        else:
            pass
    return "None"


def get_position_of_dict_entry(key, dict):
    list_of_keys = []
    for item in dict:
        list_of_keys.append(item)
    return list_of_keys.index(key)

def get_current_or_next_event():
    now = datetime.now()
    events = open_json_file('events_example.json')
    last_event = ''

    events_list = []

    for event in events:
        events_list.append(event)

    for event in events:
        end_time = string_to_datetime(events[event]["end time"])
        if end_time < now:
            last_event = event
            if end_time > now:
                break

    last_event_num = (events_list.index(last_event))
    next_event = events_list[last_event_num+1]
    return next_event

get_current_or_next_event()



def get_next_event():
    all_events = open_json_file('events_example.json')

    current_event = get_current_event()
    list_of_events = []
    for key in all_events:
        list_of_events.append(key)
    current_event_num = (list_of_events.index(current_event))
    next_event = list_of_events[current_event_num+1]
    return next_event









#print("Your current event is:", get_current_event())

def get_days_to_display():
    with open('display_data.json') as json_file:
        days_to_display = json.load(json_file)["days to display"]
    return days_to_display




def weekday_int_to_dayname(int, *args):
    weekdays = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    for arg in args:
        if arg == 'full':
            weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        elif arg == 'initial':
            weekdays = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
        elif arg == 'lower case':
            weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    return weekdays[int]

def string_to_date(string):
    output = datetime.strptime(string, "%Y-%m-%d").date()
    return output





class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    target = StringProperty()

class EventClickDialog(BoxLayout):
    pass

class RoundedButton(Button):
    pass

class SwitchItem(IRightBodyTouch, MDSwitch):
    pass

class FlatButtonItem(IRightBodyTouch, MDFlatButton):
    pass

class SelectWeek(MDDialog):
    pass

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color







def change_json_dict(file, key, value):
    a_file = open(file, "r")
    json_object = json.load(a_file)
    print(json_object)
    json_object[key] = value

    a_file = open(file, "w")

    json.dump(json_object, a_file, indent=2)
    a_file.close()


def change_json_dict_2(file, key1, key2, value):
    a_file = open(file, "r")
    json_object = json.load(a_file)
    json_object[key1][key2] = value

    a_file = open(file, "w")

    json.dump(json_object, a_file, indent=2)
    a_file.close()



def get_json_dict_value(file, key):
    a_file = open(file, "r")
    json_object = json.load(a_file)
    print(json_object)
    value = json_object[key]
    return value



def get_json_dict_value2(file, key1, key2):
    a_file = open(file, "r")
    json_object = json.load(a_file)
    print(json_object)
    value = json_object[key1][key2]
    return value







# this is copied and pasted from the google.py source code because I couldn't figure out how to import the module



# datetime objects are easier to work with, but the calendar API needs a utc string
# this function makes it so that I can convert a datetime object to a UTC string that shares
# precisely the same timestamp
def local_to_utc(input):
    # discerns the difference between utc and local time
    now_timestamp = time.time()
    local_now_timestamp = datetime.fromtimestamp(now_timestamp)
    utc_now_timestamp = datetime.utcfromtimestamp(now_timestamp)
    offset = utc_now_timestamp - local_now_timestamp

    utctime = input + offset
    utcformat = utctime.isoformat() + 'Z'
    return utcformat




def utc_to_local(input):
    # 2021-09-15T0get_days_to_display():30:00-05:00
    input = input.replace('T', ' ')
    input = input[0:19]
    output = datetime.strptime(input, '%Y-%m-%d %H:%M:%S')

    return output



def time_to_minutes(time):
    total = time.hour*60 + time.minute
    return total

# custom widgets

class TimeLineHorizontal(Widget):
    pass

class LineHorizontal(Widget):
    pass

class LineVertical(Widget):
    pass

class NowLine(Widget):
    pass


class AddItemToList(OneLineAvatarIconListItem):
    pass


class ListLineHorizontal(Widget):
    pass



class WeekdayButton(
    ThemableBehavior, CircularRippleBehavior, ButtonBehavior, BoxLayout
):
    """A class that implements a list for choosing a day."""

    text = StringProperty()
    owner = ObjectProperty()
    is_selected = BooleanProperty(False)




#class TouchFloatLayout()

class CalendarCompanionApp(MDApp):
    # this function defines the variables that will be passed between other functions
    # (most of these will be passed between the "refreshed",  "transition", and "squish" functions)
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None


    def on_touch_move(self, touch):
        if 'angle' in touch.profile:
            print('The touch angle is', touch.a)

    def days_callback(self, button):
        self.days_menu.caller = button
        self.days_menu.open()

    def days_menu_callback(self, text_item):
        self.days_menu.dismiss()
        menu_days = ["1 Day", "2 Days", "3 Days", "4 Days", "5 Days", "7 Days", "14 Days"]

        menu_items = []
        for item in menu_days:
            menu_items.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": item,
                    "height": 80,
                    "on_release": lambda x=item: self.days_menu_callback(x),
                }
            )

        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        text_item = int(text_item.split(' ')[0])
        change_json_dict('display_data.json', 'days to display', text_item)
        self.display_week_events()

    def kind_menu_open(self, button):
        self.kind_menu.caller = button
        self.kind_menu.open()

    def kind_menu_select(self, textitem):
        self.kind_menu.dismiss()
        kind_dict = open_json_file('parent_kinds.json')

        kind_list = []
        for kind in kind_dict:
            kind_list.append(kind)

        kind_menu_items = []
        for item in kind_list:
            kind_menu_items.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": item,
                    "height": 80,
                    "on_release": lambda x=item: self.kind_menu_select(x),
                }
            )
        self.kind_menu = MDDropdownMenu(
            items=kind_menu_items,
            width_mult=4,
        )



        parent = open_json_file('display_data.json')['editing parent']

        file = 'event_parents.json'

        a_file = open(file, "r")
        json_object = json.load(a_file)
        print(json_object)

        print(textitem)

        parent = open_json_file('display_data.json')['editing parent']

        if parent != 'new parent':
            json_object[parent]["kind"] = textitem

            a_file = open(file, "w")

            json.dump(json_object, a_file, indent=2)
            a_file.close()

            self.update_edit_parent(parent)
        else:
            change_json_dict('display_data.json', 'new parent kind', textitem)
            self.update_new_parent_screen()

    def interval_menu_open(self, button):
        self.interval_menu.caller = button

        # self.interval_menu.open()


    def openScreen(self, itemdrawer):
        self.openScreenName(itemdrawer.target, "left")
        self.root.ids.nav_drawer.set_state("close")



    def openScreenName(self, screenName, transitiondirection):
        self.root.ids.screen_manager.current = screenName
        self.root.ids.screen_manager.transition.direction = transitiondirection

        a_file = open("app_data.json", "r")
        json_object = json.load(a_file)
        new_previous_screen = json_object["current screen"]
        json_object["previous screen"] = new_previous_screen
        json_object["current screen"] = screenName
        a_file = open("app_data.json", "w")
        json.dump(json_object, a_file, indent=2)
        a_file.close()

    def previous_screen(self):
        a_file = open("app_data.json", "r")
        json_object = json.load(a_file)
        previous_screen = json_object["previous screen"]
        return previous_screen

    def current_screen(self):
        a_file = open("app_data.json", "r")
        json_object = json.load(a_file)
        current_screen = json_object["current screen"]
        return current_screen

    def go_back(self):
        self.openScreenName(self.previous_screen(), "right")




    def on_start(self):

        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="weekViewScreen", text="Week View",
                       icon="view-week-outline",
                       on_release=self.openScreen)
        )
        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="priorityScreen", text="Priority List",
                       icon="format-list-numbered",
                       on_release=self.openScreen)
        )
        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="parentEventsScreen", text="Recurring Events",
                       icon="replay",
                       on_release=self.open_parent_screen)
        )
        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="agenda", text="Agenda",
                       icon="view-agenda-outline",
                       on_release=self.openScreen)
        )
        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="report", text="Report",
                       icon="newspaper-variant-outline",
                       on_release=self.openScreen)
        )
        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="settings", text="Settings",
                       icon="cog-outline",
                       on_release=self.openScreen)
        )




        self.theme_cls.primary_palette = 'Gray'
        self.theme_cls.primary_hue = '300'

        render_actual_events()

        today = date.today()
        idx = (today.weekday() + 1) % 7  # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
        last_sunday = today - timedelta(days=idx)



        self.display_week_events()
        self.priority_screen()
        self.root.ids.screen_manager.current = self.current_screen()


    def priority_screen(self):
        priority_dict = open_json_file('parent_kinds.json')
        for priority in priority_dict:
            list_item = ThreeLineListItem(text=priority, secondary_text=" Movable: "+priority_dict[priority]['movable'], tertiary_text=" Squishable: "+priority_dict[priority]['squishable'])
            self.root.ids.priority_list.add_widget(list_item)

    def open_parent_screen(self, itemdrawer):
        self.openScreenName(itemdrawer.target, "left")
        self.root.ids.nav_drawer.set_state("close")
        self.load_parent_screen()


    def back_to_parent_screen(self):
        self.load_parent_screen()
        self.go_back()



    def load_parent_screen(self):
        self.root.ids.parent_list.clear_widgets()
        parent_dict = open_json_file('event_parents.json')
        for parent in parent_dict:
            parent_entry = parent_dict[parent]
            repeats = parent_entry['repeats']
            if type(repeats) == list:
                repeats = 's, '.join(repeats)+'s'
            else:
                repeats = str(repeats)

            card = MDCard(orientation='vertical',
                          padding=20,
                          height=220,
                          size_hint=(.9, None),
                          elevation=0,
                          md_bg_color=(0, 0, 0, 0)
                          )

            card.add_widget(MDLabel(text=parent, valign='center', adaptive_height=True))
            card.add_widget(MDLabel(text='   ' + parent_entry['kind'], opacity=.638))
            card.add_widget(MDLabel(text='   ' + repeats, opacity=.638))

            card.add_widget(MDLabel(text='   ' + pretty_date_range_string(parent_entry['parent start date'], parent_entry['parent end date']),  opacity=.638))

            card.add_widget(ListLineHorizontal())
            card.bind(on_touch_down=self.parent_item_click)  # set binding

            self.root.ids.parent_list.add_widget(card)
        self.root.ids.parent_list.add_widget(AddItemToList(on_press=self.open_new_parent))

    def open_new_parent(self, arg):

        change_json_dict('display_data.json', 'editing parent', 'new parent')
        change_json_dict('display_data.json', 'new parent kind', 'Select Kind')
        change_json_dict('display_data.json', 'new parent start date', 'Select Date')
        change_json_dict('display_data.json', 'new parent end date', 'Select Date')

        self.update_new_parent_screen()

        self.openScreenName("newParentScreen", "up")

    def new_event(self):
        print('noice')

    def update_new_parent_screen(self):
        #self.root.ids.new_parent_attributes_list.clear_widgets()

        #parent_dict = open_json_file('event_parents.json')[parent]

        #self.root.ids.new_parent_attributes_list.add_widget(BoxLayout(orientation='horizontal'))

        #scrollview_height = self.root.ids.new_parent_scrollview.height

        #box_layout = BoxLayout(orientation='horizontal', padding=(100,10,100,50), pos=(0,self.root.ids.new_parent_scrollview.height-200))
        #box_layout.add_widget(MDLabel(text=''))
        #title_input = MDTextField(hint_text='Title', text_color=(0, 0, 0, .8), mode='rectangle')
        #box_layout.add_widget(title_input)
        #box_layout.add_widget(MDLabel(text=''))
        #self.root.ids.new_parent_attributes_list.add_widget(box_layout)


        #self.root.ids.new_parent_attributes_list.add_widget(MDLabel(text='Kind:', pos=(20, self.root.ids.new_parent_scrollview.height-660)))
        self.root.ids.select_new_parent_kind.text = get_json_dict_value('display_data.json', 'new parent kind')

        #self.root.ids.new_parent_attributes_list.add_widget(MDRectangleFlatButton(text=kind_text, line_color=(0, 0, 0, 1), text_color=(0, 0, 0, 1), pos=(120,scrollview_height-300), on_press=self.kind_menu_open))

        #self.root.ids.new_parent_attributes_list.add_widget(MDLabel(text='Date Range:', pos=(20, self.root.ids.new_parent_scrollview.height-760)))
        #self.root.ids.new_parent_attributes_list.add_widget(MDRectangleFlatButton(text=get_json_dict_value('display_data.json', 'new parent start date'), line_color=(0, 0, 0, 1), text_color=(0, 0, 0, 1), pos=(250,scrollview_height-400), on_press=self.pick_parent_start_date))
        #self.root.ids.new_parent_attributes_list.add_widget(MDRectangleFlatButton(text=get_json_dict_value('display_data.json', 'new parent end date'), line_color=(0, 0, 0, 1), text_color=(0, 0, 0, 1), pos=(450, scrollview_height-400), on_press=self.pick_parent_end_date))
        pass


    def parent_item_click(self, card, touch):
        if card.collide_point(*touch.pos):
            parent = card.children[-1].text
            self.open_edit_parent(parent)

    def open_edit_parent(self, parent):
        self.update_edit_parent(parent)

        self.root.ids.editParentToolbar.title = 'Editing: ' + parent
        self.openScreenName('editParentScreen', 'left')


    def add_bounds(self, parent):
        parent_file = open_json_file('event_parents.json')

        parent_dict = parent_file[parent]


        # early bound should be half an hour before start, late bound half an hour after end, by default

        default_difference = 30

        early_bound = datetime.strptime(parent_dict['event start time'], "%H:%M") - timedelta(minutes=default_difference)
        early_bound = time_to_string(early_bound)


        late_bound = datetime.strptime(parent_dict['event end time'], "%H:%M") + timedelta(minutes=default_difference)
        late_bound = time_to_string(late_bound)


        parent_position = get_position_of_dict_entry(parent, parent_file)

        parent_file.pop(parent)

        parent_dict['early bound'] = early_bound
        parent_dict['late bound'] = late_bound


        #this whole function just ensures that it places the parent entry in its original order
        new_parent_file = {}
        for count, key in enumerate(parent_file):
            if count == parent_position:
                new_parent_file[parent] = parent_dict
            new_parent_file[key] = parent_file[key]



        with open('event_parents.json', 'w') as outfile:
            json.dump(new_parent_file, outfile, indent=4)

        self.update_edit_parent(parent)

    def remove_bounds(self, parent):
        parent_file = open_json_file('event_parents.json')
        parent_file[parent].pop('early bound')
        parent_file[parent].pop('late bound')
        with open('event_parents.json', 'w') as outfile:
            json.dump(parent_file, outfile, indent=4)

        self.update_edit_parent(parent)

    def update_edit_parent(self, parent):
        self.root.ids.parent_attributes_list.clear_widgets()

        items_to_update_dict = {}


        #save_item = OneLineListItem(ripple_scale=0)

        #parent_attributes_list
        parent_dict = open_json_file('event_parents.json')[parent]

        title_item = OneLineListItem(ripple_scale=0)
        title_item.add_widget(LineTextInputItem(font_size=34, hint_text=parent, pos_hint={"center_x": .5, "center_y": .5}, size_hint_x=.92, size_hint_y=.8))
        self.root.ids.parent_attributes_list.add_widget(title_item)


        kind_item = OneLineListItem(text='Kind:', ripple_scale=0)
        kind_item.add_widget(LineButtonItem(text=parent_dict['kind'], on_press=self.kind_menu_open, pos_hint={"x": .2, "center_y": .5}))
        parent_dict.pop('kind')
        self.root.ids.parent_attributes_list.add_widget(kind_item)

        date_range_item = OneLineListItem(text='Date Range:', ripple_scale=0)
        date_range_item.add_widget(LineButtonItem(text=date_string_pretty(parent_dict['parent start date']), on_press=self.pick_parent_start_date, pos_hint={"x": .33, "y": .1}))
        date_range_item.add_widget(LineButtonItem(text=date_string_pretty(parent_dict['parent end date']), on_press=self.pick_parent_end_date, pos_hint={"x": .67, "y": .1}))
        self.root.ids.parent_attributes_list.add_widget(date_range_item)

        select_repeats_interval_item = OneLineListItem(text='Repeats every:', ripple_scale=0)
        select_repeats_interval_item.add_widget(LineButtonItem(text='hm', on_press=self.interval_menu_open, pos_hint={"x": .8, "y": .1}))
        self.root.ids.parent_attributes_list.add_widget(select_repeats_interval_item)

        select_weekday_item = OneLineListItem(ripple_scale=0)
        for i in range(7):
            weekday = weekday_int_to_dayname(i, 'full')

            print(weekday)
            if weekday in parent_dict['repeats']:
                state = 'down'
            else:
                state = 'normal'

            select_weekday_item.add_widget(MyToggleButton(text=weekday_int_to_dayname(i, 'initial'), pos_hint={'x': (i/7), 'center_y': .5}, state=state, on_press=lambda x, w=weekday, s=state: self.update_repeats(parent, w, s)))
        self.root.ids.parent_attributes_list.add_widget(select_weekday_item)

        # UPDATE CHANGES TO A DICT, THEN ON SAVE, UPDATE ALL CHANGES IN DICT TO RESPECTIVE JSON FILES
        items_to_update_dict['repeats'] = []


        select_weekday_item2 = OneLineListItem(ripple_scale=0)
        for i in range(7):
            weekday = weekday_int_to_dayname(i, 'full')

            print(weekday)
            if weekday in parent_dict['repeats']:
                state = 'down'
            else:
                state = 'normal'

            select_weekday_item2.add_widget(MyToggleButton(text=weekday_int_to_dayname(i, 'initial'), pos_hint={'x': (i/7), 'center_y': .5}, state=state, on_press=lambda x, w=weekday, s=state: items_to_update_dict['repeats'].append(w) ))
        self.root.ids.parent_attributes_list.add_widget(select_weekday_item2)


        time_range_item = OneLineListItem(text='Event Start/End:', ripple_scale=0)
        time_range_item.add_widget(LineButtonItem(text=parent_dict['event start time'],
                                                  on_press=lambda x: self.pick_event_start_time(parent), pos_hint={"center_x": .55, "center_y": .5}))
        time_range_item.add_widget(
            LineButtonItem(text=parent_dict['event end time'], on_press=self.pick_parent_end_date,
                           pos_hint={"center_x": .85, "center_y": .5}))

        self.root.ids.parent_attributes_list.add_widget(time_range_item)

        bounds_item = OneLineListItem(ripple_scale=0)
        if 'early bound' in parent_dict:
            bounds_item.text = '              Bounds:'
            bounds_item.add_widget(LineButtonItem(text=parent_dict['early bound'],
                                                      on_press=self.pick_parent_start_date,
                                                      pos_hint={"center_x": .55, "center_y": .5}))
            bounds_item.add_widget(
                LineButtonItem(text=parent_dict['late bound'], on_press=self.pick_parent_end_date,
                               pos_hint={"center_x": .85, "center_y": .5}))
            bounds_item.add_widget(MDIconButton(icon='minus-circle', pos_hint={"center_y": .5}, on_press=lambda x: self.remove_bounds(parent)))
        else:
            bounds_item.add_widget(MDRoundFlatIconButton(icon='plus-circle', icon_color = (0,0,0,1), text_color=(0,0,0,1), line_color=(0,0,0,1), text='Add Bounds', pos_hint={
                "center_x": .5, "center_y": .5}, on_press=lambda x: self.add_bounds(parent)))

        self.root.ids.parent_attributes_list.add_widget(bounds_item)


        #date_range_item = OneLineListItem(text='Date Range:')
        #date_range_item.add_widget(MDRectangleFlatButton(text=date_string_pretty(parent_dict['parent start date']), line_color=(0, 0, 0, 1), text_color=(0, 0, 0, 1), pos=(220,(len(parent_dict)-2)*100), on_press=self.pick_parent_start_date))
        #date_range_item.add_widget(MDRectangleFlatButton(text=date_string_pretty(parent_dict['parent start date']), line_color=(0, 0, 0, 1), text_color=(0, 0, 0, 1), pos=(220,(len(parent_dict)-2)*100), on_press=self.pick_parent_start_date))
        #date_range_item.add_widget(MDRectangleFlatButton(text=date_string_pretty(parent_dict['parent end date']), line_color=(0, 0, 0, 1), text_color=(0, 0, 0, 1), pos=(450,(len(parent_dict)-2)*100), on_press=self.pick_parent_end_date))


        #parent_dict.pop('parent start date')
        #parent_dict.pop('parent end date')

        #self.root.ids.parent_attributes_list.add_widget(date_range_item)

        weekday_range_item = OneLineListItem(text='weekdays:')
        weekday_range_item.add_widget(
            MDRectangleFlatButton(text='weekday', line_color=(0, 0, 0, 1), text_color=(0, 0, 0, 1),
                                  pos=(220, (len(parent_dict) - 3) * 100), on_press=self.select_weekday))
        self.root.ids.parent_attributes_list.add_widget(weekday_range_item)

        for attribute in parent_dict:
            self.root.ids.parent_attributes_list.add_widget(
                OneLineListItem(text=attribute + ': ' + str(parent_dict[attribute])))

        test_widget = OneLineListItem(ripple_scale=0)
        test_widget.add_widget(LineButtonItem(text='DELETE RECURRING EVENT', pos_hint={"center_x": .5, "y": .1}, on_press=lambda x: self.delete_parent_dialog(parent)))
        self.root.ids.parent_attributes_list.add_widget(test_widget)

        change_json_dict('display_data.json', 'editing parent', parent)


        render_actual_events()
        self.display_week_events()

    def update_repeats(self, parent, weekday, state):
        print(parent,weekday,state)

        repeats = get_json_dict_value2('event_parents.json', parent, 'repeats')

        new_repeats = repeats

        if state == 'down':

            new_repeats.remove(weekday)

        else:
            new_repeats.append(weekday)

        change_json_dict_2('event_parents.json', parent, 'repeats', new_repeats)

        self.update_edit_parent(parent)


    def today(self):
        today = str(date.today())
        change_json_dict('display_data.json', 'first day', today)

        self.display_week_events()

    def this_week(self):
        today = date.today()
        idx = (today.weekday() + 1) % 7  # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
        last_sunday = today - timedelta(days=idx)

        change_json_dict('display_data.json', 'first day', str(last_sunday))

        self.display_week_events()


    # there should be a neat way to unify all these functions, I would think

    def on_display_date_save(self, instance, value, date_range):
        change_json_dict('display_data.json', 'first day', str(value))
        self.display_week_events()

    def pick_display_date(self):
        date_dialog = MDDatePicker(firstweekday=6)
        date_dialog.bind(on_save=self.on_display_date_save)
        date_dialog.open()


    def on_parent_start_date_save(self, instance, value, date_range):
        parent = open_json_file('display_data.json')['editing parent']
        if parent != 'new parent':
            change_json_dict_2('event_parents.json', parent, 'parent start date', str(value))
            self.update_edit_parent(parent)
        else:
            change_json_dict('display_data.json', 'new parent start date', str(value))
            self.update_new_parent_screen()


    def pick_parent_start_date(self, arg):
        date_dialog = MDDatePicker(firstweekday=6)
        date_dialog.bind(on_save=self.on_parent_start_date_save)
        date_dialog.open()

    def on_parent_end_date_save(self, instance, value, date_range):
        parent = open_json_file('display_data.json')['editing parent']
        if parent != 'new parent':
            change_json_dict_2('event_parents.json', parent, 'parent end date', str(value))
            self.update_edit_parent(parent)
        else:
            change_json_dict('display_data.json', 'new parent end date', str(value))
            self.update_new_parent_screen()

    def pick_parent_end_date(self, arg):
        date_dialog = MDDatePicker(firstweekday=6)
        date_dialog.bind(on_save=self.on_parent_end_date_save)
        date_dialog.open()

    def on_parent_start_time_save(self, instance, value):
        parent = open_json_file('display_data.json')['editing parent']
        time = time_to_string(value)
        change_json_dict_2('event_parents.json', parent, 'event start time', time)
        self.update_edit_parent(parent)

    def pick_event_start_time(self, parent):
        print(parent)
        current_start_time = get_json_dict_value2('event_parents.json', parent, 'event start time')
        open_to_time = datetime.strptime(current_start_time, "%H:%M").time()
        if open_to_time.hour < 12:
            am_pm = 'am'
        else:
            am_pm = 'pm'
        time_dialog = MDTimePicker(am_pm=am_pm)
        # MINOR BUG: I should not have to specify here whether the picker opens to am or pm. that should be done
        # automatically according to the specified set_time
        # ALSO: the minute prompt should be automatically brought up when the hour is selected, like how the old one
        # used to work


        print(open_to_time)
        time_dialog.set_time(open_to_time)
        time_dialog.bind(on_save=self.on_parent_start_time_save)
        time_dialog.open()


    def prev_week(self):
        with open('display_data.json') as json_file:
            first_day = string_to_date(json.load(json_file)["first day"])
        prev_first_day = first_day - timedelta(days=get_days_to_display())
        change_json_dict('display_data.json', 'first day', str(prev_first_day))


        self.display_week_events()

    def next_week(self):
        with open('display_data.json') as json_file:
            first_day = string_to_date(json.load(json_file)["first day"])
        next_first_day = first_day + timedelta(days=get_days_to_display())
        change_json_dict('display_data.json', 'first day', str(next_first_day))
        self.display_week_events()



    def display_week_events(self):
        with open('display_data.json') as json_file:
            first_day = string_to_date(json.load(json_file)["first day"])

        self.root.ids.weekview.clear_widgets()
        self.root.ids.time_column.clear_widgets()
        self.root.ids.weekdays.clear_widgets()

        last_sunday_0_00 = datetime.combine(first_day, datetime.min.time())
        next_sunday_23_59 = last_sunday_0_00 + timedelta(days=get_days_to_display(), seconds=-1)

        if last_sunday_0_00.month == next_sunday_23_59.month:
            month_header = str(last_sunday_0_00.strftime('%B'))
        else:
            month_header = str(last_sunday_0_00.strftime('%b')) + "—" + str(next_sunday_23_59.strftime('%b'))

        self.root.ids.weekviewToolbar.title = month_header + " " + str(next_sunday_23_59.year)


        day = first_day


        for i in range(get_days_to_display()):
            date = (day + timedelta(days=i))
            weekday = weekday_int_to_dayname((date.weekday() + 1) % 7)

            day_label = BoxLayout(orientation='vertical')

            weekday_label = MDLabel(text=str(weekday), halign='center')
            day_label.add_widget(weekday_label)
            date_label = MDLabel(text=str(date.day), halign='center')
            day_label.add_widget(date_label)

            self.root.ids.weekdays.add_widget(day_label)


        with open('events_example.json') as json_file:
            events = json.load(json_file)

        events_this_week = {}
        for event in events:
            start_time = string_to_datetime(events[event]["start time"])
            if last_sunday_0_00 < start_time < next_sunday_23_59:
                events_this_week[event] = events[event]

            end_time = string_to_datetime(events[event]["end time"])
            if last_sunday_0_00 < end_time < next_sunday_23_59:
                if event not in events_this_week:
                    events_this_week[event] = events[event]




        weekview = self.root.ids.weekview



        for i in range(24):
            y_hint = (i/24)*weekview.height
            horizontal_line = (TimeLineHorizontal(pos=(120, y_hint)))

            self.root.ids.weekview.add_widget(horizontal_line)

            #horizontal_line = (LineHorizontal(pos=(120, y_hint)))
            #self.root.ids.time_column.add_widget(horizontal_line)
            y_hint = ((i-12)/24)*weekview.height
            if i > 0:
                self.root.ids.time_column.add_widget(MDLabel(text=f"{24-i}:00", pos=(-50, y_hint), halign="right"))

        for i in range(get_days_to_display()):
            vertical_line = (LineVertical(pos_hint={"x": i/get_days_to_display(), "y": 0}))
            self.root.ids.weekview.add_widget(vertical_line)





        for event in events_this_week:

            end_datetime = string_to_datetime(events_this_week[event]["end time"])
            start_datetime = string_to_datetime(events_this_week[event]["start time"])
            end_date = end_datetime.date()
            start_date = start_datetime.date()



            event_end_time = end_datetime.time()
            event_start_time = start_datetime.time()

            event_duration = (end_datetime - start_datetime).seconds/60



            weekview_height = self.root.ids.weekview.height

            hour_height = weekview_height / 24

            event_end_time_coord = time_to_minutes(event_end_time)
            dif_from_first_day = (end_date - first_day).days
            x_coord = (dif_from_first_day)/get_days_to_display()
            y_coord = 1 - (event_end_time_coord/1440)
            #1440 is the amount of minutes in a day

            height = (event_duration/60) * hour_height

            top_of_card = y_coord*weekview_height + height
            if top_of_card < weekview_height:
                dif_from_first_day = (end_date - first_day).days
                x_coord = (dif_from_first_day) / get_days_to_display()

                self.add_new_card(events, event, height, x_coord, y_coord)
            else:
                difference = top_of_card - weekview_height
                height -= difference
                if dif_from_first_day < get_days_to_display():
                    self.add_new_card(events, event, height, x_coord, y_coord)
                else:
                    pass

                dif_from_first_day = (start_date - first_day).days
                if 0 <= dif_from_first_day:
                    x_coord = (dif_from_first_day) / get_days_to_display()

                    self.add_new_card(events, event, difference, x_coord, 0)
                else:
                    pass

        now = datetime.now()
        if last_sunday_0_00 < now < next_sunday_23_59:
            now_minutes = time_to_minutes(now)
            today = now.date()

            dif_from_first_day = (today - first_day).days

            y_pos = (1 - (now_minutes / 1440))
            y_pos_hint = (1 - (now_minutes / 1440))*weekview.height
            x_pos_hint = (dif_from_first_day)/get_days_to_display()
            now_line = NowLine(pos_hint={"x": x_pos_hint, "y": y_pos}, size_hint=((1/get_days_to_display()), None))
            weekview.add_widget(now_line)


    def day_button(self):
        print('helo')

    def add_new_card(self, events, event, height, x_coord, y_coord):
        kinds_file = open_json_file('parent_kinds.json')
        event_kind = events[event]['kind']
        kind_color = kinds_file[event_kind]['color']
        color_rgba = color_name_rgba[kind_color]


        card = MDCard(orientation='vertical',
                      height=height,
                      pos_hint={"x": x_coord, "y": y_coord},
                      size_hint=(.95 * (1 / get_days_to_display()), None),
                      elevation=0,
                      md_bg_color=(color_rgba)
                      )

        label = MDLabel(text=events[event]["summary"], adaptive_height=True, text_color=(1,1,1,1))
        #BUG. text label is supposed to be white. for some reason, it's unresponsive
        card.add_widget(label)
        card.add_widget(MDLabel(text=event, opacity=0))  # hidden id
        card.bind(on_touch_down=self.card_click)  # set binding
        self.root.ids.weekview.add_widget(card)

    def delete_parent_dialog(self, parent):
        print(parent)
        content = BoxLayout(orientation='vertical', size_hint_y=None, height='100dp')
        content.add_widget(MDLabel(text=f'Deleting the event-parent "{parent}" will delete all of its instances.'))
        dialog = MDDialog(
            title=f'Delete {parent}?',
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL", on_release=self.close_dialog
                ),
                MDRaisedButton(
                    text="DELETE", on_press=lambda x: self.delete_parent(parent)
                )
            ],
        )

        self.dialog = dialog
        self.dialog.open()

    def delete_parent(self, parent):
        self.close_dialog()
        parents = open_json_file('event_parents.json')
        parents.pop(parent)


        with open('event_parents.json', 'w') as outfile:
            json.dump(parents, outfile, indent=4)
        render_actual_events()
        self.display_week_events()
        self.go_back()

    def card_click(self, card, touch):
        if card.collide_point(*touch.pos):

            print('clicked on', card.children[0].text)
            event = card.children[0].text
            title = get_json_dict_value2('events_example.json', event, 'summary')

            content = BoxLayout(orientation='vertical', size_hint_y=None, height='100dp')
            content.add_widget(MDLabel(text=pretty_datetime_range_string(get_json_dict_value2('events_example.json', event, 'start time'), get_json_dict_value2('events_example.json', event, 'end time'))))
            parent = get_json_dict_value2('events_example.json', event, 'parent')
            print(parent)

            dialog = MDDialog(
                title=title,
                type="custom",
                content_cls= content,
                    buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.close_dialog
                    ),
                    MDRaisedButton(
                        text="PARENT", on_press=lambda x:[self.open_edit_parent(parent),self.close_dialog()]
                    ),
                    MDRaisedButton(
                        text="EVENT"
                    )
                ],
            )

            self.dialog = dialog
            self.dialog.open()

    def on_checkbox_active(self):
        print('m')

    def select_weekday(self, *args):
        content = BoxLayout(orientation='vertical', size_hint_y=None, height='100dp')
        weekday_labels = BoxLayout(orientation='horizontal')

        weekday_buttons = BoxLayout(orientation='horizontal')
        for i in range(7):

            weekday_buttons.add_widget(MDCheckbox(on_active=lambda x: self.on_checkbox_active))
            weekday_labels.add_widget(MDLabel(text=weekday_int_to_dayname(i, 'initial'), halign='center'))

        content.add_widget(weekday_labels)
        content.add_widget(weekday_buttons)
        content.add_widget(MDLabel(text=''))

        #content.add_widget(MDLabel(text='Deleting the parent event will delete all of its instances.'))
        dialog = MDDialog(
            title='Select Weekday',
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL", on_release=self.close_dialog
                ),
                MDRaisedButton(
                    text="OK", on_press=lambda x: self.save_weekday()
                )
            ],
        )

        self.dialog = dialog
        self.dialog.open()

    def save_weekday(self):
        print(self)
        pass

    def event_transition(self):
        now = datetime.now()
        now_str = str(now)
        size = len(now_str)
        now_str = now_str[:size-10]
        current_event = get_current_event()


        if current_event != "None":
            next_event = get_next_event()
            change_json_dict_2('events_example.json', current_event, 'end time', now_str)
        else:
            next_event = get_current_or_next_event()
        next_event_start_time = string_to_datetime(get_json_dict_value2('events_example.json', next_event, 'start time'))
        next_event_end_time = string_to_datetime(get_json_dict_value2('events_example.json', next_event, 'end time'))
        next_event_duration = (next_event_end_time - next_event_start_time).seconds

        change_json_dict_2('events_example.json', next_event, 'start time', now_str)
        change_json_dict_2('events_example.json', next_event, 'end time', str(now + timedelta(seconds=next_event_duration))[:size-10])


        self.display_week_events()


    def close_dialog(self, *args):
        self.dialog.dismiss()

    def build(self):

        menu_days = ["1 Day", "2 Days", "3 Days", "4 Days", "5 Days", "7 Days", "14 Days"]
        menu_items = []
        for item in menu_days:
            menu_items.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": item,
                    "height": 80,
                    "on_release": lambda x=item: self.days_menu_callback(x),
                }
            )
        self.days_menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

        kind_dict = open_json_file('parent_kinds.json')

        kind_list = []
        for kind in kind_dict:
            kind_list.append(kind)

        kind_menu_items = []
        for item in kind_list:
            kind_menu_items.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": item,
                    "height": 80,
                    "on_release": lambda x=item: self.kind_menu_select(x),
                }
            )

        self.kind_menu = MDDropdownMenu(
            items=kind_menu_items,
            width_mult=4,
        )
















        return Builder.load_file("main.kv")



if __name__ == "__main__":
    CalendarCompanionApp().run()







import flet as ft
import json
from datetime import datetime

# משתנים גלובליים
contacts = []
events = []
groups = []

class Contact:
    def __init__(self, name, phone, email="", group=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.group = group

class Event:
    def __init__(self, title, date, time, location, participants=None):
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.participants = participants or []

class Group:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.members = []

def main(page: ft.Page):
    # הגדרות בסיסיות של הדף
    page.title = "מערכת ניהול אנשי קשר ואירועים"
    page.window_width = 1200
    page.window_height = 800
    page.padding = 20
    page.rtl = True

    # משתנים מקומיים
    current_edit_contact = None
    selected_participants = []

    # פונקציות שמירה וטעינת נתונים
    def save_data():
        data = {
            "contacts": [
                {
                    "name": contact.name,
                    "phone": contact.phone,
                    "email": contact.email,
                    "group": contact.group
                }
                for contact in contacts
            ],
            "events": [
                {
                    "title": event.title,
                    "date": event.date,
                    "time": event.time,
                    "location": event.location,
                    "participants": [p.name for p in event.participants]
                }
                for event in events
            ],
            "groups": [
                {
                    "name": group.name,
                    "description": group.description,
                    "members": [member.name for member in group.members]
                }
                for group in groups
            ]
        }
        
        try:
            with open('app_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            show_message("הנתונים נשמרו בהצלחה", ft.Colors.GREEN)
        except Exception as e:
            show_message(f"שגיאה בשמירת הנתונים: {str(e)}", ft.Colors.RED)

    def load_data():
        try:
            with open('app_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # טעינת אנשי קשר
            contacts.clear()
            for contact_data in data.get("contacts", []):
                contact = Contact(
                    contact_data["name"],
                    contact_data["phone"],
                    contact_data.get("email", ""),
                    contact_data.get("group", "")
                )
                contacts.append(contact)
                
            # טעינת אירועים
            events.clear()
            for event_data in data.get("events", []):
                event = Event(
                    event_data["title"],
                    event_data["date"],
                    event_data["time"],
                    event_data["location"]
                )
                # הוספת משתתפים לאירוע
                for participant_name in event_data.get("participants", []):
                    participant = next((c for c in contacts if c.name == participant_name), None)
                    if participant:
                        event.participants.append(participant)
                events.append(event)
                
            # טעינת קבוצות
            groups.clear()
            for group_data in data.get("groups", []):
                group = Group(
                    group_data["name"],
                    group_data.get("description", "")
                )
                # הוספת חברים לקבוצה
                for member_name in group_data.get("members", []):
                    member = next((c for c in contacts if c.name == member_name), None)
                    if member:
                        group.members.append(member)
                groups.append(group)
                
            show_message("הנתונים נטענו בהצלחה", ft.Colors.GREEN)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            show_message(f"שגיאה בטעינת הנתונים: {str(e)}", ft.Colors.RED)
            return False



    # שדות טופס אנשי קשר
    name_field = ft.TextField(
        label="שם",
        width=200,
        text_align="right",
        prefix_icon=ft.icons.PERSON
    )
    
    phone_field = ft.TextField(
        label="טלפון",
        width=200,
        text_align="right",
        prefix_icon=ft.icons.PHONE
    )
    
    email_field = ft.TextField(
        label="אימייל",
        width=200,
        text_align="right",
        prefix_icon=ft.icons.EMAIL
    )

    group_field = ft.Dropdown(
        label="קבוצה",
        width=200,
        options=[
            ft.dropdown.Option("משפחה"),
            ft.dropdown.Option("חברים"),
            ft.dropdown.Option("עבודה"),
            ft.dropdown.Option("אחר")
        ]
    )

    search_field = ft.TextField(
        label="חיפוש",
        width=200,
        prefix_icon=ft.icons.SEARCH,
        on_change=lambda e: filter_contacts(e.control.value)
    )

    # שדות טופס אירועים
    event_title = ft.TextField(
        label="כותרת האירוע",
        width=200,
        text_align="right",
        prefix_icon=ft.icons.EVENT_NOTE
    )

    event_date = ft.TextField(
        label="תאריך",
        hint_text="DD/MM/YYYY",
        width=200,
        text_align="right",
        prefix_icon=ft.icons.CALENDAR_TODAY
    )

    event_time = ft.TextField(
        label="שעה",
        hint_text="HH:MM",
        width=200,
        text_align="right",
        prefix_icon=ft.icons.SCHEDULE
    )

    event_location = ft.TextField(
        label="מיקום",
        width=200,
        text_align="right",
        prefix_icon=ft.icons.LOCATION_ON
    )

    # שדות טופס קבוצות
    group_name_field = ft.TextField(
        label="שם הקבוצה",
        width=300,
        text_align="right",
        prefix_icon=ft.icons.GROUP
    )

    group_description_field = ft.TextField(
        label="תיאור הקבוצה",
        width=300,
        text_align="right",
        multiline=True,
        prefix_icon=ft.icons.DESCRIPTION
    )

    # רשימות תצוגה
    contacts_list_view = ft.ListView(expand=True, spacing=10, padding=20, height=400)
    events_grid_view = ft.GridView(
        expand=True,
        runs_count=2,
        max_extent=400,
        child_aspect_ratio=2.0,
        spacing=10,
        run_spacing=10,
        padding=20,
        height=400
    )
    participants_list_view = ft.ListView(height=150, spacing=5)
    groups_list_view = ft.ListView(expand=True, spacing=10, padding=20, height=400)




        

    def show_message(message, color):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        page.snack_bar.open = True
        page.update()

    def filter_contacts(search_text):
        if not search_text:
            contacts_list_view.controls = [create_contact_card(contact) for contact in contacts]
        else:
            filtered = [
                contact for contact in contacts
                if search_text.lower() in contact.name.lower() or
                   search_text in contact.phone or
                   search_text.lower() in contact.email.lower()
            ]
            contacts_list_view.controls = [create_contact_card(contact) for contact in filtered]
        page.update()

    def edit_contact(contact):
        nonlocal current_edit_contact
        current_edit_contact = contact
        name_field.value = contact.name
        phone_field.value = contact.phone
        email_field.value = contact.email
        group_field.value = contact.group
        filter_contacts("")
        page.update()

    def delete_contact(contact):
        contacts.remove(contact)
        filter_contacts("")
        update_participants_list()
        show_message("איש הקשר נמחק בהצלחה", ft.Colors.RED)
        page.update()

    def create_contact_card(contact):
        is_selected = contact == current_edit_contact
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.icons.PERSON,
                            color=ft.Colors.BLUE if is_selected else ft.Colors.BLACK,
                            size=30
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    contact.name,
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(f"טלפון: {contact.phone}"),
                                ft.Text(f"אימייל: {contact.email}" if contact.email else ""),
                                ft.Text(f"קבוצה: {contact.group}" if contact.group else "")
                            ],
                            spacing=5,
                            expand=True
                        ),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.Colors.BLUE,
                                    tooltip="ערוך",
                                    on_click=lambda _, c=contact: edit_contact(c)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    tooltip="מחק",
                                    on_click=lambda _, c=contact: delete_contact(c)
                                )
                            ],
                            spacing=0
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=10,
                bgcolor=ft.Colors.BLUE_50 if is_selected else None
            )
        )

    def create_event_card(event):
        return ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.icons.EVENT, color=ft.Colors.BLUE),
                    title=ft.Text(
                        event.title,
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),
                    subtitle=ft.Text(f"תאריך: {event.date}\nשעה: {event.time}\nמיקום: {event.location}")
                ),
                padding=10,
                on_click=lambda e: manage_event(event)  # ה-on_click צריך להיות כאן, בתוך ה-Container
            )
        )

    def toggle_participant(e, contact):
        if e.control.value:
            selected_participants.append(contact)
        else:
            selected_participants.remove(contact)

    def update_participants_list():
        participants_list_view.controls = [
            ft.Checkbox(
                label=contact.name,
                on_change=lambda e, c=contact: toggle_participant(e, c)
            )
            for contact in contacts
        ]
        page.update()

    def create_group_card(group):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.GROUP, color=ft.Colors.BLUE),
                        title=ft.Text(
                            group.name,
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),
                        subtitle=ft.Column([
                            ft.Text(group.description) if group.description else ft.Text("אין תיאור"),
                            ft.Text(f"מספר חברים: {len(group.members)}", weight=ft.FontWeight.BOLD),
                            ft.Text("חברי הקבוצה:", weight=ft.FontWeight.BOLD),
                            ft.Text(", ".join([member.name for member in group.members]) if group.members else "אין חברים בקבוצה")
                        ])
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "כניסה לקבוצה",
                                icon=ft.icons.LOGIN,
                                on_click=lambda e, g=group: enter_group(g)
                            ),
                            ft.ElevatedButton(
                                "ערוך קבוצה",
                                icon=ft.icons.EDIT,
                                on_click=lambda e, g=group: edit_group(g)
                            ),
                            ft.ElevatedButton(
                                "מחק קבוצה",
                                icon=ft.icons.DELETE,
                                bgcolor=ft.Colors.RED,
                                color=ft.Colors.WHITE,
                                on_click=lambda e, g=group: delete_group(g)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ]),
                padding=10
            )
        )
    
    def add_or_update_contact(e):
        nonlocal current_edit_contact
        if not name_field.value:
            show_message("אנא הזן שם!", ft.Colors.RED)
            return
        if not phone_field.value:
            show_message("אנא הזן מספר טלפון!", ft.Colors.RED)
            return

        if current_edit_contact:
            # הסרה מהקבוצה הקודמת אם הייתה
            if current_edit_contact.group:
                old_group = next((g for g in groups if g.name == current_edit_contact.group), None)
                if old_group and current_edit_contact in old_group.members:
                    old_group.members.remove(current_edit_contact)

            current_edit_contact.name = name_field.value
            current_edit_contact.phone = phone_field.value
            current_edit_contact.email = email_field.value
            current_edit_contact.group = group_field.value
            contact = current_edit_contact
            show_message("איש הקשר עודכן בהצלחה", ft.Colors.GREEN)
            current_edit_contact = None
        else:
            contact = Contact(
                name_field.value,
                phone_field.value,
                email_field.value,
                group_field.value
            )
            contacts.append(contact)
            show_message("איש הקשר נוסף בהצלחה", ft.Colors.GREEN)

        # הוספה לקבוצה החדשה
        if contact.group:
            new_group = next((g for g in groups if g.name == contact.group), None)
            if new_group and contact not in new_group.members:
                new_group.members.append(contact)

        name_field.value = ""
        phone_field.value = ""
        email_field.value = ""
        group_field.value = None
    
        # עדכון כל התצוגות
        filter_contacts("")
        groups_list_view.controls = [create_group_card(g) for g in groups]
        update_participants_list()
        page.update()
        save_data()

    def add_event(e):
        if not event_title.value:
            show_message("אנא הזן כותרת לאירוע!", ft.Colors.RED)
            return
        if not event_date.value:
            show_message("אנא הזן תאריך!", ft.Colors.RED)
            return
        if not event_time.value:
            show_message("אנא הזן שעה!", ft.Colors.RED)
            return

        new_event = Event(
            event_title.value,
            event_date.value,
            event_time.value,
            event_location.value,
            []
        )
        events.append(new_event)
        events_grid_view.controls.append(create_event_card(new_event))           

        event_title.value = ""
        event_date.value = ""
        event_time.value = ""
        event_location.value = ""

        
        show_message("האירוע נוסף בהצלחה", ft.Colors.GREEN)
        page.update()
        save_data()
        
    def add_group(e):
        if not group_name_field.value:
            show_message("אנא הזן שם קבוצה!", ft.Colors.RED)
            return

        new_group = Group(
            group_name_field.value,
            group_description_field.value
        )
        groups.append(new_group)
        groups_list_view.controls.append(create_group_card(new_group))
    
        # עדכון אפשרויות הקבוצה בטופס אנשי הקשר
        update_group_options()
    
        group_name_field.value = ""
        group_description_field.value = ""
        
        show_message("הקבוצה נוספה בהצלחה", ft.Colors.GREEN)
        page.update()
        save_data()

    def update_group_options():
        # מחיקת כל האפשרויות הקיימות
        group_field.options.clear()
        
        # הוספת האפשרויות הבסיסיות
        default_options = ["משפחה", "חברים", "עבודה"]
        for option in default_options:
            group_field.options.append(ft.dropdown.Option(option))
        
        # הוספת הקבוצות מהמערכת
        for group in groups:
            if group.name not in default_options:
                group_field.options.append(ft.dropdown.Option(group.name))
        
        # הוספת אפשרות "אחר" בסוף
        if not any(option.key == "אחר" for option in group_field.options):
            group_field.options.append(ft.dropdown.Option("אחר"))
        
        # עדכון הממשק
        page.update()

    def edit_group(group):
        group_name_field.value = group.name
        group_description_field.value = group.description
        page.update()

    def delete_group(group):
        groups.remove(group)
        groups_list_view.controls = [create_group_card(g) for g in groups]
    
        # עדכון אפשרויות הקבוצה בטופס אנשי הקשר
        update_group_options()
    
        # עדכון אנשי הקשר שהיו בקבוצה שנמחקה
        for contact in contacts:
            if contact.group == group.name:
                contact.group = ""
    
        show_message("הקבוצה נמחקה בהצלחה", ft.Colors.RED)
        page.update()
        save_data()

    def manage_group_members(group):
        dlg = ft.AlertDialog(
            title=ft.Text(f"ניהול חברים בקבוצה: {group.name}"),
            content=ft.Column(
                [
                    ft.Text("בחר חברים לקבוצה:"),
                    ft.Column([
                        ft.Checkbox(
                            label=contact.name,
                            value=contact in group.members,
                            on_change=lambda e, c=contact: toggle_group_member(e, group, c)
                        )
                        for contact in contacts
                    ], scroll=ft.ScrollMode.AUTO, height=200)
                ],
                tight=True
            )
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def toggle_group_member(e, group, contact):
        if e.control.value:
            if contact not in group.members:
                group.members.append(contact)
                # עדכון הקבוצה של איש הקשר
                contact.group = group.name
        else:
            if contact in group.members:
                group.members.remove(contact)
                # איפוס הקבוצה של איש הקשר אם הוא הוסר
                contact.group = ""
    
        # עדכון התצוגה של הקבוצות ואנשי הקשר
        groups_list_view.controls = [create_group_card(g) for g in groups]
        contacts_list_view.controls = [create_contact_card(c) for c in contacts]
        page.update()
        save_data() 
 

    def enter_group(group):
        dlg = ft.AlertDialog(
            title=ft.Text(f"קבוצה: {group.name}"),
            content=ft.Column(
                [
                    ft.Text("חברי הקבוצה:"),
                    ft.Column([
                        ft.Checkbox(
                            label=contact.name,
                            value=contact in group.members,
                            on_change=lambda e, c=contact: toggle_group_member(e, group, c)
                        )
                        for contact in contacts
                    ], scroll=ft.ScrollMode.AUTO, height=200)
                ],
                tight=True
            )
        )
        page.dialog = dlg
        dlg.open = True
        page.update()
        
    def manage_event(event):
        # נוסיף מילון לשמירת סטטוס המשתתפים
        participant_status = {p: "confirmed" for p in event.participants}
        pending_participants = []  # רשימת ממתינים לאישור

        def close_event_tab(e):
            tabs.tabs = [tab for tab in tabs.tabs if tab.text != f"אירוע: {event.title}"]
            tabs.selected_index = 2
            page.update()

        def toggle_contact_selection(e, contact):
            if e.control.value and contact not in event.participants and contact not in pending_participants:
                pending_participants.append(contact)
            elif not e.control.value:
                if contact in pending_participants:
                    pending_participants.remove(contact)
                if contact in event.participants:
                    event.participants.remove(contact)
                    participant_status.pop(contact, None)
            update_event_participants()
            save_data()

        def confirm_participation(contact):
            if contact in pending_participants:
                pending_participants.remove(contact)
                event.participants.append(contact)
                participant_status[contact] = "confirmed"
                update_event_participants()
                save_data()

        def remove_participant(participant):
            if participant in event.participants:
                event.participants.remove(participant)
                participant_status.pop(participant, None)
            if participant in pending_participants:
                pending_participants.remove(participant)
            update_event_participants()
            save_data()

        # רשת המשתתפים הנוכחיים
        participants_grid = ft.GridView(
            expand=True,
            runs_count=2,
            max_extent=300,
            child_aspect_ratio=2.0,
            spacing=10,
            run_spacing=10,
            padding=20,
            height=200
        )

        # רשת אנשי קשר שעוד לא נבחרו
        available_contacts_grid = ft.GridView(
            expand=True,
            runs_count=2,
            max_extent=300,
            child_aspect_ratio=2.0,
            spacing=10,
            run_spacing=10,
            padding=20,
            height=200,
            visible=False
        )

        def toggle_contacts_view(e):
            available_contacts_grid.visible = not available_contacts_grid.visible
            page.update()

        def update_event_participants():
            # עדכון רשת המשתתפים (מאושרים + ממתינים)
            all_participants = []
            
            # משתתפים מאושרים
            for participant in event.participants:
                all_participants.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                                    ft.Column(
                                        [
                                            ft.Text(participant.name, size=16, weight=ft.FontWeight.BOLD),
                                            ft.Text(f"טלפון: {participant.phone}"),
                                            ft.Text(f"אימייל: {participant.email}" if participant.email else ""),
                                            ft.Text("מאושר", color=ft.Colors.GREEN)
                                        ],
                                        spacing=5,
                                        expand=True
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        icon_color=ft.Colors.RED,
                                        tooltip="הסר מהאירוע",
                                        on_click=lambda _, p=participant: remove_participant(p)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            padding=10,
                            bgcolor=ft.colors.GREEN_50
                        )
                    )
                )
            
            # משתתפים ממתינים לאישור
            for participant in pending_participants:
                all_participants.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.PENDING, color=ft.Colors.ORANGE),
                                    ft.Column(
                                        [
                                            ft.Text(participant.name, size=16, weight=ft.FontWeight.BOLD),
                                            ft.Text(f"טלפון: {participant.phone}"),
                                            ft.Text(f"אימייל: {participant.email}" if participant.email else ""),
                                            ft.Text("ממתין לאישור", color=ft.Colors.ORANGE)
                                        ],
                                        spacing=5,
                                        expand=True
                                    ),
                                    ft.Row(
                                        [
                                            ft.IconButton(
                                                icon=ft.icons.CHECK,
                                                icon_color=ft.Colors.GREEN,
                                                tooltip="אשר השתתפות",
                                                on_click=lambda _, p=participant: confirm_participation(p)
                                            ),
                                            ft.IconButton(
                                                icon=ft.icons.DELETE,
                                                icon_color=ft.Colors.RED,
                                                tooltip="הסר מהאירוע",
                                                on_click=lambda _, p=participant: remove_participant(p)
                                            )
                                        ]
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            padding=10,
                            bgcolor=ft.colors.ORANGE_50
                        )
                    )
                )
            
            participants_grid.controls = all_participants

            # עדכון רשת אנשי הקשר הזמינים
            available_contacts = [
                contact for contact in contacts 
                if contact not in event.participants and contact not in pending_participants
            ]
            
            available_contacts_grid.controls = [
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Checkbox(
                                    value=False,
                                    on_change=lambda e, c=contact: toggle_contact_selection(e, c)
                                ),
                                ft.Column(
                                    [
                                        ft.Text(contact.name, size=16, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"טלפון: {contact.phone}"),
                                        ft.Text(f"אימייל: {contact.email}" if contact.email else ""),
                                        ft.Text(f"קבוצה: {contact.group}" if contact.group else "")
                                    ],
                                    spacing=5,
                                    expand=True
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        padding=10
                    )
                ) for contact in available_contacts
            ]
            page.update()

        def remove_participant(participant):
            event.participants.remove(participant)
            update_event_participants()
            save_data()

        event_management_content = ft.Column([
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.TextField(
                                label="כותרת האירוע",
                                value=event.title,
                                width=200,
                                text_align="right"
                            ),
                            padding=5
                        ),
                        ft.Container(
                            content=ft.TextField(
                                label="תאריך",
                                value=event.date,
                                width=200,
                                text_align="right"
                            ),
                            padding=5
                        ),
                        ft.Container(
                            content=ft.TextField(
                                label="שעה",
                                value=event.time,
                                width=200,
                                text_align="right"
                            ),
                            padding=5
                        ),
                        ft.Container(
                            content=ft.TextField(
                                label="מיקום",
                                value=event.location,
                                width=200,
                                text_align="right"
                            ),
                            padding=5
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.CLOSE,
                                    icon_color=ft.Colors.GREY,
                                    tooltip="סגור כרטיסייה",
                                    on_click=close_event_tab
                                )
                            ]),
                            padding=5
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=10
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column([
                    ft.Row(
                        [
                            ft.Text("משתתפים באירוע:", size=20, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton(
                                "הוסף משתתפים",
                                icon=ft.icons.PERSON_ADD,
                                on_click=toggle_contacts_view
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    participants_grid,
                    ft.Divider(),
                    available_contacts_grid
                ])
            )
        ])

        # בדיקה אם הכרטיסייה כבר קיימת
        for tab in tabs.tabs:
            if tab.text == f"אירוע: {event.title}":
                tabs.selected_index = tabs.tabs.index(tab)
                page.update()
                return

        # יצירת כרטיסייה חדשה
        new_tab = ft.Tab(
            text=f"אירוע: {event.title}",
            icon=ft.icons.EVENT,
            content=event_management_content
        )

        tabs.tabs.append(new_tab)
        tabs.selected_index = len(tabs.tabs) - 1
        update_event_participants()
        page.update()
        
        # כפתורים
    add_contact_button = ft.ElevatedButton(
        text="+",
        icon=ft.icons.PERSON_ADD,
        on_click=add_or_update_contact,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )

    add_event_button = ft.ElevatedButton(
        text="+",
        icon=ft.icons.EVENT_AVAILABLE,
        on_click=add_event,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )

    add_group_button = ft.ElevatedButton(
        text="+",
        icon=ft.icons.GROUP_ADD,
        on_click=add_group,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )

    # טופס אנשי קשר
    contacts_form = ft.Column([
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=add_contact_button,
                        padding=ft.padding.only(right=10)
                    ),
                    ft.Container(
                        content=name_field,
                        width=200,
                        padding=5
                    ),
                    ft.Container(
                        content=phone_field,
                        width=200,
                        padding=5
                    ),
                    ft.Container(
                        content=email_field,
                        width=200,
                        padding=5
                    ),
                    ft.Container(
                        content=group_field,
                        width=200,
                        padding=5
                    ),
                    ft.Container(
                        content=search_field,
                        padding=ft.padding.only(left=10)
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
         ),
        ft.Container(
            content=contacts_list_view,
            expand=True,
            margin=ft.margin.all(10),
            border=ft.border.all(1, ft.Colors.BLACK12),
            border_radius=10,
            padding=10
        )
    ])

    events_form = ft.Column([
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=add_event_button,
                            padding=ft.padding.only(right=10)
                        ),
                        ft.Container(
                            content=event_title,
                            width=200,
                            padding=5
                        ),
                        ft.Container(
                            content=event_date,
                            width=200,
                            padding=5
                        ),
                        ft.Container(
                            content=event_time,
                            width=200,
                            padding=5
                        ),
                        ft.Container(
                            content=event_location,
                            width=200,
                            padding=5
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=10,
            ),
            ft.Container(
                content=events_grid_view,  # שימוש ב-events_grid_view שהגדרנו בתחילת הקוד
                expand=True,
                margin=ft.margin.all(10),
                border=ft.border.all(1, ft.colors.BLACK12),
                border_radius=10,
                padding=10
            )
        ])
    # טופס קבוצות
    groups_form = ft.Column([
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=add_group_button,
                        padding=ft.padding.only(right=10)
                    ),
                    ft.Container(
                        content=group_name_field,
                        padding=5
                    ),
                    ft.Container(
                        content=group_description_field,
                        padding=5
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            padding=10
        ),
        ft.Container(
            content=groups_list_view,
            expand=True,
            margin=ft.margin.all(10),
            border=ft.border.all(1, ft.Colors.BLACK12),
            border_radius=10,
            padding=10
        )
    ])

    # כרטיסיות
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="אנשי קשר",
                icon=ft.icons.PEOPLE,
                content=contacts_form
            ),
            ft.Tab(
                text="קבוצות",
                icon=ft.icons.GROUPS,
                content=groups_form
            ),
            ft.Tab(
                text="אירועים",
                icon=ft.icons.EVENT,
                content=events_form
            ),
        ],
        expand=1
    )

    # ניסיון לטעון נתונים קיימים
    if load_data():
        # עדכון התצוגה עם הנתונים שנטענו
        contacts_list_view.controls = [create_contact_card(contact) for contact in contacts]
        events_grid_view.controls = [create_event_card(event) for event in events]
        groups_list_view.controls = [create_group_card(group) for group in groups]
        update_group_options()  # עדכון אפשרויות הקבוצה בדרופדאון    

    # הוספת התוכן לדף
    page.add(
        ft.Text(
            "מערכת ניהול אנשי קשר ואירועים",
            size=30,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        ),
        tabs
    )

ft.app(target=main)

import flet as ft
import json
import os
import requests
from github import Github
from datetime import datetime
import base64

class LoginManager:
    def __init__(self):
        self.github_token = "YOUR_GITHUB_TOKEN"  # יש להחליף בטוקן אמיתי של GitHub
        self.repo_name = "DARTYQO/people"
        self.data_folder = "DATA"
        self.current_user = None
        
    def create_login_page(self, page: ft.Page, on_login_success):
        page.title = "התחברות למערכת"
        page.window_width = 400
        page.window_height = 600
        page.padding = 20
        page.rtl = True
        
        # שדות טופס התחברות
        username_field = ft.TextField(
            label="שם משתמש",
            width=300,
            text_align="right",
            prefix_icon=ft.icons.PERSON
        )
        
        password_field = ft.TextField(
            label="סיסמה",
            width=300,
            password=True,
            text_align="right",
            prefix_icon=ft.icons.LOCK
        )
        
        error_text = ft.Text(
            color=ft.colors.RED,
            size=12
        )
        
        def try_login(e):
            if self.validate_user(username_field.value, password_field.value):
                self.current_user = username_field.value
                on_login_success()
            else:
                error_text.value = "שם משתמש או סיסמה שגויים"
                page.update()
                
        def show_register(e):
            self.create_register_page(page, on_login_success)
            
        login_form = ft.Column(
            [
                ft.Text(
                    "ברוכים הבאים",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                username_field,
                password_field,
                error_text,
                ft.ElevatedButton(
                    "התחבר",
                    width=300,
                    on_click=try_login
                ),
                ft.TextButton(
                    "אין לך חשבון? הירשם כאן",
                    on_click=show_register
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        page.controls = [login_form]
        page.update()
        
    def create_register_page(self, page: ft.Page, on_register_success):
        page.controls.clear()
        
        username_field = ft.TextField(
            label="שם משתמש",
            width=300,
            text_align="right",
            prefix_icon=ft.icons.PERSON
        )
        
        password_field = ft.TextField(
            label="סיסמה",
            width=300,
            password=True,
            text_align="right",
            prefix_icon=ft.icons.LOCK
        )
        
        confirm_password_field = ft.TextField(
            label="אימות סיסמה",
            width=300,
            password=True,
            text_align="right",
            prefix_icon=ft.icons.LOCK
        )
        
        error_text = ft.Text(
            color=ft.colors.RED,
            size=12
        )
        
        def try_register(e):
            if password_field.value != confirm_password_field.value:
                error_text.value = "הסיסמאות אינן תואמות"
                page.update()
                return
                
            if self.register_user(username_field.value, password_field.value):
                self.current_user = username_field.value
                on_register_success()
            else:
                error_text.value = "שם המשתמש כבר קיים"
                page.update()
                
        def back_to_login(e):
            self.create_login_page(page, on_register_success)
            
        register_form = ft.Column(
            [
                ft.Text(
                    "הרשמה למערכת",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                username_field,
                password_field,
                confirm_password_field,
                error_text,
                ft.ElevatedButton(
                    "הירשם",
                    width=300,
                    on_click=try_register
                ),
                ft.TextButton(
                    "חזרה להתחברות",
                    on_click=back_to_login
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        page.controls = [register_form]
        page.update()
        
    def validate_user(self, username, password):
        try:
            g = Github(self.github_token)
            repo = g.get_repo(self.repo_name)
            users_file = repo.get_contents(f"{self.data_folder}/users.json")
            users_data = json.loads(base64.b64decode(users_file.content).decode())
            
            if username in users_data:
                return users_data[username]["password"] == password
            return False
        except:
            return False
            
    def register_user(self, username, password):
        try:
            g = Github(self.github_token)
            repo = g.get_repo(self.repo_name)
            
            try:
                users_file = repo.get_contents(f"{self.data_folder}/users.json")
                users_data = json.loads(base64.b64decode(users_file.content).decode())
            except:
                users_data = {}
                
            if username in users_data:
                return False
                
            users_data[username] = {
                "password": password,
                "created_at": datetime.now().isoformat()
            }
            
            # עדכון קובץ המשתמשים
            repo.update_file(
                f"{self.data_folder}/users.json",
                f"Added new user: {username}",
                json.dumps(users_data, indent=4, ensure_ascii=False),
                users_file.sha if users_file else None
            )
            
            # יצירת תיקיית נתונים למשתמש
            empty_data = {
                "contacts": [],
                "events": [],
                "groups": []
            }
            
            try:
                repo.create_file(
                    f"{self.data_folder}/{username}/data.json",
                    f"Initialize data for user: {username}",
                    json.dumps(empty_data, indent=4, ensure_ascii=False)
                )
            except:
                pass
                
            return True
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            return False
            
    def load_user_data(self):
        if not self.current_user:
            return None
            
        try:
            g = Github(self.github_token)
            repo = g.get_repo(self.repo_name)
            data_file = repo.get_contents(f"{self.data_folder}/{self.current_user}/data.json")
            return json.loads(base64.b64decode(data_file.content).decode())
        except:
            return None
            
    def save_user_data(self, data):
        if not self.current_user:
            return False
            
        try:
            g = Github(self.github_token)
            repo = g.get_repo(self.repo_name)
            data_file = repo.get_contents(f"{self.data_folder}/{self.current_user}/data.json")
            
            repo.update_file(
                f"{self.data_folder}/{self.current_user}/data.json",
                f"Update data for user: {self.current_user}",
                json.dumps(data, indent=4, ensure_ascii=False),
                data_file.sha
            )
            return True
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return False
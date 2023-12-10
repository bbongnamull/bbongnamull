import os
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

TODO_FILE = "todo_list.json"
LAST_RUN_DATE_FILE = "last_run_date.txt"

def get_email_credentials():
    email_address = input("Enter your email address: ")
    email_password = input("Enter your email password: ")
    recipient_email = input("Enter the recipient's email address: ")

    return email_address, email_password, recipient_email

def save_todo_list(todo_list):
    with open(TODO_FILE, 'w') as file:
        json.dump(todo_list, file)

def load_todo_list():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

def save_last_run_date(current_date):
    with open(LAST_RUN_DATE_FILE, 'w') as file:
        file.write(current_date)

def load_last_run_date():
    if os.path.exists(LAST_RUN_DATE_FILE):
        with open(LAST_RUN_DATE_FILE, 'r') as file:
            return file.read().strip()
    else:
        return None

def send_email(subject, body, sender_email, sender_password, recipient_email):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")

    finally:
        server.quit()

def check_and_send_reminder(todo_list, sender_email, sender_password, recipient_email):
    current_time = datetime.now()
    overdue_tasks = [todo for todo in todo_list if todo["due_date"] and todo["due_date"] < current_time and not todo["completed"]]

    if overdue_tasks:
        subject = "Overdue Tasks Reminder"
        body = "The following tasks are overdue:\n\n"
        for task in overdue_tasks:
            body += f"- {task['task']} (Due: {task['due_date'].strftime('%Y-%m-%d %H:%M')})\n"

        send_email(subject, body, sender_email, sender_password, recipient_email)

def initialize_todo_list():
    last_run_date = load_last_run_date()
    current_date = datetime.now().strftime('%Y-%m-%d')

    if last_run_date is None or last_run_date != current_date:
        print("Initializing todo list...")
        save_last_run_date(current_date)
        return []
    else:
        return load_todo_list()



def display_menu():
    print("1. Add Task")
    print("2. Display Task List")
    print("3. Mark Task as Completed")
    print("4. Delete Task")
    print("5. View Completed Tasks")
    print("6. View Overdue Tasks")
    print("7. Export Task List")
    print("8. Exit")

def add_todo(todo_list):
    task = input("Enter the task: ")
    due_date_str = input("Enter due date and time (YYYY-MM-DD HH:MM): ")
    
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date format. Task added without due date.")
        due_date = None
    
    priority = input("Enter priority (High/Medium/Low): ").lower()
    
    todo_list.append({"task": task, "completed": False, "due_date": due_date, "priority": priority})
    print("Task added successfully.")

def display_todo_list(todo_list, show_completed=False):
    filtered_list = [todo for todo in todo_list if todo["completed"] == show_completed]
    
    if not filtered_list:
        print("No tasks.")
    else:
        for i, todo in enumerate(filtered_list, 1):
            status = "Completed" if todo["completed"] else "Not Completed"
            due_date = todo["due_date"].strftime("%Y-%m-%d %H:%M") if todo["due_date"] else "No Due Date"
            priority = todo["priority"].capitalize() if todo["priority"] in ["high", "medium", "low"] else "Not Set"
            
            print(f"{i}. {todo['task']} ({status}, Due: {due_date}, Priority: {priority})")

def mark_completed(todo_list):
    display_todo_list(todo_list)
    choice = int(input("Enter the number of the completed task: ")) - 1

    if 0 <= choice < len(todo_list):
        todo_list[choice]["completed"] = True
        print("Task marked as completed.")
    else:
        print("Invalid task number.")

def delete_todo(todo_list):
    display_todo_list(todo_list)
    choice = int(input("Enter the number of the task to delete: ")) - 1

    if 0 <= choice < len(todo_list):
        del todo_list[choice]
        print("Task deleted.")
    else:
        print("Invalid task number.")

def view_completed_tasks(todo_list):
    display_todo_list(todo_list, show_completed=True)

def view_overdue_tasks(todo_list):
    current_time = datetime.now()
    overdue_tasks = [todo for todo in todo_list if todo["due_date"] and todo["due_date"] < current_time and not todo["completed"]]
    
    if not overdue_tasks:
        print("No overdue tasks.")
    else:
        for i, todo in enumerate(overdue_tasks, 1):
            due_date = todo["due_date"].strftime("%Y-%m-%d %H:%M") if todo["due_date"] else "No Due Date"
            print(f"{i}. {todo['task']} (Due: {due_date})")

def export_task_list(todo_list):
    export_format = input("Enter export format (JSON/CSV): ").lower()
    
    if export_format == "json":
        export_file = input("Enter export file name (e.g., export.json): ")
        with open(export_file, 'w') as file:
            json.dump(todo_list, file)
        print(f"Task list exported to {export_file}.")
    elif export_format == "csv":
        export_file = input("Enter export file name (e.g., export.csv): ")
        with open(export_file, 'w') as file:
            file.write("Task,Status,Due Date,Priority\n")
            for todo in todo_list:
                status = "Completed" if todo["completed"] else "Not Completed"
                due_date = todo["due_date"].strftime("%Y-%m-%d %H:%M") if todo["due_date"] else "No Due Date"
                priority = todo["priority"].capitalize() if todo["priority"] in ["high", "medium", "low"] else "Not Set"
                file.write(f"{todo['task']},{status},{due_date},{priority}\n")
        print(f"Task list exported to {export_file}.")
    else:
        print("Invalid export format.")

def main():
    sender_email, sender_password, recipient_email = get_email_credentials()
    todo_list = initialize_todo_list()

    while True:
        display_menu()
        choice = input("Enter the number corresponding to your choice: ")

        if choice == '1':
            add_todo(todo_list)
        elif choice == '2':
            display_todo_list(todo_list)
        elif choice == '3':
            mark_completed(todo_list)
        elif choice == '4':
            delete_todo(todo_list)
        elif choice == '5':
            view_completed_tasks(todo_list)
        elif choice == '6':
            view_overdue_tasks(todo_list)
        elif choice == '7':
            export_task_list(todo_list)
        elif choice == '8':
            check_and_send_reminder(todo_list, sender_email, sender_password, recipient_email)
            save_todo_list(todo_list)
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
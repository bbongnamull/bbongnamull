import os
import json
from datetime import datetime
import matplotlib.pyplot as plt




TODO_FILE = "todo_list.json"

def save_todo_list(todo_list):
    with open(TODO_FILE, 'w') as file:
        json.dump(todo_list, file)

def load_todo_list():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

def display_menu():
    print("1. 할일 추가")
    print("2. 할일 목록 표시")
    print("3. 할일 완료 체크")
    print("4. 할일 삭제")
    print("5. 날짜별 할일 달성 현황 그래프 표시")
    print("6. 종료")

def add_todo(todo_list):
    num_tasks = int(input("추가할 할일의 수를 입력하세요: "))
    
    for _ in range(num_tasks):
        todo = input("추가할 할일을 입력하세요: ")
        if todo.strip():
            todo_list.append({"task": todo, "completed": False})
        else:
            print("할일을 입력하세요.")

    print(f"{num_tasks}개의 할일이 추가되었습니다.")


def display_todo_list(todo_list):
    if not todo_list:
        print("할일이 없습니다.")
    else:
        for i, todo in enumerate(todo_list, 1):
            status = "완료" if todo["completed"] else "미완료"
            print(f"{i}. {todo['task']} ({status})")

def mark_completed(todo_list):
    display_todo_list(todo_list)
    num_completed = int(input("완료할 할일의 수를 입력하세요: "))

    for _ in range(num_completed):
        choice = int(input("완료한 할일의 번호를 입력하세요: ")) - 1

        if 0 <= choice < len(todo_list):
            todo_list[choice]["completed"] = True
            todo_list[choice]["completion_date"] = datetime.now().strftime("%Y-%m-%d")
            print("할일이 완료로 표시되었습니다.")
        else:
            print("잘못된 번호를 입력하셨습니다.")
def delete_todo(todo_list):
    display_todo_list(todo_list)
    choice = int(input("삭제할 할일의 번호를 입력하세요: ")) - 1

    if 0 <= choice < len(todo_list):
        del todo_list[choice]
        print("할일이 삭제되었습니다.")
    else:
        print("잘못된 번호를 입력하셨습니다.")
def display_datewise_graph(todo_list):
    date_completion_dict = {}

    for todo in todo_list:
        completion_date = todo.get("completion_date")
        if completion_date:
            completion_date_str = datetime.strptime(completion_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            date_completion_dict[completion_date_str] = date_completion_dict.get(completion_date_str, 0) + 1

    dates = list(date_completion_dict.keys())
    completions = list(date_completion_dict.values())

    plt.bar(dates, completions, color='green')
    plt.xlabel('날짜')
    plt.ylabel('할일 완료 수')
    plt.title('날짜별 할일 달성 현황')
    plt.xticks(rotation=45)
    plt.show()

def mark_completed(todo_list):
    display_todo_list(todo_list)
    choice = int(input("완료한 할일의 번호를 입력하세요: ")) - 1

    if 0 <= choice < len(todo_list):
        todo_list[choice]["completed"] = True
        todo_list[choice]["completion_date"] = datetime.now().strftime("%Y-%m-%d")
        print("할일이 완료로 표시되었습니다.")
    else:
        print("잘못된 번호를 입력하셨습니다.")


def main():
    todo_list = load_todo_list()

    while True:
        display_menu()
        choice = input("원하는 작업의 번호를 입력하세요: ")

        if choice == '1':
            add_todo(todo_list)
        elif choice == '2':
            display_todo_list(todo_list)
        elif choice == '3':
            mark_completed(todo_list)
        elif choice == '4':
            delete_todo(todo_list)
        elif choice == '5':
            display_datewise_graph(todo_list)
        elif choice == '6':
            save_todo_list(todo_list)
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()
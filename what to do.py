import os

def display_menu():
    print("1. 할일 추가")
    print("2. 할일 목록 표시")
    print("3. 할일 완료 체크")
    print("4. 할일 삭제")
    print("5. 종료")

def add_todo(todo_list):
    todo = input("추가할 할일을 입력하세요: ")
    todo_list.append({"task": todo, "completed": False})
    print("할일이 추가되었습니다.")

def display_todo_list(todo_list):
    if not todo_list:
        print("할일이 없습니다.")
    else:
        for i, todo in enumerate(todo_list, 1):
            status = "완료" if todo["completed"] else "미완료"
            print(f"{i}. {todo['task']} ({status})")

def mark_completed(todo_list):
    display_todo_list(todo_list)
    choice = int(input("완료한 할일의 번호를 입력하세요: ")) - 1

    if 0 <= choice < len(todo_list):
        todo_list[choice]["completed"] = True
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

def main():
    todo_list = []

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
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()

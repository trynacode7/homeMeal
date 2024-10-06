from gui.login_page import login_page
from gui.register_page import register_page

def main():
    choice = input("Enter 1 to Register, 2 to Login: ")
    if choice == "1":
        register_page()
    elif choice == "2":
        login_page()
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
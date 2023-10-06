def get_confirmation(string) -> bool:
    print(f"You picked {string}.")
    user_input = input("Confirm? y/n: ")
    return user_input.strip().lower() in ("yes", "y")
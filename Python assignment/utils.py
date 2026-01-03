def validate_input(prompt, options, case_sensitive=False):

    while True:
        user_input = input(prompt).strip()

        if not case_sensitive:
            user_input = user_input.upper()
            options = [opt.upper() for opt in options]

        if user_input in options:
            return user_input

        print(f"Invalid input! Please choose from {', '.join(options)}")


def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{int(mins)}m {int(secs)}s"

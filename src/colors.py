# Defining ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

# Text colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Background colors
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Bright text colors
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Bright background colors
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"



"""
# Example usage
print(f"{RED}This is red text{RESET}")
print(f"{GREEN}This is green text{RESET}")
print(f"{BLUE}This is blue text{RESET}")
print(f"{YELLOW}This is yellow text{RESET}")
print(f"{MAGENTA}This is magenta text{RESET}")
print(f"{CYAN}This is cyan text{RESET}")
print(f"{WHITE}This is white text{RESET}")

# Bold and Underlined text
print(f"{BOLD}{RED}This is bold red text{RESET}")
print(f"{UNDERLINE}{BLUE}This is underlined blue text{RESET}")

# Background colors
print(f"{BG_RED}{WHITE}This is red background with white text{RESET}")
print(f"{BG_BLUE}{YELLOW}This is blue background with yellow text{RESET}")

# Bright colors
print(f"{BRIGHT_RED}This is bright red text{RESET}")
print(f"{BRIGHT_GREEN}This is bright green text{RESET}")

# Bright background colors
print(f"{BG_BRIGHT_BLUE}{BLACK}This is bright blue background with black text{RESET}")
"""
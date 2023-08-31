from termcolor import colored

#set logging values
LOG_TRUE = colored("DONE", "green")
LOG_FALSE = colored("FAILED", "red")
LOG_WARNING = colored("FAILED", "red")

def log_true(message):
    print(f"{message} [{LOG_TRUE}]")

def log_false(message):
    print(f"{message} [{LOG_FALSE}]")

def log_warn(message):
    print(f"{message} [{LOG_WARNING}]")
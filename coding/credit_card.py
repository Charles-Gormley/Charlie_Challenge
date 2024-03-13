###### Imports ######
import re

##### Functions #####
def is_valid_credit_card(number: int):
    ''' Function which processes a Regex pattern to validate credit card numbers
    Args:
        number: A string representing a credit card number
    Returns:
        A boolean value: True if the credit card number is valid, False otherwise
    '''
    # regex_pattern = r"^(?!.*(\d)(-?\1){3})[456]\d{3}(-?\d{4}){3}$" # Original regex pattern
    regex_pattern = r"^"                    # Asserts the start of the string
    regex_pattern += r"(?!.*(\d)(-?\1){3})" # Negative lookahead to prevent more than 3 consecutive repeated digits, considering hyphens
    regex_pattern += r"[456]"               # Checks if the string starts with 4, 5, or 6
    regex_pattern += r"\d{3}"               # Follows the initial digit with three more digits (making the first group of 4 digits in total)
    regex_pattern += r"(-?\d{4}){3}"        # Matches three more groups of four digits, possibly separated by a single hyphen
    regex_pattern += r"$"                   # Asserts the end of the string
    
    return re.match(regex_pattern, number) is not None

def main():
    ''' Main function to read the input and process the credit card numbers'''
    # Read the first line to get the number of credit card numbers to validate
    n = int(input().strip())
    
    # Process each credit card number
    for _ in range(n):
        number = input().strip() # Read the credit card number
        if is_valid_credit_card(number): # Check if the credit card number is valid
            print("Valid") 
        else:
            print("Invalid")

##### Main #####
if __name__ == "__main__":
    main()
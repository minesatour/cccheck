import random
import os
import re

# Constants for file names
BANK_API_FILE = "bankapi.txt"
CARDS_FILE = "cards.txt"
BIN_FILE = "BIN.txt"
VALID_CARDS_FILE = "valid.txt"

URL_PATTERN = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# Load data from files
def load_file(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return []
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"Error: {e}")
        return []

# Save data to files
def save_file(filename, data):
    try:
        with open(filename, "w") as file:
            for item in data:
                file.write(str(item) + "\n")
    except Exception as e:
        print(f"Error: {e}")

# Generate a random credit card number with a valid BIN (first 6 digits)
def generate_credit_card(bin_number):
    random_digits = "".join(str(random.randint(0, 9)) for _ in range(10))  # Generate 10 random digits
    return bin_number + random_digits

# Validate a credit card number using Luhn algorithm
def is_valid_credit_card_luhn(card_number):
    card_number = re.sub(r"\D", "", card_number)  # Remove non-digit characters
    if len(card_number) != 16:
        return False
   
    checksum = 0
    even_digits = False
    for digit in reversed(card_number):
        digit = int(digit)
        if even_digits:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
        even_digits = not even_digits
   
    return checksum % 10 == 0

# Validate a credit card number using ISO/IEC 7812 standards
def is_valid_credit_card_iso_7812(card_number):
    iin = card_number[:6]  # Extract the Issuer Identification Number (IIN)
    # Sample IIN ranges for validation (can be expanded based on actual data)
    valid_iins = ['400000', '411111', '510000']
    return iin in valid_iins

# Combined validation function using multiple algorithms
def is_valid_credit_card_super(card_number):
    return (
        is_valid_credit_card_luhn(card_number) and
        is_valid_credit_card_iso_7812(card_number)
    )

# Menu option to add a bank API to the bankapi.txt file
def add_bank_api():
    bank_api = input("Enter Bank API URL: ")
    if not URL_PATTERN.match(bank_api):
        print("Error: Invalid URL.")
        return
    bank_apis = load_file(BANK_API_FILE)
    bank_apis.append(bank_api)
    save_file(BANK_API_FILE, bank_apis)
    print("Bank API added successfully.")

# Menu option to add multiple credit card numbers to cards.txt
def add_credit_cards():
    try:
        num_cards = int(input("Enter the number of credit cards to add: "))
        if num_cards <= 0:
            raise ValueError("Number of cards must be a positive integer.")
        cards = load_file(CARDS_FILE)
        bins = load_file(BIN_FILE)
        for _ in range(num_cards):
            cards.append(generate_credit_card(random.choice(bins)))
        save_file(CARDS_FILE, cards)
        print(f"{num_cards} credit cards generated and added.")
    except ValueError as e:
        print(f"Error: {e}")

# Menu option to add multiple BIN numbers to BIN.txt
def add_bin_numbers():
    try:
        num_bins = int(input("Enter the number of BIN numbers to add: "))
        if num_bins <= 0:
            raise ValueError("Number of BIN numbers must be a positive integer.")
        bins = load_file(BIN_FILE)
        for _ in range(num_bins):
            bin_number = input("Enter BIN number: ")
            if len(bin_number) != 6 or not bin_number.isdigit():
                print("Error: BIN number must be a 6-digit number.")
                continue
            bins.append(bin_number)
        save_file(BIN_FILE, bins)
        print(f"{num_bins} BIN numbers added.")
    except ValueError as e:
        print(f"Error: {e}")

# Menu option to create valid credit cards using BIN.txt file
def create_credit_cards():
    bins = load_file(BIN_FILE)
    try:
        num_cards = int(input("Enter the number of credit cards to create: "))
        if num_cards <= 0:
            raise ValueError("Number of cards must be a positive integer.")
        cards = []
        for i in range(num_cards):
            bin_number = random.choice(bins)
            cards.append(generate_credit_card(bin_number))
            print(f"Generated {i+1} out of {num_cards} credit cards.")
        save_file(CARDS_FILE, cards)
        print(f"{num_cards} credit cards generated and saved.")
    except ValueError as e:
        print(f"Error: {e}")

# Menu option to check and save valid credit cards using combined validation
def check_and_save_valid_cards():
    cards = load_file(CARDS_FILE)
    valid_cards = []
    for i, card in enumerate(cards, start=1):
        if is_valid_credit_card_super(card):
            valid_cards.append(card)
        print(f"Checked {i} out of {len(cards)} credit cards.")
   
    if valid_cards:
        save_valid_cards(valid_cards)
        print(f"{len(valid_cards)} valid credit cards saved to {VALID_CARDS_FILE}.")
    else:
        print("No valid credit cards found.")

# Save valid credit cards to valid.txt
def save_valid_cards(valid_cards):
    try:
        with open(VALID_CARDS_FILE, "w") as file:
            for card in valid_cards:
                expiry_date = f"{random.randint(1, 12)}/{random.randint(22, 25)}"  # Example expiry date
                cvv = f"{random.randint(100, 999)}"  # Example CVV
                balance = f"${random.randint(100, 10000):.2f}"  # Example balance
                file.write(f"{card} {expiry_date} {cvv} {balance}\n")
    except Exception as e:
        print(f"Error: {e}")

# Display menu options
def display_menu():
    print("\n1. Add Bank API")
    print("2. Add Credit Cards")
    print("3. Add BIN Numbers")
    print("4. Create Credit Cards")
    print("5. Check and Save Valid Cards")
    print("6. View Bank APIs")
    print("7. View BIN Numbers")
    print("8. View Generated Cards")
    print("9. View Valid Cards")
    print("10. Clear Data")
    print("11. Exit")

# Main function to run the script
def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-11): ")
        if choice == "1":
            add_bank_api()
        elif choice == "2":
            add_credit_cards()
        elif choice == "3":
            add_bin_numbers()
        elif choice == "4":
            create_credit_cards()
        elif choice == "5":
            check_and_save_valid_cards()
        elif choice == "6":
            view_bank_apis()
        elif choice == "7":
            view_bin_numbers()
        elif choice == "8":
            view_generated_cards()
        elif choice == "9":
            view_valid_cards()
        elif choice == "10":
            clear_data()
        elif choice == "11":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 11.")

if __name__ == "__main__":
    main()




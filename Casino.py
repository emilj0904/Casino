import random
from time import sleep
from pathlib import Path

# MISCELLANEOUS

def deduct_bet(balance):
    while True:
        bet = input("Make your bet: £")
        if not bet.isdigit() or int(bet) < 0:
            print("Invalid bet. Try again.")
            continue
        bet = int(bet)
        if bet > balance:
            print("Insufficient funds. Try again.")
            continue
        break

    balance -= bet

    return balance, bet 





# 1 - SLOTS

def slot_num_rounds():
    print("Welcome to: SLOTS")
    while True:
        rounds = input("How many rounds? ")
        if not rounds.isdigit():
            print("Invalid number. Try again.")
            continue
        rounds = int(rounds)
        if not 1 <= rounds <= 10:
            print("Please do between 1 and 10 rounds.")
            continue
        break
    
    print("----------------------------------")

    return rounds


def slot_game(rounds, balance):
    selections = ("🍒", "🍋", "🔔", "⭐", "💎", "7")

    for counter in range(rounds):
        balance, bet = deduct_bet(balance)
        print("Spinning...")
        sleep(0.5)
        print()

        row = [random.choice(selections) for selection in range(3)]
        print(" | ".join(row))
        print()

        balance = slot_outcome(row, bet, balance)
        
        print(f"New balance: £{balance}")
        print("--------------------")

        if balance == 0:
            break

    sleep(2)

    return balance
    

def slot_outcome(row, bet, balance):
    if row[0] == row[1] == row[2]:
        if row[0] == "7":
            print("JACKPOT!!!")
            print("JACKPOT!!!")
            print("JACKPOT!!!")
            balance += 1000 * bet
            print(f"You won £{1000 * bet}!")
        elif row[0] == "💎":
            print("Three diamonds!")
            balance += 50 * bet
            print(f"You won £{50 * bet}!")
        else:
            print("Triple!")
            balance += 15 * bet
            print(f"You won £{15 * bet}!")
    
    elif row[0] == row[1] or row[1] == row[2] or row[0] == row[2]:
        print("Pairs!")
        balance += 2 * bet
        print(f"You won £{2 * bet}!")

    else:
        print("No luck.")

    return balance





# 2 - BLACKJACK

# Algorithms:

def blac_deal_one_card(hand_cards, hand_suits, cards, suits):
    index = random.randint(0, len(cards) - 1)
    hand_cards.append(cards[index])
    hand_suits.append(suits[index])
    cards.pop(index)
    suits.pop(index)

    return hand_cards, hand_suits, cards, suits


def blac_calculate_pts(hand_cards):
    points = 0
    aces = 0

    for card in hand_cards:
        if card in ("2", "3", "4", "5", "6", "7", "8", "9"):
            points += int(card)
        elif card in ("X", "J", "Q", "K"):
            points += 10
        else:
            points += 11
            aces += 1

    while points > 21 and aces > 0:
        points -= 10
        aces -= 1

    return points


def blac_display_cards(cards, suits, hide_cards=False):
    if not hide_cards:
        print("┌─────┐ " * len(cards))
        for counter in range(len(cards)):
            print(f"│ {cards[counter]}{suits[counter]}  │", end = " ")
        print()
        print("└─────┘ " * len(cards))
    else:
        print("┌─────┐ " * len(cards))
        print(f"│ {cards[0]}{suits[0]}  │", end = " ")
        print("│  ?  │ " * (len(cards) - 1))
        print("└─────┘ " * len(cards))


def blac_hit_or_stand():
    hitting = input("Hit or stand? ").upper()
    while hitting not in ("HIT", "STAND", "H", "S"):
        print("Invalid input. Try 'HIT' or 'STAND'.")
        hitting = input("Hit or stand? ").upper()
        
    hitting = True if hitting == 'HIT' or hitting == 'H' else False

    return hitting


# Game:

def blac_game(balance):
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "X", "J", "Q", "K"] * 4
    suits = ["♥️"] * 13 + ["♦️"] * 13 + ["♣️"] * 13 + ["♠️"] * 13

    dealer_cards = []
    dealer_suits = []
    player_cards = []
    player_suits = []

    print("Welcome to: BLACKJACK")
    balance, bet = deduct_bet(balance)
    print("----------------------------------")

    player_cards, player_suits, cards, suits = blac_deal_one_card(player_cards, player_suits, cards, suits)
    dealer_cards, dealer_suits, cards, suits = blac_deal_one_card(dealer_cards, dealer_suits, cards, suits)
    dealer_cards, dealer_suits, cards, suits = blac_deal_one_card(dealer_cards, dealer_suits, cards, suits)

    hitting = True
    player_pts = 0
    player_bust = False
    dealer_bust = False

    while hitting:
        player_cards, player_suits, cards, suits = blac_deal_one_card(player_cards, player_suits, cards, suits)
        player_pts = blac_calculate_pts(player_cards)

        print("Dealer:")
        blac_display_cards(dealer_cards, dealer_suits, True)
        print()
        print("Player:")
        blac_display_cards(player_cards, player_suits)
        print(f"You have {player_pts} points.")

        if player_pts > 21:
            player_bust = True
            break
        else:
            hitting = blac_hit_or_stand()
            print("----------------------------------")

    if not player_bust:
        print("It is now the dealer's turn.")
        sleep(1)
        dealer_bust, dealer_cards, dealer_suits, cards, suits, dealer_pts = blac_dealers_turn(dealer_cards, dealer_suits, cards, suits)
        print("----------------------------------")

    sleep(1)

    if dealer_bust:
        balance = blac_dealer_bust(dealer_cards, dealer_suits, dealer_pts, balance, bet)
    elif player_bust:
        print("You went bust! No luck.")
    else:
        balance = blac_compare_hands(dealer_cards, dealer_suits, player_cards, player_suits, dealer_pts, player_pts, bet, balance)

    sleep(2)
    return balance


def blac_dealers_turn(dealer_cards, dealer_suits, cards, suits):
    dealer_bust = False
    
    dealer_pts = blac_calculate_pts(dealer_cards)
    while dealer_pts < 17:
        dealer_cards, dealer_suits, cards, suits = blac_deal_one_card(dealer_cards, dealer_suits, cards, suits)
        dealer_pts = blac_calculate_pts(dealer_cards)

        if dealer_pts > 21:
            dealer_bust = True
            break

    return dealer_bust, dealer_cards, dealer_suits, cards, suits, dealer_pts


# Outcomes:

def blac_dealer_bust(dealer_cards, dealer_suits, dealer_pts, balance, bet):
    print("Dealer:")
    blac_display_cards(dealer_cards, dealer_suits)
    print()
    print(f"Dealer went bust at {dealer_pts} points. You win!")
    balance += 2 * bet
    print(f"You won £{2 * bet}!")

    return balance


def blac_compare_hands(dealer_cards, dealer_suits, player_cards, player_suits, dealer_pts, player_pts, bet, balance):
    print("Dealer:")
    blac_display_cards(dealer_cards, dealer_suits)
    print(f"The dealer had {dealer_pts} points.")
    print()
    print("Player:")
    blac_display_cards(player_cards, player_suits)
    print(f"You had {player_pts} points.")

    if dealer_pts > player_pts:
        print("The dealer had more points. No luck.")
    elif dealer_pts < player_pts:
        print("You had more points. You win!")
        balance += 2 * bet
        print(f"You won £{2 * bet}!")
    else:
        print("It's a tie.")
        balance += bet
        print(f"You won your bet back.")

    return balance





# 3 - ROULETTE

def roul_bet_type():
    print("Welcome to: ROULETTE")
    print("What would you like to bet on?")
    print("1. A number")
    print("2. A colour")
    print("3. The parity")
    bet_type = input("\n")

    while bet_type not in ('1', '2', '3'):
        print("Invalid choice. Try again.")
        bet_type = input()

    return bet_type
    

def roul_get_win_cond(bet_type):
    if bet_type == '1':
        choice = input("Select a number: ")
        while not choice.isdigit() or not 0 <= int(choice) <= 36:
            print("Choose a whole number between 0 and 36.")
            choice = input("Select a number: ")

    elif bet_type == '2':
        choice = input("Pick a colour: ").upper()
        while choice not in ("BLACK", "RED", "B", "R"):
            print("Invalid input. Try 'BLACK' or 'RED'.")
            choice = input("Select a colour: ").upper()

        choice = '⬛' if choice == 'BLACK' or choice == 'B' else '🟥'

    else:
        choice = input("Choose a parity: ").upper()
        while choice not in ("ODD", "EVEN", "O", "E"):
            print("Invalid input. Try 'ODD' or 'EVEN'.")
            choice = input("Choose a parity: ").upper()

        choice = 'O' if choice == 'ODD' or choice == 'O' else 'E'

    return choice
    

def roul_game(balance):
    roulette_cols = ("🟩", 
                     "🟥", "⬛", "🟥", "⬛", "🟥", "⬛", "🟥", "⬛", "🟥",
                     "⬛", "⬛", "🟥", "⬛", "🟥", "⬛", "🟥", "⬛", "🟥",
                     "🟥", "⬛", "🟥", "⬛", "🟥", "⬛", "🟥", "⬛", "🟥",
                     "⬛", "⬛", "🟥", "⬛", "🟥", "⬛", "🟥", "⬛", "🟥")

    balance, bet = deduct_bet(balance)
    print("Rolling...")
    sleep(1)
    print()
    roll = random.randint(0, 36)
    print(roll, roulette_cols[roll])
    print()

    return roll, roulette_cols[roll], bet, balance


def roul_outcome(bet_type, win_cond, balance, bet, roll, colour):
    # Outcome for correct number
    if bet_type == '1':
        if str(roll) == win_cond:
            print("You guessed the right number!")
            balance += 36 * bet
            print(f"You won £{36 * bet}!")
        else:
            print("No luck.")
    
    # Outcome for correct colour
    elif bet_type == '2':
        if win_cond == colour:
            print(f"You guessed the right colour!")
            balance += 2 * bet
            print(f"You won £{2 * bet}!")
        else:
            print("No luck.")

    # Outcome for correct parity
    else:
        if ((roll % 2 == 0 and win_cond == 'E') or (roll % 2 != 0 and win_cond == 'O')) and roll != 0:
            print(f"You guessed the right parity!")
            balance += 2 * bet
            print(f"You won £{2 * bet}!")
        else:
            print("No luck.")

    print("----------------------------------")
    sleep(2)

    return balance





# 4 - BAR

def view_drink_menu():
    menu = {"Lager": 7,
            "Gin and Tonic": 10,
            "Martini": 14,
            "Mojito": 13,
            "Margarita": 11,
            "Pina Colada": 10,
            "Old Fashioned": 17,
            "Cosmopolitan": 15,
            "Aperol Spritz": 11,
            "Scotch Whiskey": 23,
            "Sex on the Beach": 14,
            "Rum and Coke": 15,
            "Strawberry Daiquiri": 9,
            "Cranberry Juice": 3,
            "Tom Pearl Special": 50}

    print("DRINKS MENU:")
    print()
    for drink, price in menu.items():
        print(f"{drink:<20} - £{price}")

    return menu


def order_drink(menu, balance):
    item_found = False
    
    while not item_found:
        print()
        print("Type 'EXIT' to leave the bar.")
        print("Type 'MENU' to view the menu again.")
        order = input("Pick a drink: ").lower().replace(" ", "")
        for drink in menu.keys():
            if drink.lower().replace(" ", "") == order:
                item_found = True
                print()
                print(f"You ordered a {drink} for £{menu.get(drink)}")
                display_message()
                sleep(1)
                print("----------------------------------")
                balance -= menu.get(drink)

                break
        
        if order.upper() == "MENU":
            view_drink_menu()
        if order.upper() == "EXIT":
            print("----------------------------------")
            break

        if not item_found:
            print()
            print("That's not on the menu. Try again.")

    sleep(2)

    return balance


def display_message():
    messages = ("You ferociously guzzle the drink. Have some self respect.",
                "You're so drunk you vomit just before the entrance to the toilets.",
                "You sip on the drink performatively.",
                "You bitterly grumble at the bartender for underfilling the glass.",
                "You spill half of the drink on yourself.",
                "You catch someone trying to roofie your drink.",
                "You hand the drink to a hot girl and tell her it's 'on you'. She throws it in your face and calls you a creep.",
                "The bartender stares at you in horror.",
                "You're so drunk you're starting to see double.",
                "You feel a sudden, strong urge to pee.",
                "You finish the drink in 30 seconds and start to regret paying so much.",
                "You make eye contact with someone across the bar. You stare at each other awkwardly.",
                "Your drunkeness convinces you to bet everything on red.",
                "You begin planning a hangover cure in advance.",
                "The drink tastes horrible.",
                "It's made exactly how you like it.",
                "You suspect the bartender spat in it.",
                "'I can quit whenever I want', you pathetically try to convince yourself.",
                "You tell yourself this is the last drink before you quit.",
                "As you finish the drink, you remember you need to drive home.",)
    
    print(random.choice(messages))



# MAIN MENU

def import_balance():
    with open(Path(__file__).parent / "balance.txt", "r") as file:
        balance = int(file.read())

    return balance


def home(balance):
    is_playing = True

    print("----------------------------------")
    print("Welcome to the casino.")

    while is_playing and balance > 0:
        print(f"Your balance is £{balance}")
        print("----------------------------------")
        sleep(1)

        print("Select a choice. Your options are:")
        print("1. Slots 🎰")
        print("2. Blackjack ♦️")
        print("3. Roulette 🛞")
        print("4. Buy a drink 🍸")
        print("5. Leave the casino 🥺")
        choice = input("\n")
        print("----------------------------------")

        if choice == '1':
            rounds = slot_num_rounds()
            balance = slot_game(rounds, balance)

        elif choice == '2':
            balance = blac_game(balance)

        elif choice == '3':
            bet_type = roul_bet_type()
            win_cond = roul_get_win_cond(bet_type)
            roll, colour, bet, balance = roul_game(balance)
            balance = roul_outcome(bet_type, win_cond, balance, bet, roll, colour)

        elif choice == '4':
            print("Welcome to: THE BAR")
            print("----------------------------------")
            sleep(1)
            menu = view_drink_menu()
            balance = order_drink(menu, balance)

        elif choice == '5':
            is_playing = False

        else:
            print("That's not a valid choice. Please try again.")
            sleep(1)
            print("----------------------------------")
            continue

    if balance == 0:
        print("----------------------------------")
        print("You've went bankrupt!")
        return 100
    else:
        return balance


def export_balance(balance):
    with open(Path(__file__).parent / "balance.txt", "w") as file:
        file.write(str(balance))

    print("Your balance has been saved.")


def main():
    balance = import_balance()
    balance = home(balance)
    export_balance(balance)

main()
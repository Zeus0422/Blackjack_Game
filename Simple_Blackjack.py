import random
import sys

# Tracks the number of each card type that has been chosen, assuming a single deck.
card_counts = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}
# Initial bet amount for the game.
bet_amount = 10


def main():
    # Initialize game by reading the player's current bankroll from a file.
    read_bankroll_from_file()

    # Define the deck of cards available in this game.
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

    # Initialize empty hands for the player (pc) and dealer (dc).
    pc = []  # Player's current hand
    dc = []  # Dealer's current hand

    # Tracks if the player overbought in any split hands. Initially, all values are set to 0 (no overbought).
    ob = [0, 0, 0, 0]
    # Split counter, unused in this simplified version.
    sp = 0

    # Begin the game by dealing initial cards to the player and the dealer.
    pc, dc = deal(cards, pc, dc)
    # Proceed to the main gameplay loop.
    play(cards, pc, dc, ob)


def read_bankroll_from_file():
    # Declare 'bankroll' as a global variable to modify its value within this function.
    global bankroll

    try:
        # Attempt to open the 'bankroll.txt' file to read the player's bankroll.
        with open('bankroll.txt', 'r') as file:
            content = file.read()
            # Split the file content on '=' symbol to extract the bankroll value.
            parts = content.split('=')

            if len(parts) != 2:
                # Ensure the file format is as expected; otherwise, raise an error.
                raise ValueError("Invalid format in the file")
            value = parts[1].strip()

            try:
                # Convert the extracted value to an integer and assign it to 'bankroll'.
                bankroll = int(value)
            except ValueError:
                # Handle the case where the value is not a valid integer.
                raise ValueError("Value in the file is not an integer")

    except FileNotFoundError:
        # Handle the case where the 'bankroll.txt' file does not exist.
        print("Error: File 'bankroll.txt' not found")

    except Exception as e:
        # Catch all other exceptions and print an error message.
        print("An error occurred:", e)


def deal(cards, pc, dc):
    # Access the global 'bankroll' variable to potentially modify it based on game outcomes.
    global bankroll

    # Assign two randomly chosen cards to both player and dealer.
    pc = [choose_card(), choose_card()]

    # Convert any Aces from 11 to 1 if necessary and print the player's hand.
    convert_ace(pc)
    print_hand("", pc)

    # Dealer receives two cards, with the second card hidden from the player.
    dc = [random.choice(cards), random.choice(cards)]
    print_hand(0, dc)
    print()

    # Check for a blackjack condition at the start of the game.
    if pc[0] + pc[1] == 21 and dc[0] + dc[1] != 21:
        # Player has a blackjack and wins the game immediately.
        print("Blackjack!")
        print_hand("", pc)
        print_hand(10, dc)

        # Update the player's bankroll in the file to reflect the win.
        update_bankroll_in_file("w", bankroll)
        sys.exit()

    if pc[0] + pc[1] == 21 and dc[0] + dc[1] == 21:
        # Both player and dealer have blackjack, resulting in a push (tie).
        print("Push:", sum(pc), "vs", sum(dc))

        # Update the player's bankroll in the file to reflect the push.
        update_bankroll_in_file("p", bankroll)

        sys.exit()

    return pc, dc


def choose_card():
    # Access the global 'card_counts' dictionary to track chosen cards.
    global card_counts

    # Create a list of available cards that have been chosen less than 4 times.
    available_cards = [card for card, count in card_counts.items() if count < 4]

    if available_cards:
        # Randomly select an available card and increment its count in 'card_counts'.
        chosen_card = random.choice(available_cards)
        card_counts[chosen_card] += 1
        return chosen_card

    else:
        # Raise an exception if no cards are available, indicating a logical error in the game's design.
        raise Exception("No more cards available to choose.")


def print_hand(hand_number, hand):
    # Print the hand based on the provided 'hand_number' identifier.
    if hand_number == 0:
        # Print the dealer's initial hand with one card hidden.
        print(f"Dealer_Hand: {hand[0]}, ?")

    elif hand_number == "":
        # Print the player's hand.
        print(f"Player_Hand: ", end="")
        for i, item in enumerate(hand[:-1]):
            print(f"{hand[i]}, ", end="")
        print(hand[-1])

    elif hand_number == 10:
        # Print the dealer's hand after taking their turn.
        print("Dealer_Hand: ", end="")
        for i, item in enumerate(hand[:-1]):
            print(f"{hand[i]}, ", end="")
        print(hand[-1])

    else:
        # Print a player's hand after a split.
        print(f"Player_{hand_number}: ", end="")
        for i, item in enumerate(hand[:-1]):
            print(f"{hand[i]}, ", end="")
        print(hand[-1])


def play(cards, pc, dc, ob):
    # Access the global 'bankroll' variable for potential modification during the game.
    global bankroll

    # Prompt the player for their next action, offering different options based on the game state.
    if pc[0] == pc[1]:
        choice = input("Type 'h' to hit, Type 's' to stay, Type 'd' to double or Type 'sp' to split: ")
    else:
        choice = input("Type 'h' to hit, Type 's' to stay or Type 'd' to double: ")

    if choice.lower() == "s":
        # Player chooses to stay, ending their turn.
        print("Stay", end="\n\n")
        convert_ace(pc)
        print_hand("", pc)

        dealer(cards, dc)
        compare_hand("", pc, dc)

    elif choice.lower() == "h":
        # Player chooses to hit, receiving an additional card.
        pc = hit(cards, pc, dc)

        dealer(cards, dc)
        if ob[0] == 0:
            compare_hand("", pc, dc)

    elif choice.lower() == "d":
        # Player chooses to double their bet and receive one additional card.
        pc = double(cards, pc, dc)

        dealer(cards, dc)
        compare_hand("", pc, dc)

    if choice.lower() == "sp":
        # Add two more cards to the player's hand for the split.
        # These cards are added to facilitate the creation of two separate hands.
        pc.append(choose_card())
        pc.append(choose_card())

        # Inform the player that their hand has been split into two new hands, each beginning with one of the original paired cards.
        print("Split, Hand1:", pc[0], "and", pc[2])
        print("Split, Hand2:", pc[1], "and", pc[3], end="\n\n")

        # Process the first split hand. This involves taking the first and third cards as the new Hand1.
        hand1, sp = split("Hand1", cards, [pc[0], pc[2]], ob)

        if sp == 1:  # If the player decides to split Hand1 again.
            print("Hand1, Split", end="\n\n")
            # The first hand is split again, and new cards are dealt to create two new hands from Hand1.
            hand1, sp1 = split("Hand1", cards, [pc[0], choose_card()], ob)

            # If the player splits the first hand again, process the additional hands created from the original Hand1.
            if sp1 == 1:
                hand1, sp11 = split("Hand1", cards, [pc[0], choose_card()], ob)
                hand2, sp12 = split("Hand2", cards, [pc[1], choose_card()], ob)
                # Additional splits from Hand1 could lead to the creation of Hand3 and Hand4, depending on player choices.
                hand3, sp13 = split("Hand3", cards, [pc[0], choose_card()], ob)
                hand4, sp14 = split("Hand4", cards, [pc[1], pc[3]], ob)

            else:
                # If the player does not choose to split Hand1 again, Hand2 is processed with the second and fourth cards.
                hand2, sp2 = split("Hand2", cards, [pc[1], choose_card()], ob)

                if sp2 == 1:  # If the player decides to split Hand2.
                    print("Hand2, Split", end="\n\n")
                    hand2, sp22 = split("Hand2", cards, [pc[1], choose_card()], ob)
                    hand3, sp23 = split("Hand3", cards, [pc[2], choose_card()], ob)
                    hand4, sp24 = split("Hand4", cards, [pc[3], choose_card()], ob)

                else:
                    # If Hand2 is not split again, process additional hands as needed based on player choices.
                    hand3, sp3 = split("Hand3", cards, [pc[2], choose_card()], ob)
                    if sp3 == 1:
                        hand3, sp33 = split("Hand3", cards, [pc[2], choose_card()], ob)
                        hand4, sp34 = split("Hand4", cards, [pc[3], choose_card()], ob)

        else:
            # If the player does not split the initial Hand1, proceed to create and process Hand2 with the originally paired cards.
            hand2, sp = split("Hand2", cards, [pc[1], pc[3]], ob)

            if sp == 1:  # Check if the player decides to split the newly formed Hand2.
                print("Hand2, Split", end="\n\n")
                hand2, sp2 = split("Hand2", cards, [pc[1], choose_card()], ob)

                # Further processing of splits from Hand2, creating additional hands based on player decisions.
                if sp2 == 1:
                    hand2, sp22 = split("Hand2", cards, [pc[1], choose_card()], ob)
                    hand3, sp23 = split("Hand3", cards, [pc[2], choose_card()], ob)
                    hand4, sp24 = split("Hand4", cards, [pc[3], choose_card()], ob)

                else:
                    hand3, sp3 = split("Hand3", cards, [pc[2], choose_card()], ob)
                    if sp3 == 1:
                        hand3, sp23 = split("Hand3", cards, [pc[2], choose_card()], ob)
                        hand4, sp24 = split("Hand4", cards, [pc[3], choose_card()], ob)

        # Theoretically, more than three splits are possible, but this simplified version does not implement them.

        # Determine the outcome for each hand, checking for overbought situations.
        if ob[0] == 0:
            dealer(cards, dc)
        elif ob[1] == 0:
            dealer(cards, dc)
        elif ob[2] == 0:
            if 'hand3' in locals():  # This checks if the variable 'hand3' is defined to prevent errors.
                dealer(cards, dc)
        elif ob[3] == 0:
            if 'hand4' in locals():
                dealer(cards, dc)
        else:
            print("Dealer_Card_1 =", dc[0])

        # Compare each hand to the dealer's hand to determine the outcome.
        if ob[0] == 0:
            compare_hand("Hand1", hand1, dc)
        if ob[0] == 1:
            print_hand("Hand1", hand1)
            print("Overbought", end="\n\n")
            update_bankroll_in_file("l", bankroll)

        if ob[1] == 0:
            compare_hand("Hand2:", hand2, dc)
        if ob[1] == 1:
            print_hand("Hand2", hand2)
            print("Overbought", end="\n\n")
            update_bankroll_in_file("l", bankroll)

        if 'hand3' in locals():
            if ob[2] == 0:
                compare_hand("Hand3:", hand3, dc)
            if ob[2] == 1:
                print_hand("Hand3", hand3)
                print("Overbought", end="\n\n")
                update_bankroll_in_file("l", bankroll)

        if 'hand4' in locals():
            if ob[3] == 0:
                compare_hand("Hand4:", hand4, dc)
            if ob[3] == 1:
                print_hand("Hand4", hand4)
                print("Overbought", end="\n\n")
                update_bankroll_in_file("l", bankroll)


def hit(cards, pc, dc):
    global bankroll

    # The hit function allows the player to take additional cards until they decide to stay or bust.
    while True:
        pc.append(random.choice(cards))
        print(f"Hit, Player_card_{len(pc)} =", pc[-1])

        pc = convert_ace(pc)  # Adjust for Aces being 11 or 1 as needed.
        print()
        print_hand("", pc)  # Print the updated hand after each hit.
        print_hand(0, dc)  # Show the dealer's visible card.

        if sum(pc) > 21:
            print("\nOverbought, Dealer wins")
            print_hand(10, dc)  # Show the dealer's full hand if the player busts.
            print()

            update_bankroll_in_file("l", bankroll)  # Update the bankroll file for a loss.

            sys.exit()  # Exit the game if the player busts.

        choice = input("\nType 'h' to hit or Type 's' to stay: ")
        if choice.lower() == "s":
            print("Stay", end="\n\n")
            print_hand("", pc)  # Print the player's final hand if they choose to stay.
            break  # Exit the loop if the player decides to stay.

    return pc  # Return the player's hand after hitting or staying.


def double(cards, pc, dc):
    global bet_amount
    global bankroll

    bet_amount *= 2  # Double the bet amount for the current hand.

    pc.append(random.choice(cards))  # Add one card to the player's hand.
    print("Double, Player_card_3 =", pc[2])

    pc = convert_ace(pc)  # Adjust for Aces being 11 or 1 as needed.
    print()
    print_hand("", pc)  # Print the player's hand after doubling.

    if sum(pc) > 21:
        print_hand(0, dc)  # Show the dealer's visible card if the player busts.
        print("\nOverbought, Dealer wins")
        print_hand(10, dc)  # Show the dealer's full hand.
        print()

        update_bankroll_in_file("l", bankroll)  # Update the bankroll file for a loss.
        sys.exit()  # Exit the game if the player busts.

    return pc  # Return the player's hand after doubling.


def split(hand, cards, pc, ob):
    sp = 0
    # Determine which hand is being split based on the 'hand' argument.
    if hand == "Hand1":
        i = 0
    elif hand == "Hand2":
        i = 1
    elif hand == "Hand3":
        i = 2
    elif hand == "Hand4":
        i = 3

    # Check if the two cards in the hand are of the same value, allowing for a split.
    if pc[0] == pc[1]:
        choice2 = input(f"{hand}: {pc[0]} and {pc[1]}, Type 'h' to hit, Type 's' to stay, Type 'd' to double or type 'sp' to split again: ").lower()
        if choice2 == "sp":
            sp = 1  # Indicates a split occurred; this variable is not fully utilized in this version.
            return pc, sp

    else:
        choice2 = input(f"{hand}: {pc[0]} and {pc[1]}, Type 'h' to hit, Type 's' to stay or Type 'd' to double: ").lower()

    if choice2 == "h":
        # Allow the player to hit multiple times after splitting.
        while True:
            pc.append(choose_card())
            print(f"Hit, Player_card_{len(pc)} =", pc[-1])

            pc = convert_ace(pc)  # Adjust for Aces being 11 or 1 as needed.

            if sum(pc) > 21:
                print()
                print_hand(hand, pc)  # Show the hand that went over.
                print("Overbought, Dealer wins", end="\n\n")
                ob[i] = 1  # Mark the hand as overbought.
                break  # Exit the loop if the player busts.

            print()
            print_hand(hand, pc)  # Print the hand after each hit.

            choice = input("Type 'h' to hit or Type 's' to stay: ")
            if choice.lower() == "s":
                print(f"Stay, {hand}: ", end="")
                print_hand(hand, pc)  # Show the final hand if the player stays.
                return pc, sp

    if choice2 == "s":
        pc = convert_ace(pc)  # Adjust for Aces being 11 or 1 if needed.

        print(f"Stay, {hand}: {pc[0]}, {pc[1]}", end="\n\n")
        return pc, sp

    if choice2 == "d":
        pc.append(random.choice(cards))
        pc = convert_ace(pc)  # Adjust for Aces being 11 or 1 if needed.
        print(f"Double, {hand}: {pc[0]}, {pc[1]}, {pc[2]}", end="\n\n")

        if sum(pc) > 21:
            print("Overbought, Dealer wins")  # Indicate the player busts after doubling.

        return pc, sp  # Return the modified hand and the split counter.


def convert_ace(hand):
    # Automatically convert Aces from 11 to 1 if the hand total exceeds 21.
    while sum(hand) > 21 and 11 in hand:
        ace_index = hand.index(11)  # Find the first Ace with value 11.
        hand[ace_index] = 1  # Change its value to 1.
        print(f"Player_card_{ace_index + 1} (Ace) automatically changed to 1")

    return hand  # Return the modified hand.


def dealer(cards, dc):
    global bankroll

    # Dealer takes cards until their total is 17 or higher.
    while sum(dc) < 17:
        next_dc = random.choice(cards)
        dc.append(next_dc)
        dc = convert_ace(dc)  # Adjust for Aces being 11 or 1 as needed.

    print_hand(10, dc)  # Show the dealer's final hand.

    if sum(dc) > 21:
        print()
        print("Dealer overbought, you win", end="\n\n")

        update_bankroll_in_file("w", bankroll)  # Update the bankroll file for a win.
        sys.exit()

    else:
        print("Dealer stays", end="\n\n")  # Dealer stays if their total is 17 or higher.


def compare_hand(hand, pc, dc):
    global bankroll

    if hand != "":
        print(hand)  # Print the name of the hand being compared, if provided.

    # Compare the player's hand total to the dealer's to determine the outcome.
    if sum(pc) > sum(dc):
        print("You win:", sum(pc), "vs", sum(dc), end="\n\n")
        update_bankroll_in_file("w", bankroll)  # Player wins and updates bankroll.

    elif sum(pc) == sum(dc):
        print("Push:", sum(pc), "vs", sum(dc), end="\n\n")
        update_bankroll_in_file("p", bankroll)  # Game is a push; bankroll remains the same.

    elif sum(pc) < sum(dc):
        print("Dealer wins:", sum(pc), "vs", sum(dc), end="\n\n")
        update_bankroll_in_file("l", bankroll)  # Player loses and updates bankroll.

    pc = [0, 0, 0]  # Reset the player's hand for the next round.

    return pc  # Return the reset hand.


def update_bankroll_in_file(wlp, new_bankroll):
    # Update the player's bankroll based on the game outcome.
    global bankroll

    if wlp == "w":
        bankroll += bet_amount  # Increase bankroll for a win.
        print(f"You win:", bet_amount)
        print("New bankroll:", int(bankroll))

    elif wlp == "l":
        bankroll -= bet_amount  # Decrease bankroll for a loss.
        print(f"You lose:", bet_amount)
        print("New bankroll:", int(bankroll))

    elif wlp == "p":
        print(f"No one wins:")  # No change to bankroll for a push.
        print("Bankroll:", int(bankroll))

    try:
        # Write the updated bankroll to the 'bankroll.txt' file.
        with open('bankroll.txt', 'w') as file:
            file.write(f'bankroll = {int(new_bankroll)}')

    except Exception as e:
        print("An error occurred while updating bankroll:", e)

    print()  # Print a newline for readability.


main()  # Start the game by calling the main function.

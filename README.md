# Blackjack Game - README

This document provides a comprehensive overview of a Blackjack game implemented in Python. The game simulates a classic casino card game between a player and a dealer, adhering to standard Blackjack rules. The primary goal for the player is to achieve a hand value closer to 21 than the dealer's hand without exceeding 21.

## Overview of the Program

The program is structured to replicate the Blackjack gaming experience, including betting, hand splitting, and handling Aces correctly. It utilizes several functions to manage game flow, card handling, player decisions, and score calculation. Additionally, it includes a system to track the player's bankroll across games by reading from and writing to an external file.

## Key Components

- **Card Handling:** Uses a single deck represented by a list of integers where face cards are denoted by 10 and Aces can be either 1 or 11.
- **Player Decisions:** Players can hit, stay, double down, or split their hand based on the cards they receive.
- **Splitting Hands:** The game allows the player to split their hand into separate hands if they receive a pair.
- **Bankroll Management:** The player's bankroll is tracked through an external file, allowing persistence between game sessions.
- **Ace Handling:** Special logic is included to adjust the value of Aces from 11 to 1 to prevent busting when beneficial for the player.

## Detailed Function Descriptions

### `main()`
The entry point of the program, orchestrating the game's overall flow. It loads the player's bankroll, initializes the deck, player's hand (pc), dealer's hand (dc), and tracks overbought statuses for split hands. It deals initial cards and enters the main game loop, making it the core of the game's lifecycle.

### `read_bankroll_from_file()`
Attempts to read the player's bankroll from `bankroll.txt`, ensuring game continuity. Validates the file format and content, setting the global `bankroll` variable. Handles errors gracefully, providing feedback for missing or malformed files.

### `deal(cards, pc, dc)`
Deals initial cards, checking for instant win conditions like Blackjack. It sets the stage for the game, emphasizing the randomness and initial strategy (e.g., whether to hit or stay based on initial cards).

### `choose_card()`
Simulates drawing a card from a deck, factoring in the card's remaining availability to mimic a real deck's depletion. Critical for the game's fairness and unpredictability.

### `print_hand(hand_number, hand)`
Displays hands, adjusting output based on the game context (e.g., hidden dealer card, split hands). Enhances user experience by clearly showing game state.

### `play(cards, pc, dc, ob)`
The heart of the game, handling player inputs and decisions. It navigates through the possible actions (hit, stay, double, split) and progresses the game accordingly, showcasing the game's interactive nature.

### `hit(cards, pc, dc)`
Allows adding cards to the player's hand, embodying the risk-reward essence of Blackjack. Manages the strategic decision of when to risk taking another card.

### `double(cards, pc, dc)`
Enables betting strategy by allowing the player to double their bet for one additional card, adding depth to the game's betting mechanics.

### `split(hand, cards, pc, ob)`
Offers strategic diversity by letting players split pairs into two hands, each played separately. This function highlights the complexity and strategic variation in Blackjack.

### `convert_ace(hand)`
Adjusts Ace values to optimize the hand's total, crucial for the dynamic nature of Ace values in Blackjack. This function directly impacts strategy, allowing players to navigate close-to-bust scenarios more safely.

### `dealer(cards, dc)`
Automates the dealer's actions, ensuring gameplay adheres to Blackjack rules. This function represents the game's challenge, as the dealer's actions are fixed and predictable, contrasting with the player's strategic freedom.

### `compare_hand(hand, pc, dc)`
Determines the round's outcome by comparing player and dealer hands, affecting the player's bankroll based on the result. It encapsulates the resolution of each game round, delivering the thrill of victory or the disappointment of defeat.

### `update_bankroll_in_file(wlp, new_bankroll)`
Saves the player's updated bankroll to a file, ensuring continuity of the player's financial status across sessions. This function underlines the game's persistence feature, allowing long-term progress tracking.

## Additional Key Aspects

- **Ace Handling:** Implements a nuanced approach to Ace value adjustments, a cornerstone of Blackjack strategy.
- **Bankroll Management:** Introduces a real-world gambling aspect by tracking wins, losses, and overall financial status.
- **Error Handling:** Ensures robustness by gracefully managing potential issues, such as file access errors or unexpected player inputs.

## Credits

This Blackjack game was developed by [Carlos Eckert], a passionate programmer with a keen interest in creating engaging and interactive gaming experiences. For more information on the developer or to explore other projects, visit https://github.com/Zeus0422 or contact via email: carloseckert05coding@gmail.com.
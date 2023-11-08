import random
import cv2
import mediapipe as mp

# Define the possible moves
moves = ["rock", "paper", "scissors"]

# Function to get the computer's move based on the previous opponent move and the result
def get_computer_move(opponent_last_move, opponent_won_last):
    if opponent_last_move:
        if opponent_won_last:
            # Play the move that defeats the opponent's last move
            return {"rock": "paper", "paper": "scissors", "scissors": "rock"}[opponent_last_move]
        else:
            # Play the move that the opponent played last
            return opponent_last_move
    else:
        # Play a random move the first time
        return random.choice(moves)

# Function to determine the winner of a round
def determine_winner(player_move, computer_move):
    if player_move == computer_move:
        return 0  # Tie
    elif (player_move == "rock" and computer_move == "scissors") or \
         (player_move == "paper" and computer_move == "rock") or \
         (player_move == "scissors" and computer_move == "paper"):
        return 1  # Player wins
    else:
        return -1  # Computer wins

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Game setup
rounds = int(input("Enter the number of rounds (3, 5, or 7): "))
opponent_last_move = None
opponent_won_last = False

# Initialize variables to keep track of scores
player_score = 0
computer_score = 0

# Main game loop
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process the captured frame to detect hand landmarks
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Extract hand landmarks and calculate the gesture
            # Here, you would implement the logic to recognize the gesture
            # and map it to a move (rock, paper, scissors)
            # For simplicity, let's assume a simple gesture recognition method
            # where you use the position of landmarks to determine the move.

            # Replace the following lines with your gesture recognition logic
            # Example: 
            # player_move = recognize_gesture(landmarks)
            # player_move = "rock"  # Replace with the actual recognized move
            
            # In this example, we'll use a random move for demonstration purposes.
            player_move = random.choice(moves)

            # Play a round of the game
            computer_move = get_computer_move(opponent_last_move, opponent_won_last)
            print(f"Computer plays: {computer_move}")
            result = determine_winner(player_move, computer_move)

            if result == 1:
                print("You win!")
                player_score += 1
                opponent_won_last = False
            elif result == -1:
                print("Computer wins!")
                computer_score += 1
                opponent_won_last = True
            else:
                print("It's a tie!")

            # Remember the opponent's last move
            opponent_last_move = player_move

    # Display the frame with recognized move
    cv2.putText(frame, f"Your move: {player_move}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Rock, Paper, Scissors Game", frame)

    # Press 'q' to exit the game
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Display the final results and the overall winner
print("Game over!")

if player_score > computer_score:
    print("You are the overall winner!")
elif player_score < computer_score:
    print("Computer is the overall winner!")
else:
    print("It's a tie game!")


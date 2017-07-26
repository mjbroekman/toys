answer = "Watson"
print("Here is a guessing game. You get three guesses.")
print("What is the name of the computer that played on Jeopardy?")
response = raw_input()

if response == answer:
    print("That's right!")
else:
    print("Sorry. Guess again.")
    response = raw_input()
    if response == answer:
        print("That's right!")
    else:
        print("Sorry. One more guess.")
        response = raw_input()
        if response == answer:
            print("That's right!")
        else:
            print("Sorry. That's all your guesses.")
            print("The correct answer is " + answer)

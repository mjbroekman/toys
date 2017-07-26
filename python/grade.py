print("Enter a numeric grade: ")
grade = int(raw_input())
if grade >= 90:
    letter = "A"
elif grade >= 80:
    letter = "B"
elif grade >= 70:
    letter = "C"
elif grade >= 60:
    letter = "D"
elif grade < 60:
    letter = "F"
else:
    letter = "Unrecognized input"

print("Letter grade is " + letter)

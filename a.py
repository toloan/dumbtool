print("Insisting on fixing user input")
first = 1
second = 2
third = 3
fora
 i in range(5):
    try:
        extra = input("What is the extra value? ")
    except StandardError:
        print("That's not a number. Please try again.")

total = first+second+third+extra
print(total)
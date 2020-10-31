burger_price = input("How much money do you want from me man?  ")
within_budget = float(burger_price) <= 10.00

vegetarian = input("Do they at least have a vegetarian option for the veggie peopledem? (yeah/nah)  ")
have_vegetarian = vegetarian == "yeah"

should_go = within_budget and have_vegetarian

if should_go == True:
    print("LET'S GOOOOO!!!!")
else:
    print("STAY HOME")







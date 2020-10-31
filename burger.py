# burger_price = float(input("How much is it this time smh?  "))
# within_budget = burger_price <= 10.00

# vegetarian = input("Is there a v option?  ")
# v_option = vegetarian == "yeah"

# meets_criteria = within_budget and v_option

# if meets_criteria:
#    print("Fine, spend your money here")

# if not meets_criteria:
#    print("Nah, it's not worth it")
# so assigning is the important step here, otherwise the Boolean statement won't happen

# meal_price = float(input('How much did the meal cost? '))
# discount_choice = input('Do you have a discount? y/n ')
# discount_applicable = discount_choice == 'y'
# if meal_price > 20 and discount_applicable:
#    total_meal = meal_price * 0.9
#    print("Discount has been applied. Your total is now {}".format(total_meal))
# else:
#    print("Spend more!")
# YOO if you're reading this, put this q in slack because they didn't take the £20 into consideration

temperature = int(input("What's the degrees celsius babe?  "))
if temperature > 200:
    print("Bro it's too hot! Turn it down")
elif temperature == 180:
    print("Perfect! Remember to still check on it though")
elif temperature < 150:
    print("Not hot enough. TURN IT UP!!")
else:
    print("Yeah that's close enough")

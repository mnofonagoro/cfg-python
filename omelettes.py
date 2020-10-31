eggs_in_box = 6
eggs_for_omelette = 1
number_of_boxes = int(input("How many boxes do you have?  "))

number_of_omelettes = int((number_of_boxes * eggs_in_box)/eggs_for_omelette)

print("You can make {} omelettes with {} boxes".format(number_of_omelettes, number_of_boxes))
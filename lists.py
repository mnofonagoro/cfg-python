import random

#costs = [8.30, 7.12, 5.01, 1.00, 0.99, 5.92, 3.50]
#total_cost = 0

#for cost in costs:
 #   total_cost = total_cost + cost

#print(total_cost)

first_names = ['Eren', 'Levi', 'Mikasa', 'Erwin']
last_names = ['Yaeger', 'Ackerman', 'Smith', "Ofonagoro"]
first_name = random.choice(first_names)
last_name = random.choice(last_names)
print('{} {}'.format(first_name, last_name))

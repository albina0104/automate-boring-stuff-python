# Sandwich Maker
# Asks the user for sandwich preferences, shows total price.

import pyinputplus as pyip

bread_types = {
    'wheat': 2.50,
    'white': 3.00,
    'sourdough': 3.20
}

protein_types = {
    'chicken': 10.00,
    'turkey': 15.60,
    'ham': 20.10,
    'tofu': 12.10
}

cheese_types = {
    'cheddar': 10.30,
    'Swiss': 12.10,
    'mozzarella': 15.45
}

additional_ingredients = {
    'mayo': 3.00,
    'mustard': 2.50,
    'lettuce': 5.00,
    'tomato': 7.30
}


print('Welcome to Sandwich Maker!')
total_price = 0

chosen_bread = pyip.inputMenu(list(bread_types.keys()), numbered=True)
total_price += bread_types[chosen_bread]

chosen_protein = pyip.inputMenu(list(protein_types.keys()), numbered=True)
total_price += protein_types[chosen_protein]

needs_cheese = pyip.inputYesNo("Do you want cheese? ")
if needs_cheese == 'yes':
    chosen_cheese = pyip.inputMenu(list(cheese_types.keys()), numbered=True)
    total_price += cheese_types[chosen_cheese]

for ingredient in additional_ingredients.keys():
    choice = pyip.inputYesNo(f'Do you want {ingredient}? ')
    if choice == 'yes':
        total_price += additional_ingredients[ingredient]

sandwiches_quantity = pyip.inputInt("How many sandwiches do you need? ", min=1)
total_price *= sandwiches_quantity

print(f'You will buy {sandwiches_quantity} sandwiches. Total price: ${total_price:.2f}')

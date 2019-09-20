import json

class Meal:
    def __init__(self, meal_name=None):
        self.meal_name = meal_name
        self.ingredients = list()
        self.ingredient_names = set()
        self.instructions = list()

    def add_ingredient(self, ingredient, quantity=None, unit=None):

        #add an ingredient and quantity to the list of ingredients
        #returns false if the ingredient is already in the list

        cur_ingredient = {"name": ingredient, "quantity": quantity, "unit":unit}

        already_exists = (ingredient in self.ingredient_names)

        self.ingredient_names.add(ingredient)

        if already_exists:
            return False

        self.ingredients.append(cur_ingredient)

        return True

    def update_ingredient(self, ingredient, quantity=None, unit=None):

        #update an existing ingredient quantity
        #if it does not already exist, the ingredient will be added as a new ingredient

        cur_ingredient = {"name": ingredient, "quantity": quantity, "unit": unit}

        update_ing = None

        exists = False
        for ing in enumerate(self.ingredients):
            if ing[1]["name"] == cur_ingredient["name"]:
                self.ingredients[ing[0]] = cur_ingredient

                exists = True
                break

        if not exists:
            self.add_ingredient(ingredient, quantity)

    def remove_ingredient(self, ingredient):
        for ing in enumerate(self.ingredients):
            if ing[1]["name"] == ingredient:
                del self.ingredients[ing[0]]
                self.ingredient_names.remove(ingredient)

    def add_instruction(self, instruction):
        if instruction in self.instructions:
            return False

        self.instructions.append(instruction)

        return True

    def update_instruction(self, instruction, new_instruction):
        for i, cur_instruction in enumerate(self.instructions):
            if cur_instruction == instruction:
                self.instructions[i] = new_instruction
                break

    def remove_instruction(self, instruction):
        if instruction in self.instructions:
            self.instructions.remove(instruction)

    def reorder_instruction(self, instruction, direction):
        instruction_idx = self.instructions.index(instruction)

        if direction.lower() == "up":
            insert_idx = instruction_idx - 1
        elif direction.lower() == "down":
            insert_idx = instruction_idx + 1

        if insert_idx < 0 or insert_idx > len(self.instructions):
            return

        temp = self.instructions[instruction_idx]
        self.instructions.remove(temp)

        self.instructions.insert(insert_idx, temp)

    def to_json(self):
        data = {
            'meal_name': self.meal_name,
            'instructions': self.instructions,
            'ingredients': self.ingredients,
            'ingredient_names': list(self.ingredient_names)
        }

        return json.dumps(data)

    def from_json(self, json_string):
        data = json.loads(json_string)

        self.meal_name = data["meal_name"]
        self.instructions = data["instructions"]
        self.ingredients = data["ingredients"]
        self.ingredient_names = set(data["ingredient_names"])
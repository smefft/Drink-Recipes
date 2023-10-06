from Drinks import DrinkList, Drink
from Recipe import Recipe
from Spirits import UserSpirit

if __name__ == "__main__":
    print("\n---Welcome to your personal drink generator---\n")
    spirit = UserSpirit().get_user_spirit()
    drink_list = DrinkList(spirit)
    drink_info = drink_list.prompt_user_for_drink()
    user_drink_id = Drink(drink_info).get_drink_id()

    print(Recipe(user_drink_id))


class UserSpirit:
    spirits = ['gin', 'tequila', 'vodka', 'rum', 'whiskey','brandy', 'bourbon']

    def __init__(self):
        self.user_spirit: str = self._prompt_for_user_spirit()
    
    def set_user_spirit(self, spirit):
        self.user_spirit = spirit

    def get_user_spirit(self):
        return self.user_spirit

    def _prompt_for_user_spirit(self) -> str:
        self.print_list_of_spirits()
        spirit_index: str = input("Choose the number of your spirit: ")
        spirit: str = None
        while not spirit: spirit = self._get_spirit_from_index(int(spirit_index))
        return spirit

    def print_list_of_spirits(self) -> None:
        print("Spirits to choose from:")
        for i, s in enumerate(self.spirits):
            print(f"  {i+1} {s.capitalize()}")     
    
    def _get_spirit_from_index(self, index: int) -> str:
        try:
            spirit = self.spirits[index-1]
            return spirit
        except IndexError:
            print(f"Not a valid choice. Please choose a number between 1 and {len(self.spirits)}")
            return ""

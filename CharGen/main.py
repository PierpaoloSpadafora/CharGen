import tkinter as tk
from view import CharacterCreatorView
from character_model import CharacterModel
from controller import CharacterCreatorController


def main() -> None:
    root = tk.Tk()
    root.title("Character Creator")

    model = CharacterModel()
    view = CharacterCreatorView(root)
    CharacterCreatorController(model, view)

    root.mainloop()


if __name__ == "__main__":
    main()

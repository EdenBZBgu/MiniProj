from Classes.Pasuk import Pasuk


def main():
    #p1 = Pasuk("1_1_1", "בראשית ברא אלהים את השמים ואת הארץ")
    p2 = Pasuk("Tanakh.Torah.Genesis.1.1", "בראשית ברא אלהים את השמים ואת הארץ")
    p2.build_constituency_tree()
    p2.constituency_tree.print_tree()
    # p1.build_teamim_tree()
    # p1.teamim_tree.print_tree()
    #
    # p2 = Pasuk(
    #     "1_1_21",
    #     "ויברא אלהים את התנינם הגדלים ואת כל נפש החיה הרמשת אשר שרצו המים למינהם ואת כל עוף כנף למינהו וירא אלהים כי טוב",
    # )
    # p2.build_teamim_tree()
    # p2.teamim_tree.print_tree()



if __name__ == "__main__":
    main()

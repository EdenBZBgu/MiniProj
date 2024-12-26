from Classes.Torah import Torah


def main():
    t = Torah()
    t.read("ExternalData/torah.xlsx")
    t.parse_trees()
    t.save()

    t2 = Torah()
    t2.load()


if __name__ == "__main__":
    main()

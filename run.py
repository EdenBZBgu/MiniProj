from Classes.Torah import Torah


def main():
    t = Torah()
    t.read("ExternalData/torah.xlsx")
    t.parse_trees()
    # t.save("torah_dmp.pkl")


if __name__ == "__main__":
    main()

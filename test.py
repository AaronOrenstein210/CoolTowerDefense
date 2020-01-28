def main():
    text = "Hello World"

    def change():
        return "Changed World"

    print(text)
    text = change()
    print(text)


main()

"""Initial baseline inventory script before the maintenance improvements."""

from inventory import inventory


def main():
    total = 0
    for item in inventory:
        total += item["quantity"] * item["price"]
    print("Total stock value:", total)


if __name__ == "__main__":
    main()

import argparse
import json
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--product", help="path to a product file", type=str, required=True)
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.product) as product_fd:
        product_data = json.load(product_fd)

        for product in product_data:
            print_data = [f"title: {product['title']}",
                          f"price: {product['price']}",
                          f"area: {str(product['area'])}",
                          f"link: {product['link']}"]
            print(os.linesep.join(print_data))
            print(max([len(x) for x in print_data]) * "*")


if __name__ == '__main__':
    main()

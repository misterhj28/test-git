import random


def generate_lotto_numbers():
    numbers = random.sample(range(1, 46), 6)
    numbers.sort()
    return numbers


if __name__ == "__main__":
    lotto_numbers = generate_lotto_numbers()
    print("로또 번호:", lotto_numbers)
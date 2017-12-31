import coffeewhale
import time


def main():
    test_func()


@coffeewhale.on_except
def test_func():
    print('start sleeping')
    time.sleep(1)
    print('after sleep')
    raise Exception()
    # coffeewhale.notify(url="https://hooks.slack.com/services/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",
    # result='hello world!')


if __name__ == "__main__":
    main()

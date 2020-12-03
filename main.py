import rollbar


def print_hi(name):
    print(f'Hi, {name}')


def test_rollbar(msg_text):
    rollbar.init('8026b336e7e4475482765f8b119d4049')
    rollbar.report_message(msg_text)


def error_test():
    a=1
    b='test'
    try:
        print(a+b[5])
    except TypeError:
        rollbar.report_message('Trying to sum int & str in error_test function')
    except Exception:
        rollbar.report_exc_info()


if __name__ == '__main__':
    test_rollbar('This is the initial message for testing')
    error_test()

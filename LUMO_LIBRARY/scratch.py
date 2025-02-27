import argparse

def function_timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(func.__name__)
        print(end - start)
        return result

    return wrapper

x = True
y = True
z = True

if x and y and z:
    print("hey")


parser = argparse.ArgumentParser(exit_on_error=False)
# parser.add_argument('milk', nargs='?', action='store', type=str)
sub = parser.add_subparsers(dest='command')
cal = sub.add_parser('match')
bee = sub.add_parser('clown')

cal.add_argument('match2', nargs="?")
cal.add_argument('match3', nargs="*")

# p, u = parser.parse_known_args(['baby', 'match', 'traby', 'raby'])
# print(p, u)
# print(p)


try:
    p, u = parser.parse_known_args()
    print(p, u)
except:
    p, u = parser.parse_known_args([])

print(p,u)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--barbie', nargs='?', type=int, default=50)
parser.add_argument('--cars', nargs='?', type=int, default=50)
parser.add_argument('--movie', nargs='?', type=str, default='other', choices=['melodrama', 'football', 'other'])

args = parser.parse_args()
movie = 0 if args.movie == 'melodrama' else 50 if args.movie == 'other' else 100
cars = 50 if args.cars > 100 or args.cars < 0 else args.cars
barbie = 50 if args.barbie > 100 or args.barbie < 0 else args.barbie
boy = round((100 - barbie + cars + movie) / 3)
girl = 100 - boy
print('boy:', boy)
print('girl:', girl)
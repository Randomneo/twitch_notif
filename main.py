import argparse
from app.app import main, web


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--application', '-a', choices=['bot', 'web'], default='bot')
    args = parser.parse_args()
    if args.application == 'web':
        web()
    elif args.application == 'bot':
        main()

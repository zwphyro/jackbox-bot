from argparse import ArgumentParser


def get_args():
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        "--room-code",
        required=True,
        help="The room code of the game to join.",
    )
    argument_parser.add_argument(
        "--preview",
        action="store_true",
        help="Open a browser view of bot actions.",
    )
    return argument_parser.parse_args()

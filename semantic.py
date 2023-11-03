import os
import argparse
import asyncio

from semantic_ai.config import Settings


def parse_arguments():
    parser = argparse.ArgumentParser(description='Semantic AI configuration')
    parser.add_argument('--config-file', help="location of config file")
    # parser.add_argument('--name', help='Module name', default='semantic_ai', choices=['semantic_ai'])
    args = parser.parse_args()
    return args


async def main():
    args = parse_arguments()


if __name__ == "__main__":
    asyncio.run(main())

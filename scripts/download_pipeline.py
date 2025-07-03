# run_pipeline.py

import tyro
from evadia.splitters import SplitterConfig, load_splitter


def main(splitter: SplitterConfig):
    splitter_func = load_splitter(splitter)
    print("Downloaded Splitter: ", splitter_func)

if __name__ == "__main__":
    tyro.cli(main, config=(tyro.conf.ConsolidateSubcommandArgs,))

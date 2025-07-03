# run_pipeline.py

import tyro
from evadia.splitters import SplitterConfig, load_splitter


def main(splitter: SplitterConfig):
    splitter_func = load_splitter(splitter)

    examples = ["Gardens, trees, benches", "Splash pads and shade"]
    all_ideas = [i for text in examples for i in splitter_func.split(text)]

    print("Ideas:")
    for idea in all_ideas:
        print(f"- {idea}")

if __name__ == "__main__":
    tyro.cli(main, config=(tyro.conf.ConsolidateSubcommandArgs,))

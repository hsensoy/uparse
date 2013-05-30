#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy
import json
from common import Measure
from tree2sentence import leaves

__author__ = 'husnusensoy'


def brackets(sentence, words):
    if len(sentence) == 3:
        if isinstance(sentence[1], list):
            lbracketing = brackets(sentence[1], words)

        if isinstance(sentence[2], list):
            rbracketing = brackets(sentence[2], words)

        return lbracketing + rbracketing + [(min(l for l, _ in lbracketing), max(m for _, m in rbracketing) )]
    else:
        i = words.index(sentence[1])
        return [(i, i + 1)]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Evaluate the bracketing metric of parser')
    parser.add_argument('key_file', help='Key file')
    parser.add_argument('output_file', help='Output file')
    parser.add_argument("--unary", help="Include unary brackets", action="store_true")
    parser.add_argument('--root', help="Include root bracket covering full sentence", action="store_false")

    args = parser.parse_args()

    assert args.key_file[-4:] == ".key"

    measure = Measure()
    with open(args.key_file, "rb") as key_fp, open(args.output_file, "rb") as model_fp:
        for key, model in zip(key_fp, model_fp):
            if model.strip() != '#####':
                key_json = json.loads(key)
                lvs = leaves(key_json)
                key_bracket = brackets(key_json, lvs)

                if not args.unary:
                    key_bracket = filter(lambda tuple: tuple[1] - tuple[0] > 1, key_bracket)

                if not args.root:
                    key_bracket = filter(lambda tuple: tuple[1] - tuple[0] != len(lvs), key_bracket)

                key_bracket_set = set(key_bracket)

                model_json = json.loads(model)
                lvs = leaves(model_json)
                model_bracket = brackets(model_json, lvs)

                if not args.unary:
                    model_bracket = filter(lambda tuple: tuple[1] - tuple[0] > 1, model_bracket)

                if not args.root:
                    model_bracket = filter(lambda tuple: tuple[1] - tuple[0] != len(lvs), model_bracket)

                model_bracket_set = set(model_bracket)

                measure.add(key=key_bracket_set,output=model_bracket_set)

    print str(measure)


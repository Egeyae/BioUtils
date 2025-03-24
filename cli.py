import argparse

main_parser = argparse.ArgumentParser(
    prog="BioUtils CLI",
    description="Various bioinformatics utilities: seq (sequence extraction)",
)
main_parser.add_argument(
    "tool",
    help="The tool that will be executed: seq",
)

main_parser.add_argument(
    "-i", "--input-file",
    help="The input file. Has priority over input string.",
    default=None,
)

main_parser.add_argument(
    "-is", "--input-string",
    help="Instead of a file, directly provide a string",
    default="",
)

main_parser.add_argument(
    "-o", "--output",
    help="The output file",
    default=None,
)

main_parser.add_argument(
    "-ot", "--output-type",
    help="The type of the output, can be raw or fasta (raw by default)",
    default="raw")

main_parser.add_argument(
    "--hide-output",
    default=False,
    action="store_true",
    help="Hide the output in the terminal",
)

args = main_parser.parse_args()
tool = args.tool

if args.input_file:
    with open(args.input_file, "r") as f:
        in_ = f.read()
elif args.input_string:
    in_ = args.input_string
else:
    in_ = None

match tool:
    case "seq":
        from seqextract import *

        run(in_, output_file=args.output, output_type=args.output_type, noprint=args.hide_output)
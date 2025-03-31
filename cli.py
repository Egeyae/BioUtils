import argparse
import sys
import scales
from scales import load_scale, get_scale_name

main_parser = argparse.ArgumentParser(
    prog="BioUtils CLI",
    description="Various bioinformatics utilities",
)

subparsers = main_parser.add_subparsers(dest="tool", required=True)

seq_parser = subparsers.add_parser("seq", help="Extract sequences from an input file or string")

seq_parser.add_argument(
    "-i", "--input-file",
    help="The input file. Has priority over input string.",
    default=None,
)

seq_parser.add_argument(
    "-is", "--input-string",
    help="Instead of a file, directly provide a string",
    default="",
)

seq_parser.add_argument(
    "-o", "--output",
    help="The output file",
    default=None,
)

seq_parser.add_argument(
    "-ot", "--output-type",
    help="The type of the output, can be raw or fasta (raw by default)",
    choices=["raw", "fasta"],
    default="raw",
)

seq_parser.add_argument(
    "-of", "--output-format",
    help="The output format, can be ol (one line), w<n>(.<s>) (wrap every n with separator s, s is optional)",
    default="fasta",
)

seq_parser.add_argument(
    "--hide-output",
    default=False,
    action="store_true",
    help="Hide the output in the terminal",
)

seq_type_group = seq_parser.add_mutually_exclusive_group()

seq_type_group.add_argument(
    '-p', '--protein',
    action='store_const', dest='seq_type', const='p',
    help="Define the sequence type, can be dna or protein (protein by default)"
)

seq_type_group.add_argument('-d', '--dna', 
    action='store_const', dest='seq_type', const='d'
)

seq_parser.set_defaults(seq_type='p')


hydrophob_parser = subparsers.add_parser("hydrophob", help="Generates hydrophobicity profile of a protein sequence")

hydrophob_parser.add_argument(
    "-i", "--input-file",
    help="The input file. Has priority over input string.",
    default=None,
)

hydrophob_parser.add_argument(
    "-is", "--input-string",
    help="Instead of a file, directly provide a string",
    default="",
)

hydrophob_parser.add_argument(
    "-o", "--output",
    help="The output file",
    default=None,
)

hydrophob_parser.add_argument(
    "--show",
    default=False,
    action="store_true",
    help="Show directly the generated graph, disabled by default",
)

hydrophob_parser.add_argument(
    '-s', '--scale',
    default=scales.get_scale_ids()[0],
    choices=scales.get_scale_ids(),
    help="The scale to use",
)

hydrophob_parser.add_argument(
    '-w', '--window-size',
    type=int,
    help="The window size to use",
    default=3,
)

hydrophob_parser.add_argument(
    '-gui', '--interface',
    action='store_true',
    default=False,
    help="Run with a graphic user interface, adds other options as launch params on the interface"
)

scales_parser = subparsers.add_parser("scales", help="Manage scales")

scales_parser.add_argument(
    '-l', '--list',
    action='store_true',
    help="List available scales",
    default=False
)

args = main_parser.parse_args()

if args.tool in ("seq", "hydrophob"):
    if not args.tool == "hydrophob" and args.interface:
        if args.input_file:
            with open(args.input_file, "r") as f:
                in_ = f.read()
        elif args.input_string:
            in_ = args.input_string
        else:
            print("No input provided, can not proceed")
            sys.exit(1)

match args.tool:
    case "seq":
        from seqextract import *

        run(in_, output_file=args.output, output_type=args.output_type, noprint=args.hide_output, seq_type=args.seq_type)

    case "hydrophob":
        from hydrophob import *

        if args.interface:
            gui()
        else:
            if not args.window_size % 2 == 1:
                print("Window size must be odd", file=sys.stderr)
                sys.exit(1)
            run(in_, output_file=args.output, show=args.show, scale_values=load_scale(args.scale), window=args.window_size, scale=get_scale_name(args.scale))

    case "scales":
        if args.list:
            scales.show_scales()

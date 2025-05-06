import argparse
import sys
from os import system
import scales
from scales import load_scale, get_scale_name

main_parser = argparse.ArgumentParser(
    prog="BioUtils CLI",
    description="Various bioinformatics utilities",
)

subparsers = main_parser.add_subparsers(dest="tool", required=True)

gui_parser = subparsers.add_parser("gui", help="Run the various tools in a web interface")

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

scales_parser = subparsers.add_parser("scales", help="Manage scales")

scales_parser.add_argument(
    '-l', '--list',
    action='store_true',
    help="List available scales",
    default=False
)

dotplot_parser = subparsers.add_parser("dotplot", help="Dotplot graph")

dotplot_parser.add_argument(
    "-ia", "--input-file-a",
    help="The input file for sequence A. Has priority over input string A.",
    default=None,
)

dotplot_parser.add_argument(
    "-isa", "--input-string-a",
    help="Instead of a file, directly provide a string for sequence A",
    default="",
)

dotplot_parser.add_argument(
    "-ib", "--input-file-b",
    help="The input file for sequence B. Has priority over input string B.",
    default=None,
)

dotplot_parser.add_argument(
    "-isb", "--input-string-b",
    help="Instead of a file, directly provide a string for sequence B",
    default="",
)

dotplot_parser.add_argument(
    "-o", "--output",
    help="The output file",
    default=None,
)

dotplot_parser.add_argument(
    "--show",
    default=False,
    action="store_true",
    help="Show directly the generated graph, disabled by default",
)

dotplot_parser.add_argument(
    '-w', '--window-size',
    type=int,
    help="The window size to use",
    default=1,
)

dotplot_parser.add_argument(
    "-ov", "--overlap",
    action="store_true",
    default=False,
    help="Create a dotplot with overlap, false by default"
)



args = main_parser.parse_args()
in_ = None
if args.tool in ("seq", "hydrophob", "dotplot"):
    if args.tool == "dotplot":
        if args.input_file_a:
            with open(args.input_file_a, "r") as f:
                in_a = f.read()
        elif args.input_string_a:
            in_a = args.input_string_a
        else:
            print("No sequence A provided, can not proceed", file=sys.stderr)
            sys.exit(1)

        if args.input_file_b:
            with open(args.input_file_b, "r") as f:
                in_b = f.read()
        elif args.input_string_b:
            in_b = args.input_string_b
        else:
            print("No sequence B provided, can not proceed", file=sys.stderr)
            sys.exit(1)
    else:
        if args.input_file:
            with open(args.input_file, "r") as f:
                in_ = f.read()
        elif args.input_string:
            in_ = args.input_string
        else:
            print("No input provided, can not proceed", file=sys.stderr)
            sys.exit(1)

match args.tool:
    case "seq":
        from seqextract import *

        run(in_, output_file=args.output, output_type=args.output_type, noprint=args.hide_output, seq_type=args.seq_type)

    case "hydrophob":
        from hydrophob import *

        if not args.window_size % 2 == 1:
            print("Window size must be odd", file=sys.stderr)
            sys.exit(1)
        run(in_, output_file=args.output, show=args.show, scale_values=load_scale(args.scale), window=args.window_size, scale=get_scale_name(args.scale))

    case "scales":
        if args.list:
            scales.show_scales()

    case "dotplot":
        from dotplot import *

        run(in_a, in_b, output_file=args.output, show=args.show, window=args.window_size, overlap=args.overlap)

    case "gui":
        system("PYTHONPATH=$(pwd) streamlit run Main.py")


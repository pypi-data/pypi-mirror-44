from pesummary.utils import CommandLine

if __name__ == "__main__":
    parser = CommandLine()
    opts = parser.parse_args()
    print(opts.webdir)
    print(opts.psd)

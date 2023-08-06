import pandas as pd

def read_headers(fname):
    df = pd.read_excel(fname)
    print('\n'.join([str(x) for x in df.columns]))


def read_column(fname, column):
    df = pd.read_excel(fname)
    print('\n'.join([str(x) for x in df[column]]))


def main():
    import sys
    if len(sys.argv) not in [2, 3]:
        exit('Usage: xlpus file.xls [ColumnName]')

    if len(sys.argv) == 2:
        read_headers(sys.argv[1])
    else:
        read_column(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()

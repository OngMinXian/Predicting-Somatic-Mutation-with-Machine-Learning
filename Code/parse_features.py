# import libraries
from collections import OrderedDict
import gzip

VCF_HEADER = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']

def lines(filename):
    """
    Open an optionally gzipped VCF file and generate an OrderedDict for each line.
    """
    file_opener = gzip.open if filename.endswith('.gz') else open
    
    with file_opener(filename) as file:
        for line in file:
            if line.startswith(b'#'):
                continue
            else:
                yield parse(line)

def parse(line):
    """
    Parse a single VCF line and return an OrderedDict.
    """
    result = OrderedDict()

    row = line.decode('utf8').rstrip().split('\t')

    # Read the values in the first seven columns.
    for i, col in enumerate(VCF_HEADER[:7]):
        result[col] = _get_value(row[i])

    # INFO field consists of "key1=value;key2=value;...".
    infos = row[7].split(';')

    for i, info in enumerate(infos, 1):
        # info should be "key=value".
        try:
            key, value = info.split('=')
        # But sometimes it is just "value", so we'll make our own key.
        except ValueError:
            key = 'INFO{}'.format(i)
            value = info
        # Set the value to None if there is no value.
        result[key] = _get_value(value)

    return result


def _get_value(value):
    """
    Interpret null values and return ``None``. Return a list if the value contains a comma.
    """
    if not value or value in ['', '.', 'NA']:
        return None
    if ',' in value:
        return value.split(',')
    return value

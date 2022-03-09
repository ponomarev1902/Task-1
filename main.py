import chardet
import argparse
import codecs
import os


def detect(file, chunk=2048):
    """Tries to resolve the encoding of the file."""
    with open(file, 'rb') as f:
        return chardet.detect(f.read(chunk))


def decode_file(file, encoding, chunk=1024):
    """Decodes the file according to it encoding to utf-8."""
    with codecs.open(file, 'r', encoding) as origin:
        target_name = file + '.temp'
        with codecs.open(target_name, 'w', encoding='utf-8') as target:
            while True:
                text = origin.read(chunk)
                print(text)
                if not text:
                    break
                target.write(text)
    os.replace(target_name, file)


def main(path='.'):
    threshold = 0.9
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            if not dir_name.islower():
                dir_path = os.path.join(root, dir_name)
                new_dir = os.path.join(root, dir_name.lower())
                os.rename(dir_path, new_dir)
        for file in files:
            file_path = os.path.join(root, file)
            encoding, confidence, _ = detect(file_path).values()
            if confidence >= threshold:
                decode_file(file_path, encoding)
            else:
                print(f'File {file} has unknown encoding.')
            if not file.islower():
                new_file = os.path.join(root, file.lower())
                os.rename(file_path, new_file)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Path')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()
    if args.path:
        main(args.path)
    else:
        main()

import argparse
import fnmatch
from pathlib import Path
import os
import shutil
import subprocess
import sys
import time

DEEPSPEECH_TEXT_LINE_LOC = -2 # MAGIC

def deepspeech_one_file(ds_dir, cur_path):
    res = subprocess.run(
        ['deepspeech',
        '--model', str(ds_dir / 'output_graph.pb'),
        '--lm', str(ds_dir / 'lm.binary'),
        '--trie', str(ds_dir / 'trie'),
        '--audio', str(cur_path)],
        capture_output=True,
        encoding='utf-8'
    )

    return res.stdout

def recognize_files(in_dir, out_dir, ds_dir, ext):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
        time.sleep(1)

    os.mkdir(out_dir)

    for root, dirs, files in os.walk(in_dir):
        audios = fnmatch.filter(files, '*' + ext)
        if audios:
            cur_dir = out_dir / os.path.relpath(root, in_dir)
            os.mkdir(cur_dir)

            for aud in audios:
                out_fn = cur_dir / (os.path.splitext(aud)[0] + '.txt')
                cur_path = Path(root) / Path(aud)

                print(f"Recognizing file: {cur_path}...")
                text = deepspeech_one_file(ds_dir, cur_path)

                with out_fn.open('w', encoding='utf-8') as outf:
                    outf.write(text)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('in_dir', type=Path, help="Input directory")
    parser.add_argument('out_dir', type=Path, help="Output directory")
    parser.add_argument('ds_dir', type=Path, help="Deepspeech directory")
    parser.add_argument('--ext', default='.wav', help="File extension")

    args = parser.parse_args()


    print('*** Starting!')
    recognize_files(args.in_dir, args.out_dir, args.ds_dir, args.ext)
    print('*** Done!')

if __name__ == '__main__':
    sys.exit(main())

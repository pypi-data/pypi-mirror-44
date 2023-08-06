# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: basenef
@file: doc_generator.py
@date: 4/13/2019
@desc:
'''
from getpass import getuser
import os
import sys
import time
import numpy as np
from basenef.utils import tqdm
from basenef.config import DOC_PATH
import matplotlib

matplotlib.use('Agg')
timestamp = time.time()
datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))
datetime_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(int(timestamp)))

author = getuser()


def title_block_gen():
    title_block = f"""
# NEF AutoDoc {datetime}
- Author: {author} 
- Generation time: {datetime}
- Operation system: {sys.platform}
- OS language: {os.environ['LANG']}
- Duration: 0.0 sec
- Total errors: 0
- Total warning: 0
- Description: 




\pagebreak


"""
    return [title_block]


def _text_gen_as_table(dct: dict = {}):
    out_text = ['|key|values|\n|:---|:---|\n']
    for key, val in dct.items():
        if key == 'data':
            out_text.append(f"| {key} | Ignored |\n")
        elif not isinstance(val, dict):
            if isinstance(val, str) and len(val) > 30:
                out_text.append(f"| {key} | Ignored |\n")
            else:
                out_text.append(f"| {key} | {val} |\n")
        else:
            out_text.append(f"| {key} | {'Ignored'} |\n")

    return out_text


def block_gen(dct: dict = {}, *, foldername = DOC_PATH, filename = ''):
    out_text = []

    print('Generating text blocks...')
    for key, val in tqdm(dct.items()):
        out_text.append(f'### Name: {key}\n')
        out_text += _text_gen_as_table(val)
        if 'data' in val.keys():
            print(foldername + 'figures')
            if not os.path.isdir(foldername + 'figures'):
                os.mkdir(foldername + 'figures')
            if isinstance(val, dict):
                from basenef.tools.file_io import data_loader
                url = val['data']
                data = data_loader(url)
            else:
                data = val.data

            if isinstance(data, np.ndarray):
                from matplotlib import pyplot as plt
                shape = data.shape
                plt.figure(figsize = (30, 10))
                plt.subplot(131)
                plt.imshow(data[:, :, int(shape[2] / 2)])
                plt.subplot(132)
                plt.imshow(data[:, int(shape[1] / 2), :].transpose())
                plt.subplot(133)
                plt.imshow(data[int(shape[0] / 2), :, :].transpose())
                if filename == '':
                    img_path = foldername + f'figures/{datetime_str}' + key + 'data.png'
                else:
                    img_path = foldername + f'figures/{filename}' + key + 'data.png'
                plt.savefig(img_path)
                # out_text.append(f'![]({key}data.png)\n')
                out_text.append(f"![This is the caption]({img_path})\n")
                out_text.append(f"\\pagebreak\n\n")

    return out_text


def statistic_block_gen(dct: dict = {}):
    out_text = []

    key_set = set()
    for name, sub_dct in dct.items():
        for key, val in sub_dct.items():
            if isinstance(val, str) and len(val) < 30:
                key_set.add(key)
            #
            # try:
            #     float(val)
            #     key_set.add(key)
            # except:
            #     pass
    col_names = ['|name ', '|:---']
    for key in key_set:
        col_names[0] += '|' + key + ''
    else:
        col_names[0] += '|\n'
    for _ in key_set:
        col_names[1] += '|:---'
    else:
        col_names[1] += '|\n'
    out_text += col_names

    for name, sub_dct in dct.items():
        row = '| ' + name + ' '
        for key in key_set:
            if key in sub_dct:
                row += '|' + str(sub_dct[key]) + ''
            else:
                row += '|-'
        else:
            row += '|\n'

        out_text += [row]

    return out_text


def doc_gen(dct: dict = {}, filename: str = None):
    import pypandoc
    if filename is None:
        filename = 'doc_gen-' + datetime_str + '.md'
    out_text = title_block_gen()
    out_text += block_gen(dct, foldername = DOC_PATH, filename = filename)
    out_text += statistic_block_gen(dct)
    with open(DOC_PATH + filename, 'w') as fout:
        fout.writelines(out_text)
    print('Converting MD to PDF...')
    pypandoc.convert_file(DOC_PATH + filename, 'pdf', outputfile = DOC_PATH + filename + '.pdf')
    return filename

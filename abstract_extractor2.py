import os
import argparse


def word_count(path_for_wc, count_file_name):
    f = open(path_for_wc + '/' + str(count_file_name) + '.txt', 'r')
    length = len(f.read())
    f.close()

    return length


def parse_ace(ann_path, ann_file, length):
    tag_list = []

    f = open(ann_path + '/' + ann_file + '.ann', 'w')

    for line in open(ann_path + '/' + ann_file + '.ann'):
        line = line.rstrip()

        line_list = line.split('\t')
        start_char = line_list[1].split(' ')[1]
        if ';' in line:
            end_char = line_list[1].split(' ')[3]
        else:
            end_char = line_list[1].split(' ')[2]

        if 'Arg1:' in line:
            arg_tag1 = line_list[1].split(' ')[1].split(':')[1]
            arg_tag2 = line_list[1].split(' ')[2].split(':')[1]

            if (arg_tag1 in tag_list) or (arg_tag2 in tag_list):
                pass
            else:
                f.write(line + '\n')

        elif 'coref' in line:
            arg_tag1 = line_list[1].split(' ')[1]
            arg_tag2 = line_list[1].split(' ')[2]

            if (arg_tag1 in tag_list) or (arg_tag2 in tag_list):
                pass
            else:
                f.write(line + '\n')

        elif (int(start_char) > length) or (int(end_char) > length):
            tag_list.append(line_list[0])
        else:
            f.write(line + '\n')
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str, help="Working target directory")
    args = parser.parse_args()
    path = args.directory
    print("Working folder: ", path)

    new_file_list = []
    file_list = os.listdir(path)

    for i in range(len(file_list)):
        if file_list[i].split('.')[-1] == 'txt':
            new_file_list.append(file_list[i].split('.')[0] + '.' + file_list[i].split('.')[1])

    file_list = list(set(new_file_list))
    print(file_list)

    for i in file_list:
        current_file_name = i.split('.')[0] + str('.') + i.split('.')[1]
        words = word_count(path, current_file_name)
        print('Text length is', words, 'in', str(current_file_name))
        parse_ace(path, current_file_name, words)

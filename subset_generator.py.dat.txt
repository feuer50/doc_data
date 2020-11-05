import os
import argparse


def word_count(path_for_wc, count_file_name):
    f = open(path_for_wc + '/' + str(count_file_name) + '.txt', 'r')
    length = len(f.read())
    f.close()

    return length


def parse_txt(txt_path, txt_file, iter_no, start_length, final_length):
    os.makedirs(txt_path + '/subset/', exist_ok=True)
    f = open(txt_path + '/' + txt_file + '.txt', 'r')
    text = f.read()
    f.close()

    f = open(txt_path + '/subset/' + txt_file + '_' + str(iter_no) + '.txt', 'w')
    f.write(text[start_length:final_length])
    f.close()


def parse_ace(ann_path, ann_file, iter_no, start_length, final_length):
    os.makedirs(ann_path + '/subset/', exist_ok=True)

    tag_list = []

    f = open(ann_path + '/subset/' + ann_file + '_' + str(iter_no) + '.ann', 'w')

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

        elif ((int(start_char) > final_length) or (int(end_char) > final_length) or
             (int(start_char) < start_length) or (int(end_char) < start_length)):
            # print("start_char:", start_char)
            # print("end_char:", end_char)
            # print("start_length:", start_length)
            # print("final_length:", final_length)
            tag_list.append(line_list[0])
            # exit()
        else:
            start_char = int(start_char) - start_length
            end_char = int(end_char) - start_length

            # T22 Composition 861 867 ethane

            line_list[1] = ' '.join([line_list[1].split(' ')[0], str(start_char), str(end_char)])
            line = '\t'.join([line_list[0], line_list[1], line_list[2]])

            print(line)

            f.write(line + '\n')
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str, help="Working target directory (without closed '/')")
    parser.add_argument('span_char', type=int, help="Span of subset document")
    args = parser.parse_args()
    path = args.directory
    span_char = args.span_char
    print("Working folder: ", path)
    print("Span character to chunk: ", span_char)

    new_file_list = []
    file_list = os.listdir(path)

    for i in range(len(file_list)):
        if file_list[i].split('.')[-1] == 'txt':
            new_file_list.append(file_list[i].split('.')[0] + '.' + file_list[i].split('.')[1])

    file_list = list(set(new_file_list))

    for i in file_list:
        current_file_name = i.split('.')[0] + str('.') + i.split('.')[1]
        words = word_count(path, current_file_name)
        print('Text length is', words, 'in', str(current_file_name))

        final_turn = int(words / span_char)

        for j in range(final_turn):
            if j == 0:
                start_char = j*span_char
            else:
                start_char = j*span_char + 1
            if j == final_turn - 1:
                end_char = words
            else:
                end_char = (j + 1)*span_char
            print(start_char, end_char)
            parse_txt(path, current_file_name, j, start_char, end_char)
            parse_ace(path, current_file_name, j, start_char, end_char)

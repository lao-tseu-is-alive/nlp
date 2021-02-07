import re


def get_lines_from_file(file_path, file_encoding='utf-8'):
    """reads a text file at file_path, with specified file_encoding
    and returns a list of the lines (array of lines) found in this files"""
    with open(file_path, mode='r', encoding=file_encoding) as f:
        return f.readlines()


def get_indices_for_regex(lines_array, regex_expression):
    """ returns a list of the indices in the line_array list of strings,
    that match the given regex_expression
    """
    return [i for i, elem in enumerate(lines_array) if re.match(regex_expression, elem)]


def print_indices_text(lines_array, the_indexes, message=''):
    """will print the lines from the given lines_array at all the_indexes parameter """
    print(f'found this {message} at indexes {the_indexes}')
    print("\n".join(['[{:5}] {}'.format(i, lines_array[i]) for i in the_indexes]))


def get_real_book_from_gutenberg_file(gutenberg_file_path, file_encoding='utf-8', offset=1):
    a_book = get_lines_from_file(gutenberg_file_path, file_encoding=file_encoding)
    gutenberg_indices = get_indices_for_regex(a_book, r'\*\*\* (START|END) OF THIS PROJECT GUTENBERG EBOOK')
    if len(gutenberg_indices) == 2:
        my_real_book = [i.rstrip() for i in a_book[gutenberg_indices[0] + 1:gutenberg_indices[1] - 1]]
        return my_real_book[offset:-offset]


def print_head_and_tail(lines_array, offset=10):
    print("### 10 FIRST LINES : ###\n{}\n########################".format("\n".join(lines_array[:offset])))
    print("### 10 LAST  LINES : ###\n{}\n########################".format("\n".join(lines_array[-offset:])))

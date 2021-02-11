import re

VICTOR_HUGO_LES_MISERABLES_TOME_1_FANTINE_FILE_PATH = 'data/pg17489.txt'
VICTOR_HUGO_LES_MISERABLES_TOME_1_FANTINE_ENGLISH_FILE_PATH = 'data/pg48731.txt'


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
    # print(f'found this {message} at indexes {the_indexes}')
    print("\n".join(['[{:5}] {}'.format(i, lines_array[i]) for i in the_indexes]))


def get_real_book_from_gutenberg_file(gutenberg_file_path, file_encoding='utf-8', offset=1):
    a_book = get_lines_from_file(gutenberg_file_path, file_encoding=file_encoding)
    gutenberg_indices = get_indices_for_regex(a_book, r'\*\*\* (START|END) OF THIS PROJECT GUTENBERG EBOOK')
    if len(gutenberg_indices) == 2:
        my_real_book = [i.rstrip() for i in a_book[gutenberg_indices[0] + 1:gutenberg_indices[1] - 1]]
        return my_real_book[offset:-offset]


def print_head_and_tail(lines_array, offset=10):
    print("### {} FIRST LINES : ###\n{}\n########################".format(offset, "\n".join(lines_array[:offset])))
    print("### {} LAST  LINES : ###\n{}\n########################".format(offset, "\n".join(lines_array[-offset:])))


def print_book_sections_indices(lines_array, section_regex=r'^Livre (.+)\-\-(.+)$'):
    my_sections_indices = get_indices_for_regex(lines_array, section_regex)
    print_indices_text(lines_array, my_sections_indices)


def get_dict_book_parts(lines_array, section_regex=r'^Livre (.+)\-\-(.+)$', remove_title_lines=True):
    my_sections_indices = get_indices_for_regex(lines_array, section_regex)
    my_sections = {}
    for i, v in enumerate(my_sections_indices):
        # print(f'{i:<{5}}:{v:>{15}}, {lines_array[v]}')
        key = f'{i + 1:0>{2}}) {lines_array[v]}'
        # print(key, i < (len(my_sections_indices) - 1))
        if i < (len(my_sections_indices) - 1):
            if remove_title_lines:
                my_sections[key] = lines_array[v + 1:my_sections_indices[i + 1]]
            else:
                my_sections[key] = lines_array[v:my_sections_indices[i + 1]]
        else:
            my_sections[key] = lines_array[v:]
    return my_sections


def get_chapters_dic_of_first_section_of_french_book(
        gutenberg_file_path=VICTOR_HUGO_LES_MISERABLES_TOME_1_FANTINE_FILE_PATH):
    all_book = get_real_book_from_gutenberg_file(VICTOR_HUGO_LES_MISERABLES_TOME_1_FANTINE_FILE_PATH, offset=5)
    REAL_BEGIN_OF_BOOK = 117  # first index after the table of contents
    my_book = all_book[REAL_BEGIN_OF_BOOK:]
    my_book_sections = get_dict_book_parts(my_book, section_regex=r'^Livre (.+)\-\-(.+)$')
    my_first_section = my_book_sections['01) Livre premier--Un juste']
    return get_dict_book_parts(my_first_section, section_regex=r'^Chapitre\s([IVX]+)$')


def get_chapters_dic_of_first_section_of_english_book(
        gutenberg_file_path=VICTOR_HUGO_LES_MISERABLES_TOME_1_FANTINE_ENGLISH_FILE_PATH):
    all_book = get_real_book_from_gutenberg_file(
        VICTOR_HUGO_LES_MISERABLES_TOME_1_FANTINE_ENGLISH_FILE_PATH, offset=5)
    REAL_BEGIN_OF_BOOK = 117  # first index after the table of contents
    my_book = all_book[REAL_BEGIN_OF_BOOK:]
    my_book_sections = get_dict_book_parts(my_book, section_regex=r'^Livre (.+)\-\-(.+)$')
    my_first_section = my_book_sections['01) Livre premier--Un juste']
    return get_dict_book_parts(my_first_section, section_regex=r'^Chapitre\s([IVX]+)$')


if __name__ == '__main__':
    BOOK_PATH = '../data/pg17489.txt'
    NUM_LINES_BOOK = 14399
    NUM_LINES_GUTENBERG_BOOK = 14010

    INDICES_GUTENBERG_BOOK = [19, 14041]
    book = get_lines_from_file(BOOK_PATH)
    num_lines_book = len(book)
    if NUM_LINES_BOOK != num_lines_book:
        print(f"""
        WARNING[Problem in function get_lines_from_file] :
        in the original books there is \t {NUM_LINES_BOOK} lines, 
        with get_lines_from_files i get\t {num_lines_book} lines 
        """)
    else:
        print(f'## OK : found {num_lines_book:8_} lines in the file {BOOK_PATH}')

    my_indices = get_indices_for_regex(book, r'\*\*\* (START|END) OF THIS PROJECT GUTENBERG EBOOK')

    if INDICES_GUTENBERG_BOOK != my_indices:
        print(f"""
        WARNING[Problem in function get_indices_for_regex] :
        in the original books the indices where \t {INDICES_GUTENBERG_BOOK} , 
        with get_indices_for_regex i get\t {my_indices} instead ! Check the function ! 
        """)
    else:
        print(f'## OK : found GUTENBERG DELIMITERS at {my_indices}')

    my_gutenberg_book = get_real_book_from_gutenberg_file(BOOK_PATH, file_encoding='utf-8', offset=5)
    num_lines_my_gutenberg_book = len(my_gutenberg_book)

    if NUM_LINES_GUTENBERG_BOOK != num_lines_my_gutenberg_book:
        print(f"""
        WARNING[Problem in function get_real_book_from_gutenberg_file] :
        in the original 'real' book there is \t {NUM_LINES_GUTENBERG_BOOK} lines, 
        with get_lines_from_files i get\t {num_lines_my_gutenberg_book} lines instead ! Check the function.
        """)
    else:
        print(f'## OK : found {num_lines_my_gutenberg_book:8_} real lines in the gutenberg file {BOOK_PATH}')
    print(f"## OK : let's print all sections indices of the book")
    print_book_sections_indices(my_gutenberg_book)
    REAL_BEGINNING_OF_BOOK = 117  # indices after table of contents
    print(
        f"## OK : let's keep only the lines of the real sections, starting from index {REAL_BEGINNING_OF_BOOK} upwards")
    my_gutenberg_book = my_gutenberg_book[117:]
    my_offset = 8
    print(f"## OK : let's print {my_offset} first and last lines of all the book")
    print_head_and_tail(my_gutenberg_book, offset=my_offset)
    print(f"## OK : now let us get a dictionary from the book sections")
    book_sections = get_dict_book_parts(my_gutenberg_book, section_regex=r'^Livre (.+)\-\-(.+)$')
    sections_keys_string = "\n".join(book_sections.keys())
    print(f"BOOK SECTIONS KEYS : \n{sections_keys_string}")
    print(f"## OK : let's print {my_offset} first and last lines of the first section :")
    first_section = book_sections['01) Livre premier--Un juste']
    print_head_and_tail(first_section, offset=my_offset)
    print(f"## OK : now let us get a dictionary from the first section chapters")
    section_chapters = get_dict_book_parts(first_section, section_regex=r'^Chapitre\s([IVX]+)$')
    chapters_keys_string = "\n".join(section_chapters.keys())
    print(f"FIRST SECTION CHAPTER KEYS : \n{chapters_keys_string}")
    first_section_chapter_1 = section_chapters['01) Chapitre I']
    print(f"## OK : let's print {my_offset} first and last lines of the first chapter of the section :")
    print_head_and_tail(first_section_chapter_1, offset=my_offset)

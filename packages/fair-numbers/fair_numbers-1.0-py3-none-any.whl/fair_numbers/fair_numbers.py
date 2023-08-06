def nicer(number, description_number=False):
    """
    Форматирует целое число number в понятный вид и возвращает как строку
    При неправильных аргументах выбрасывает исключение

    Обязательный аргумент – number. Предел – 999 999 999 999 миллиардов
    Если number больше предела – выбрасывает исключение
    Необязательный аргумент – булево значение description_number

    description_number отвечает за текстовое обозначение разрядов числа
    True – обозначает, False – не обозначает. По умолчанию – False
    """
    def format_thousands():
        if description_number is True:
            return num[0] + ' тыс. ' + num[1::]
        return num[0] + ' ' + num[1::]

    def format_tens_thousands():
        if description_number is True:
            return num[0:2:] + ' тыс. ' + num[2::]
        return num[0:2:] + ' ' + num[2::]

    def format_hundreds_thousands():
        if description_number is True:
            return num[0:3:] + ' тыс. ' + num[3::]
        return num[0:3:] + ' ' + num[3::]

    def format_one_millions():
        if description_number is True:
            return num[0] + ' млн. ' + num[1:4:] + ' тыс. ' + num[4::]
        return num[0] + ' ' + num[1:4:] + ' ' + num[4::]

    def format_tens_millions():
        if description_number is True:
            return num[0:2:] + ' млн. ' + num[2:5:] + ' тыс. ' + num[5::]
        return num[0:2:] + ' ' + num[2:5:] + ' ' + num[5::]

    def format_hundreds_millions():
        if description_number is True:
            return num[0:3] + ' млн. ' + num[3:6] + ' тыс. ' + num[6::]
        return num[0:3] + ' ' + num[3:6] + ' ' + num[6::]

    def format_one_billions():
        if description_number is True:
            return num[0] + ' млрд. ' + num[1:4:] + ' млн. ' + num[4:7:] +\
                   ' тыс. ' + num[7::]
        return num[0] + ' ' + num[1:4:] + ' ' + num[4:7:] + ' ' + num[7::]

    def format_tens_billions():
        if description_number is True:
            return num[0:2:] + ' млрд. ' + num[2:5:] + ' млн. ' + num[5:8:] +\
                   ' тыс. ' + num[8::]
        return num[0:2:] + ' ' + num[2:5:] + ' ' + num[5:8:] + ' ' + num[8::]

    def format_hundreds_billions():
        if description_number is True:
            return num[0:3:] + ' млрд. ' + num[3:6:] + ' млн. ' + num[6:9] +\
                   ' тыс. ' + num[9::]
        return num[0:3:] + ' ' + num[3:6:] + ' ' + num[6:9] + ' ' + num[9::]

    if (not isinstance(number, int) or not isinstance(description_number, bool)):
        raise Exception('Incorrect first or second argument')
    elif (number > 999999999999):
        raise Exception('Number too large')
    num = str(number)
    length_num = len(num)
    if length_num == 4:
        return format_thousands()
    elif length_num == 5:
        return format_tens_thousands()
    elif length_num == 6:
        return format_hundreds_thousands()
    elif length_num == 7:
        return format_one_millions()
    elif length_num == 8:
        return format_tens_millions()
    elif length_num == 9:
        return format_hundreds_millions()
    elif length_num == 10:
        return format_one_billions()
    elif length_num == 11:
        return format_tens_billions()
    elif length_num == 12:
        return format_hundreds_billions()
    else:
        return num

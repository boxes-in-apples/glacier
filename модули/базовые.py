def tokenize(multiline_text, delimiter=' '):
    """
    Преобразует многострочный текст в матрицу (список списков),
    которая может быть использована как команды.
    """
    matrix = []
    lines = multiline_text.strip().split('\n')
    
    for line in lines:
        if not line.strip(): # Пропускаем пустые строки
            continue
            
        # Улучшенное разбиение
        if delimiter == ' ':
            elements = list(filter(None, line.strip().split()))
        else:
            elements = line.strip().split(delimiter)
            
        if elements:
            matrix.append(elements)
            
    return matrix

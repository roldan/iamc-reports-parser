import io, re, csv, sys

def extract_table(filename, start_exp, end_exp):
    """Convierte el contenido de 'filename' (output de `pdftotext -layout`) a una tabla en base a 'start_exp', 'end_exp'

    Parameters:
    filename (str): Path al archivo con el contenido de `pdftotext -layout`
    start_exp (str): Expresión para comenzar a extraer líneas (inclusiva)
    end_exp (str): Expresión para dejar de extraer líneas (exclusiva)

    Returns:
    list:Lista con las filas/columnas de la tabla

    """
    f = open(filename, 'r')
    i = 1
    lines = []
    section_started = False
    for l in f:
        line = l.strip()

        # Start getting lines
        if start_exp in l.lower():
            section_started = True

        if section_started and line:
            columns = re.split("  +", line)
            if columns:
                lines.append(columns)
        
        # Stop getting lines
        if end_exp in l.lower():
            section_started = False

        i += 1

    return lines

def parse_open_options_positions_table(lines):
    """Limpia filas y columnas de la tabla para quedarse sólo con la información relevante

    Parameters:
    lines (list): Lista con las filas de la tabla (output de 'extract_table')

    Returns:
    list:Lista con las filas/columnas de la tabla parseadas

    """
    
    lines = filter(lambda x: len(x) > 1 or x[0].lower() in ['opciones de compra', 'opciones de venta'], lines)

    blacklist  = ['anexo b', 'especie', 'cubiertas', 'total']
    lines = list(filter(lambda x: not any(item in x[0].lower() for item in blacklist), lines))

    symbol = None
    type = None
    i = 0
    for line in lines:
        if line[0].isnumeric():
            line.pop(0)

        if line[0].lower() == 'opciones de compra':     # Empiezan los calls
            type = 'CALL'
        elif line[0].lower() == 'opciones de venta':    # Empiezan los puts
            type = 'PUT'
        else:
            if len(line) == 8:                          # Empieza nuevo subyacente
                symbol = line[0]
            else:
                line.insert(0, symbol)              
            line.insert(2, type)                        
        i += 1

    # Borro filas que ya no necesitamos
    blacklist  = ['opciones de compra', 'opciones de venta']
    lines = filter(lambda x: x[0].lower() not in blacklist, lines)

    return lines

"""
Ejemplo de uso (requiere `pdftotext`):

1) pdftotext -layout report.pdf
2) python iamc_to_csv.py report.txt > report.csv
"""
if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print("Debe especificar una ruta de archivo válida. Ej: `python iamc_to_csv.py /ruta/al/archivo.txt`")
        exit()

    try:
        filename = sys.argv[1]
        lines = extract_table(filename, 'posiciones abiertas por especie al', 'total opciones de venta')
        lines = parse_open_options_positions_table(lines)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows([['Especie', 'Serie', 'Tipo', 'Cubiertas', 'Opuestas', 'Cruzadas', 'Descubiertas', 'Total', 'Variación c/día anterior']])  
        writer.writerows(lines)
        print(output.getvalue())

    except Exception as ex:
        print(ex)
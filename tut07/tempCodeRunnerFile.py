
        range_cell = sheet[f'{col}{3}':f'{col}{11}']
        for cell in range_cell:
            for x in cell:
                x.border = thin_border
    for i in range(iter + 1):
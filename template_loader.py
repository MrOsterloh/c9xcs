from pyxlsb import open_workbook


def loader_TemplateBasis_180305(wb_path):
    try:
        result = dict()
        with open_workbook(wb_path) as wb:
            with wb.get_sheet('Output') as sheet:
                for row in sheet.rows():
                    name = row[0].v
                    value = row[3].v

                    if name and value:
                        result[name] = value

            with wb.get_sheet('Backup') as sheet:
                for nr, row in enumerate(sheet.rows()):
                    if nr == 0 :
                        continue
                    elif nr > 2:
                        break
                    else:
                        name = row[0].v
                        value = row[1].v

                        if name and value:
                            result[name] = value

            with wb.get_sheet('Settings') as sheet:
                for nr, row in enumerate(sheet.rows()):
                    if nr < 40:
                        continue
                    elif nr > 48:
                        break
                    else:
                        name = row[6].v
                        value = row[8].v

                        if name and value:
                            result[name] = value

        return result
    except Exception as err:
        print(err)
        return None


if __name__ == '__main__':
    wb_path = r'\\vw.vwg\vwdfs\K-E\EG\1534\Groups\EGPE-4\03_Messung\02_BEV\VW120_7_PA\VB+RW\VW1200_9_0051_Autostart_180629_NEFZ1_H79\180705_2NEFZ\Auswertung_VW1200_9_0051_Autostart_180705_2NEFZ.xlsb'

    res = loader_TemplateBasis_180305(wb_path)
    print(res)

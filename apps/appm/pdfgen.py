from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def pdf_printer(request, datalist, idevents, ratsiya):
    doc = SimpleDocTemplate(str(idevents), pagesize=landscape(letter))
    elements = []
    if ratsiya:
        # T/r n0 Seriya nomer Ism Familiya Soxa xizmat Tel nomer Qaytarildi
        data = [['T/r ', 'N_', 'Seriya nomer', 'Ism Familiya', 'Soxa xizmat', 'Tel nomer', 'Imzo', 'Qaytarildi']]
        tr = 0
        for obyekt in datalist:
            datas = []
            tr += 1
            datas.append(tr)
            datas.append(obyekt[0].rcode)
            datas.append(obyekt[0].qr_code)
            data.append(datas)

        t = Table(data, 100, 50)
        t._argW[0], t._argW[1], t._argW[2], t._argW[3], t._argW[4] = 30, 30, 100, 150, 150

    else:
        # T/r n0 Seriya nomer Ism Familiya Soxa xizmat Tel nomer Qaytarildi
        data = [['T/r ', 'Katalog', 'Model', 'QR Code']]
        tr = 0
        for obyekt in datalist:
            datas = []
            tr += 1
            datas.append(tr)
            datas.append(obyekt[0].katalog)
            datas.append(obyekt[0].model)
            datas.append(obyekt[0].qr_code)
            data.append(datas)

        t = Table(data, 100, 50)

        t._argW[0] = 50
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                           ('VALIGN', (0, 0), (0, -1), 'TOP'),
                           ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ]))
    elements.append(t)
    # write the document to disk
    doc.build(elements)
    import shutil
    shutil.move(str(idevents), 'pdf/' + str(idevents))
    return FileResponse(open('pdf/' + str(idevents), 'rb'), as_attachment=False,
                        filename='IIV_' + str(idevents) + '.pdf')

from fpdf import FPDF
from datetime import datetime
# from pymongo import MongoClient
# from dotenv import dotenv_values
# from flask import Flask, redirect, url_for, render_template, request, session, flash, abort
# from routes import order_pages, user_pages

# import time
# import copy


# config = dotenv_values(".env")

# password_mg_db = config["MONGODB_PWD"]
# connection_string = f"mongodb+srv://herman:{password_mg_db}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
# client = MongoClient(connection_string)
# db = client.packinglist

# user_collection = db.users
# orders_collection = db.lsorders
# last_order_collection = db.lastorder


# def format_date_now():
#     if datetime.today().day < 10:
#         dag = f"0{datetime.today().day}"
#     else:
#         dag = datetime.today().day

#     dd_now = f"{dag}-{datetime.today().month}-{datetime.today().year}-{datetime.today().hour}h{datetime.today().minute}m"
#     return dd_now


# orders_from_db = orders_collection.find(
#     {"number": {"$lte": 354707}}).sort("number", -1).limit(1)

# orders_from_db = orders_collection.find(
#     {"flagPrinted": False}).sort("id", -1).limit(1)


def create_orderbonnen(orders, hoogste, aantal_pag):
    pdf = FPDF()
    machine = '600 dpi, 100/50/1000 D 90, H2, P180'
    machine2 = 'X 252 30/20/400'
    logo = "./static/img/Logo-brianto.png"
    dummy = "./static/img/dummy.png"

    def format_date(str):
        date_format = '%Y-%m-%dT%H:%M:%S+02:00'
        formatted_date = datetime.strptime(
            str, date_format).strftime("%d-%m-%Y %H:%M")
        return formatted_date

    # solve unicode issues hith latin-1 supported fonts
    def solve_unicode(str):
        formatted_1 = str.replace('’', '-')
        formatted_str = formatted_1.encode(
            'latin1', errors="replace").decode('latin1')

        return formatted_str

    def print_products(product):

        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(
            115, 10, f'{product["productTitle"]} {product["variantTitle"]}', 0, 0, 'L')
        pdf.set_font('helvetica', '', 10)
        pdf.cell(25, 10, f'{product["articleCode"]}', 0, 0, 'C')
        pdf.cell(25, 10, '998877', 0, 0, 'C')
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(15, 10, f'{product["quantityOrdered"]}', 0, 0, 'C')
        pdf.set_font('Times', '', 14)
        pdf.cell(15, 10, 'O', 0, 1, 'C')
        pdf.set_font('helvetica', '', 10)
        cord_y = pdf.get_y()
        pdf.set_font('helvetica', '', 9)
        pdf.multi_cell(80, 5, f'{product["productie_inst_1"]}', 0, 1, 'L')
        pdf.multi_cell(80, 5, f'{product["productie_inst_2"]}', 0, 1, 'L')
        if product["jpgFileName"]:
            try:

                pdf.image(f'/Users/herma/stack2/prints/{product["jpgFileName"]}', x=90, y=cord_y+3, w=0, h=40, type='',
                          link='')
                pdf.set_y(cord_y + 45)
            except:
                pdf.image(dummy, x=90, y=cord_y+5, w=0, h=20, type='',
                          link='')
                pdf.set_y(cord_y + 25)
        else:
            pdf.image(dummy, x=90, y=cord_y+5, w=0, h=20, type='',
                      link='')
            pdf.set_y(cord_y + 25)

    # CREATE PDF
    # HEADING

    for order in orders:

        pdf.add_page()
        pdf.set_fill_color(211, 211, 211)
        pdf.image(logo, x=None, y=None, w=50, h=0, type='',
                  link='')
        pdf.set_xy(x=70, y=10)
        pdf.set_font('helvetica', 'B', 20)
        pdf.cell(130, 10, 'PRODUCTIEBON', 0, 1, 'R')
        pdf.set_font('helvetica', '', 20)
        pdf.cell(190, 8, f'Ordernr.Lightspeed: {order["number"]}', 0, 1, 'R')
        pdf.set_font('helvetica', '', 12)
        pdf.cell(
            60, 8, f'Besteldatum: {format_date(order["created_at"])}', 0, 0, 'L')
        pdf.set_font('helvetica', '', 16)
        pdf.cell(130, 8, f'Ordernr.Exact: {order["number"]}', 0,  1, 'R')
        # pdf.cell(80)
        pdf.set_font('helvetica', '', 10)
        pdf.cell(115, 8, 'Omschrijving', 0, 0, 'L', True)
        pdf.cell(25, 8, 'Articelcode', 0, 0, 'C', True)
        pdf.cell(25, 8, 'Magazijn', 0, 0, 'C', True)
        pdf.cell(15, 8, 'Aantal', 0, 0, 'C', True)
        pdf.cell(10, 8, '', 0, 1, 'C', True)

    # PRODUCTEN
        for product in order["products"]:
            if pdf.get_y() < 240:
                print_products(product)
                # pdf.set_font('helvetica', 'B', 10)
                # pdf.cell(
                #     115, 10, f'{product["productTitle"]} {product["variantTitle"]}', 0, 0, 'L')
                # pdf.set_font('helvetica', '', 10)
                # pdf.cell(25, 10, f'{product["articleCode"]}', 0, 0, 'C')
                # pdf.cell(25, 10, '998877', 0, 0, 'C')
                # pdf.set_font('helvetica', 'B', 11)
                # pdf.cell(15, 10, f'{product["quantityOrdered"]}', 0, 0, 'C')
                # pdf.set_font('Times', '', 14)
                # pdf.cell(15, 10, 'O', 0, 1, 'C')
                # pdf.set_font('helvetica', '', 10)
                # cord_y = pdf.get_y()
                # print(cord_y)
                # pdf.set_font('helvetica', '', 9)
                # pdf.multi_cell(80, 5, f'{machine}', 0, 1, 'C')
                # pdf.multi_cell(80, 5, f'{machine}', 0, 1, 'C')
                # if product["jpgFileName"]:
                #     try:

                #         pdf.image(f'/Users/herma/stack2/prints/{product["jpgFileName"]}', x=90, y=cord_y+3, w=0, h=40, type='',
                #                   link='')
                #         pdf.set_y(cord_y + 45)
                #     except:
                #         pdf.image(dummy, x=90, y=cord_y+5, w=0, h=20, type='',
                #                   link='')
                #         pdf.set_y(cord_y + 25)
                # else:
                #     pdf.image(dummy, x=90, y=cord_y+5, w=0, h=20, type='',
                #               link='')
                #     pdf.set_y(cord_y + 25)

            else:
                pdf.add_page()
                print_products(product)

    # SHIPMENT
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(70, 10, f'{order["shipmentTitle"]}', 0, 1, 'L')

    # OPMERKINGENVELD
        pdf.set_font('helvetica', '', 9)
        if order["comment"] != "":
            pdf.multi_cell(
                180, 5, f'Opmerkingen: {solve_unicode(order["comment"])}', 0, 1, 'L')

    # FOOTER
        if pdf.get_y() < 245:
            pdf.set_y(245)
        else:
            pdf.add_page()
            pdf.set_y(245)

        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(70, 10, 'Verzendadres', 0, 0, 'L')
        pdf.cell(70, 10, 'Contactinformatie', 0, 1, 'L')
        pdf.set_font('helvetica', '', 9)
        if order["addressShippingCompany"] != False:
            pdf.cell(
                70, 5, f'{solve_unicode(order["addressShippingCompany"])}', 0, 0, 'L')
        else:
            pdf.cell(
                70, 5, f'{solve_unicode(order["addressShippingName"])}', 0, 0, 'L')

        pdf.cell(
            70, 5, f'{solve_unicode(order["firstname"])} {solve_unicode(order["lastname"])}', 0, 1, 'L')

        pdf.cell(
            70, 5, f'{solve_unicode(order["addressShippingStreet"])} {order["addressShippingNumber"]} {order["addressShippingExtension"]}', 0, 0, 'L')
        pdf.cell(70, 5, f'{order["email"]}', 0, 1, 'L')

        pdf.cell(
            70, 5, f'{order["addressShippingZipcode"]} {solve_unicode(order["addressShippingCity"])}', 0, 0, 'L')
        pdf.cell(70, 5, f'{order["mobile"]}', 0, 1, 'L')
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(
            70, 5, f'{order["addressShippingCountry"]}', 0, 1, 'L')

    pdf.output(
        f'/Users/herma/stack2/pdf/Bonnen-{hoogste}-p-{aantal_pag}.pdf', 'F')
#       pdf.output(f'/home/hodb/STACK/pdf/Bonnen-{hoogste}-p-{aantal_pag}.pdf', 'F')


if __name__ == "__main__":
    print(__name__, ": VAN FETCH CREATE-PDF")
    # fetch_and_save_lsorders(last_order)
    # create_orderbonnen(orders_from_db, 777, 2)
    # print("done")
    # for order in gevonden_orders_copy:

    #     print(order["number"], 2)

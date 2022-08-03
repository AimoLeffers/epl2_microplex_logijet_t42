import socket
import logging
from datetime import datetime


def main():
    logging.basicConfig(level=logging.DEBUG)
    message = setup_message(p_nr="P151104.SET",
                            p_customer="Test \"Investment\" Unternehmensgruppe, Test Vermögensverwaltungs-GmbH & Co. Kg",
                            p_desc="Rinderkennzeichnungsfleischetikettierungsüberwachungsaufgabenübertragungsgesetz",
                            basket_nr="92",
                            print_date=datetime.today().strftime('%d.%m.%Y'))

    tcp_print('192.168.1.134', message)
    return


def setup_message(p_nr: str, p_customer: str, p_desc: str, basket_nr: str, print_date: str):
    """
    Provides the EPL2 formated string as bytes to print a project label
    :param p_nr: Projectnumber
    :param p_customer: Name of the customer
    :param p_desc: Decription of the project
    :param basket_nr: number of the product basket
    :param print_date: date of the printing
    :return:
    """
    max_len_per_line = 31
    len_p_customer = len(p_customer)
    len_p_desc = len(p_desc)
    print_msg = ""

    """clean up Umlaute"""
    # Quick and dirty hack to prevent ugly prints. There migth be a better solution deeper within the EPL2 language.
    p_customer = p_customer.replace("ö", "oe")
    p_customer = p_customer.replace("ü", "ue")
    p_customer = p_customer.replace("ä", "ae")
    p_customer = p_customer.replace("Ö", "oe")
    p_customer = p_customer.replace("Ü", "ue")
    p_customer = p_customer.replace("Ä", "ae")
    p_customer = p_customer.replace("\"", "")

    p_desc = p_desc.replace("ö", "oe")
    p_desc = p_desc.replace("ü", "ue")
    p_desc = p_desc.replace("ä", "ae")
    p_desc = p_desc.replace("Ö", "oe")
    p_desc = p_desc.replace("Ü", "ue")
    p_desc = p_desc.replace("Ä", "ae")

    p_desc = p_desc.replace("\"", "")

    """Add the projectnumber in the first line"""
    print_msg += ascii_text_formater(50, 50, 4, p_nr, font_size_mult_x=6, font_size_mult_y=6)

    """Adding the customer name"""
    if len_p_customer > max_len_per_line:
        """If there is too much text for one line, split the string and print the rest on the second line"""
        p_customer_first_line = p_customer[:max_len_per_line]
        p_customer_second_line = p_customer[max_len_per_line:]

        print_msg += ascii_text_formater(50, 280, 4, p_customer_first_line, font_size_mult_x=2, font_size_mult_y=2)
        print_msg += ascii_text_formater(50, 350, 4, p_customer_second_line, font_size_mult_x=2, font_size_mult_y=2)

    else:
        print_msg += ascii_text_formater(50, 280, 4, p_customer, font_size_mult_x=2, font_size_mult_y=2)

    """Adding the project description"""
    if len_p_desc > max_len_per_line:
        """If there is too much text for one line, split the string and print the rest on the second line"""
        p_desc_first_line = p_desc[:max_len_per_line]
        p_desc_second_line = p_desc[max_len_per_line:]

        print_msg += ascii_text_formater(50, 500, 4, p_desc_first_line, font_size_mult_x=2, font_size_mult_y=2)
        print_msg += ascii_text_formater(50, 570, 4, p_desc_second_line, font_size_mult_x=2, font_size_mult_y=2)

    else:
        print_msg += ascii_text_formater(50, 500, 4, p_desc, font_size_mult_x=2, font_size_mult_y=2)

    """Adding the basketnumber"""
    print_msg += ascii_text_formater(50, 700, 2, f"Warenkorbnummer: {basket_nr}")
    """Adding the print date"""
    print_msg += ascii_text_formater(50, 725, 2, f"Druckdatum: {print_date}")
    print_msg += "P1\n"
    return bytes(print_msg, 'utf-8')


def ascii_text_formater(x_pos: int,
                        y_pos: int,
                        resident_font: int,
                        message: str,
                        rotation: int = 0,
                        font_size_mult_x: int = 1,
                        font_size_mult_y: int = 1,
                        orientation: str = 'N'):
    """
    This function provides the format to print an ASCII text string
    :param x_pos: Horizontal start position (X) in dots
    :param y_pos: Vertical start position (Y) in dots
    :param rotation: Rotation (0 = None, 1 = 90°, 2 = 180°, 3 = 270°)
    :param resident_font: Font selection (1 to 5)
    :param message: Textmessage that will be printed
    :param font_size_mult_x: Horizontal multiplier, expands the text horizontally (1 to 9)
    :param font_size_mult_y: Vertical multiplier, expands the text vertically (1 to 9)
    :param orientation:  N for normal or R for reverse image (Defaults to N = normal)
    :return:
    """

    command_string = f"A{x_pos}," \
                     f"{y_pos}," \
                     f"{rotation}," \
                     f"{resident_font}," \
                     f"{font_size_mult_x}," \
                     f"{font_size_mult_y}," \
                     f"{orientation}," \
                     f"\"{message}\"" \
                     f"\n"

    return command_string


def tcp_print(printer_ip: str, print_message: bytes, printer_port: int = 9100):
    """
    Prints a message in RAW-Format on the specified printer
    :param printer_ip:  IP-Adresse of the printer
    :param printer_port: Port of the printer (Defaults to 9100)
    :param print_message: the message, which will be send
    :return:
    """
    logging.info(f"IP: {printer_ip}")
    logging.info(f"Port: {printer_port}")
    logging.info(f"Port: {print_message}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((printer_ip, printer_port))
    sock.sendall(print_message)
    sock.close()
    return


if __name__ == "__main__":
    main()

import smtplib, ssl, getpass, csv, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465  # For SSL
password = getpass.getpass("Type your password and press enter: ")
from_address = "your@mail.com"

# Create the plain-text and HTML version of your message
text = u"""Subject: Odoo - Impuesto Compra en Dolares

Estimado {name},

Queremos recordarle que Odoo le ofrece un 20% de descuento al pagar por 1 año por su base de datos.

La siguiente información muestra el precio del contrato con el descuento:

- Mensualidad: ${price}
- Total por 12 meses: ${year}
- Total con descuento: ${promo}
- Ahorro: ${discount}

Por favor, avíseme si le interesa recibir una cotización con los detalles.

Número de contrato: {reference}

Saludos cordiales,

Isaac Benitez
Customer Success Manager

Odoo Inc.
250 Executive Park Blvd. Suite 3400
San Francisco, CA 94134
Tel: +1 (650) 262-6821"""

# Create a secure SSL context
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(from_address, password)
    with open("data.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for reference, name, email, price in reader:
            year = float(price)*12
            promo = year*0.8
            discount = year*0.2
            server.sendmail(
                from_address,
                email,
                text.format(
                    reference=reference,
                    name=name, 
                    price='{:,.2f}'.format(float(price)), 
                    year='{:,.2f}'.format(year), 
                    promo='{:,.2f}'.format(promo), 
                    discount='{:,.2f}'.format(discount)
                ).encode("utf-8"),
            )
            print('>>> Email sent to ' + name + '... Waiting 5 seconds...')
            time.sleep(5)

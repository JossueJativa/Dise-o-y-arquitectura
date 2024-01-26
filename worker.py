# Worker script to consume tasks from RabbitMQ and send emails
# worker.py
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pika

def send_email_and_generate_cert(username, course, date, email, pdf_content):
    try:
        remitente_correo = "jativatamayojossuedavid@gmail.com"
        remitente_contrasena = "bylb bbgv jzps jpux"  # Replace with your password
        destinatario_correo = email

        mensaje = MIMEMultipart()
        mensaje["From"] = remitente_correo
        mensaje["To"] = destinatario_correo
        mensaje["Subject"] = "Certificado adjunto"

        adjunto = MIMEApplication(pdf_content.encode('utf-8'), _subtype="pdf")  # Convert string to bytes
        adjunto.add_header("content-disposition", "attachment", filename="certificado.pdf")
        mensaje.attach(adjunto)

        servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        servidor_smtp.starttls()
        servidor_smtp.login(remitente_correo, remitente_contrasena)
        servidor_smtp.sendmail(remitente_correo, destinatario_correo, mensaje.as_string())
        servidor_smtp.quit()

        print("Se envió la información")
    except Exception as e:
        print("No se pudo enviar el correo. Error:", str(e))

def callback(ch, method, properties, body):
    task_data = json.loads(body.decode('utf-8'))
    send_email_and_generate_cert(**task_data)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Change to your RabbitMQ server
        channel = connection.channel()

        channel.queue_declare(queue='email_queue')
        channel.basic_consume(queue='email_queue', on_message_callback=callback)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except Exception as e:
        print("Error starting worker:", str(e))

if __name__ == '__main__':
    start_worker()
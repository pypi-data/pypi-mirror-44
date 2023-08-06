from . import site_list
import smtplib

class MailHandler:
    def __init__(self, logger, application, suppression_time, local_email=None, local_password=None):
        self.logger = logger
        self.app_name = application
        self.suppression_time = suppression_time
        self.local_email = local_email
        self.local_password = local_password

    def setup(self):
        if not self.local_email or not self.local_password:
            try:
                self.smtp = smtplib.SMTP('localhost')
                self.smtp.set_debuglevel(1)  # 1 On 0 Off
                return
            except Exception as e:
                self.logger.log('Error setting up email client: ' + str(e))
        
        self.smtp = smtplib.SMTP('smtp.gmail.com:587')
        self.smtp.set_debuglevel(0)  # 1 On 0 Off
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(self.local_email,
                        self.local_password)

    def send_email(self, brand_name, sender, recipients, subject, body):
        self.setup()
        brand = 'none' if brand_name is None else brand_name
        send_status = self.suppression_time == 0 or site_list.send_for_brand(brand, self.suppression_time)

        if send_status:
            message = self.build_message(sender,
                                         recipients,
                                         subject,
                                         body)
            self.send(sender, recipients, message)
            self.smtp.quit()

            if self.suppression_time > 0:
                site_list.update_last_email_time(brand)

    def build_message(self, sender, recipients, subject, body):
        return '\r\n'.join([
            'From: ' + sender,
            'To: ' + ', '.join(recipients),
            'Subject: ' + subject,
            '',
            body
        ])

    def send(self, sender, recipients, message):
        try:
            self.smtp.sendmail(sender, recipients, message)
        except Exception as e:
            self.logger.log('Error trying to send email: ' + str(e))

from core.database import influx
from core.email import mail_handler
from core.log import seq
import schedule
import time


class Runner:
    def run(self, app_name, entry_point, server=True, email_active=True, suppression_time=0, local_email=None, local_password=None, interval=None, start_times=None):
        self.logger = seq.Seq(app_name)
        self.database = influx.Influx(self.logger, app_name)
        self.email_active = email_active
        
        if self.email_active:
            if server:
                self.mailer = mail_handler.MailHandler(self.logger, app_name, suppression_time)
            elif not server and (local_email and local_password):
                self.mailer = mail_handler.MailHandler(self.logger, app_name, suppression_time,
                                                       local_email, local_password)
            else:
                msg = 'Mailer not created - Set server to True or supply local_email and local_password parameters'
                print(msg)
                self.log(msg, severity='info')
                return
                
        if interval and start_times:
            msg = 'Can only pass either "interval" or "start_times" as arguments to run function, not both'
            print(msg)
            self.log(msg)
            return
        elif interval:
            msg = 'Scheduler set to run every ' + str(interval) + ' seconds'
            print(msg)
            self.log(msg, severity='info')
            schedule.every(interval).seconds.do(entry_point)
        elif start_times:
            for start_time in start_times:
                msg = 'Scheduler set to run every day at ' + str(start_time)
                print(msg)
                self.log(msg, severity='info')
                schedule.every().day.at(start_time).do(entry_point)        
        else:
            msg = 'No "interval" or "start_times" arguments passed to run function'
            print(msg)
            self.log(msg)
            return
        
        while True:
            schedule.run_pending()
            time.sleep(1)

    # logging
    def log(self, message, severity='error', token_id=None):
        self.logger.log(message, severity, token_id)

    # database
    def write_response_time(self, response_time):
        self.database.record_response_time(response_time)
        
    def write_status(self, status):
        self.database.record_status(status)

    def write_brand_status(self, brand, status):
        self.database.record_brand_status(brand, status)
    
    def write_service_status(self, brand, ping, status):
        self.database.record_service_status(brand, ping, status)
    
    def write_website_status(self, brand, ping, status, content):
        self.database.record_website_status(brand, ping, status, content)

    # email
    def send_email(self, brand, sender, recipients, subject, body):
        if self.email_active:
            self.mailer.send_email(brand, sender, recipients, subject, body)
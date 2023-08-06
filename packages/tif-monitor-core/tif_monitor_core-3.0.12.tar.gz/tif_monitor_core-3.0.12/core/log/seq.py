from core.settings import settings
import logging
import seqlog


class Seq:

    def __init__(self, app_name):
        seqlog.log_to_seq(
            server_url=settings.seq['url'],
            batch_size=1,
            api_key=settings.seq['key'],
            auto_flush_timeout=0.0001,
            override_root_logger=True
        )
        self.seq_logger = logging.getLogger()
        self.seq_logger.name = 'Monitor Logger'
        self.seq_logger.setLevel(logging.INFO)
        self.log_message = 'Message: {message}. appName: {appName}. TokenID: {token_id}'
        self.app_name = app_name

    def log(self, message, severity='error', token_id=None):
        """ Logs into SEQ using the settings in the host settings.py file.

            Severity Types:
                - Error
                - Critical
                - Warning
                - Info
                - Debug
        """

        message = str.lower(message)
        severity = str.lower(severity)
        token_id = "None" if token_id is None else str.lower(token_id)
        app = self.app_name

        if severity == 'error':
            self.seq_logger.error(self.log_message, message=message, appName=app, token_id=token_id)

        elif severity == 'critical':
            self.seq_logger.critical(self.log_message, message=message, appName=app, token_id=token_id)

        elif severity == 'warning':
            self.seq_logger.warning(self.log_message, message=message, appName=app, token_id=token_id)

        elif severity == 'info':
            self.seq_logger.info(self.log_message, message=message, appName=app, token_id=token_id)

        elif severity == 'debug':
            self.seq_logger.debug(self.log_message, message=message, appName=app, token_id=token_id)

        else:
            self.seq_logger.error('Message: {message}. appName: {appName}.', message=message, appName=app)
            print('Severity: {severity} was not found so logging error\n'.format(severity=severity))

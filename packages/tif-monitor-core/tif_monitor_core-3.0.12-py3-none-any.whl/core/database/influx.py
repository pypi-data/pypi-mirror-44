from core.settings import settings
from influxdb import InfluxDBClient


class Influx:

    def __init__(self, logger, app_name):    
        self.client = InfluxDBClient(host=settings.influx['host'], 
                                     port=settings.influx['port'], 
                                     database=settings.influx['db_name'])
        self.logger = logger
        self.app_name = app_name

    def record_response_time(self, response_time):
        """ Logs response times to InFluxDB.

        :return: Success Or Failure
        """
        print('Response Time to Log: ' + str(response_time))

        points = [
            {
                'measurement': self.app_name,
                'fields': {'response_times': response_time}
            }
        ]

        self.insert_one(points)

    def record_status(self, status):
        print('Recording ' + str(status))

        points = [
            {
                'measurement': self.app_name,
                'fields': {'result': status}
            }
        ]

        self.insert_one(points)

    def record_brand_status(self, brand, status):
        print('Recording ' + str(status) + ' for ' + brand)

        points = [
            {
                'measurement': self.app_name,
                'tags': {'brand': brand},
                'fields': {'result': status}
            }
        ]

        self.insert_one(points)

    def record_service_status(self, brand, ping, status):
        print('Recording service status' + str(status) + ' for ' + str(brand))

        points = [
            {
                'measurement': self.app_name,
                'tags': {'brand': brand},
                'fields': {'ping': ping,
                            'status': status}
            }
        ]

        self.insert_one(points)

    def record_website_status(self, brand, ping, status, content):
        print('Recording website status' + str(status) + ' for ' + str(brand))

        points = [
            {
                'measurement': self.app_name,
                'tags': {'brand': brand},
                'fields': {'ping': ping,
                            'status': status,
                            'content_code': content}
            }
        ]

        self.insert_one(points)

    def insert_one(self, points):
        try:
            self.client.write_points(points, protocol=u'json')
        except Exception as ex:
            print('Unable to record response time: ' + str(ex))
            self.logger.log(message='Unable to record response time: ' + str(ex))

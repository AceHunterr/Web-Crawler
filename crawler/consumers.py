import json
from channels.generic.websocket import WebsocketConsumer
from .utils import crawl

import logging

logger = logging.getLogger(__name__)

class CrawlConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        logger.debug('WebSocket connection established')
        self.send(text_data=json.dumps({
            'message': 'WebSocket connection established... Website is being crawled right now'
        }))

    def disconnect(self, close_code):
        logger.debug(f'WebSocket disconnected with close code: {close_code}')
        pass

    def receive(self, text_data):
        logger.debug(f'Received message: {text_data}')
        text_data_json = json.loads(text_data)
        url = text_data_json['url']

        def report_progress(current_url):
            logger.debug(f'Visited URL: {current_url}')
            self.send(text_data=json.dumps({
                'url': current_url
            }))

        self.send(text_data=json.dumps({'message': f'Starting crawl for {url}'}))
        report = crawl(url, report_progress=report_progress)
        # print("report",report)
        self.send(text_data=json.dumps({'report': report}))

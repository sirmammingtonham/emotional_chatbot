import os
from ibm_watson import ToneAnalyzerV3
from ibm_watson.tone_analyzer_v3 import ToneInput
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .tone_models import Tone

class ToneAnalyzer:
    def __init__(self):
        API_KEY = os.environ.get('TONE_ANALYZER_APIKEY')
        URL = os.environ.get('TONE_ANALYZER_URL')

        # Authentication via IAM
        authenticator = IAMAuthenticator(API_KEY)
        self.service = ToneAnalyzerV3(
            version='2017-09-21',
            authenticator=authenticator)
        self.service.set_service_url(URL)

    def analyze(self, input):
        tone_input = ToneInput(input)
        tone = self.service.tone(tone_input=tone_input, content_type="application/json").get_result()
        return Tone(input, tone)

# some tests
if __name__ == "__main__":
    analyzer = ToneAnalyzer()
    print(analyzer.analyze('I am very happy. It is a good day.'))
    print(analyzer.analyze('Everything sucks.'))
import json
from datetime import datetime
from unittest.mock import patch

import django.conf
from django.test import TestCase

import django_vox.backends.postmark_email
import django_vox.backends.template_email
import django_vox.backends.twilio


def mocked_requests_post(url, _data=None, json=None, **_kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        @property
        def text(self):
            return str(self.json_data)

        @property
        def ok(self):
            return self.status_code // 100 == 2

    if url == django_vox.backends.postmark_email.Backend.ENDPOINT:
        if not (json.get('TemplateAlias') or json.get('TemplateId')):
            return MockResponse(
                {'ErrorCode': "403", 'Message': 'details'}, 422)
        else:
            return MockResponse({
                "To": "george@example.org",
                "SubmittedAt": "2014-02-17T07:25:01.4178645-05:00",
                "MessageID": "0a129aee-e1cd-480d-b08d-4f48548ff48d",
                "ErrorCode": 0, "Message": "OK"}, 200)
    elif url == 'https://webhook.example':
        return MockResponse('', 200)
    return MockResponse(None, 404)


class TestTwilioBackend(TestCase):

    TEXT = 'Here is a text message \n\n for {{ you }}'
    PARAMS = {'you': 'me'}
    SUBJECT = 'IGNORED'
    MESSAGE = 'Here is a text message \n\n for me'
    PREVIEW = 'Here is a text message <br/><br/> for me'

    @classmethod
    def test_build_message(cls):
        backend = django_vox.backends.twilio.Backend()
        message = backend.build_message(cls.SUBJECT, cls.TEXT, cls.PARAMS, [])
        assert cls.MESSAGE == message

    @classmethod
    def test_preview_message(cls):
        backend = django_vox.backends.twilio.Backend()
        message = backend.preview_message(cls.SUBJECT, cls.TEXT, cls.PARAMS)
        assert cls.PREVIEW == message

    def test_send_message(self):
        backend = django_vox.backends.twilio.Backend()
        message = backend.build_message(
            self.SUBJECT, self.TEXT, self.PARAMS, [])
        with patch('twilio.rest.Client'):
            with self.assertRaises(django.conf.ImproperlyConfigured):
                backend.send_message('+321', ['+123'], message)
            with self.settings(DJANGO_VOX_TWILIO_ACCOUNT_SID='abc',
                               DJANGO_VOX_TWILIO_AUTH_TOKEN='secret'):
                backend.send_message('+321', ['+123'], message)
                import twilio.rest
                client = twilio.rest.Client
                assert len(client.mock_calls) > 1
                assert client.mock_calls[0][0] == ''  # class instantiation
                fname, args, kwargs = client.mock_calls[1]
                assert fname == '().messages.create'
                assert args == ()
                assert len(kwargs) == 3
                assert '+123' == kwargs['to']
                assert '+321' == kwargs['from_']
                assert self.MESSAGE == kwargs['body']


class TestPostmarkBackend(TestCase):

    TEXT = 'line 1 : {{ line_1 }}\n' \
           'line 2 : {{ line_2 }}\n' \
           'line 3 : {{ line_3 }}\n' \
           'line 4 : {{ line_4 }}\n' \
           '\n\n' \
           'c\'est vide'
    PARAMS = {
        'line_1': 'poisson un', 'line_2': 'poisson deux',
        'line_3': 'poisson rouge', 'line_4': 'poisson bleu'}
    SUBJECT = 'SUBJECT'
    MESSAGE = '<html>\n' \
              '<h1>SUBJECT</h1>\n' \
              '<dl>\n' \
              '<dt>line 1</dt><dd>poisson un</dd>\n' \
              '<dt>line 2</dt><dd>poisson deux</dd>\n' \
              '<dt>line 3</dt><dd>poisson rouge</dd>\n' \
              '<dt>line 4</dt><dd>poisson bleu</dd>\n' \
              '<dt>c\'est vide</dt><dd></dd>\n' \
              '</dl>\n' \
              '</html>'
    PREVIEW = MESSAGE

    @classmethod
    def test_build_message(cls):
        backend = django_vox.backends.postmark_email.Backend()
        message = backend.build_message(
            cls.SUBJECT, cls.TEXT, cls.PARAMS, [])
        assert cls.MESSAGE == message

    @classmethod
    def test_preview_message(cls):
        backend = django_vox.backends.postmark_email.Backend()
        message = backend.preview_message(cls.SUBJECT, cls.TEXT, cls.PARAMS)
        assert cls.PREVIEW == message

    def test_send_message(self):
        backend = django_vox.backends.postmark_email.Backend()
        bad_message = backend.build_message(
            '', self.TEXT, self.PARAMS, [])
        message = backend.build_message(
            self.SUBJECT, self.TEXT, self.PARAMS, [])
        from_address = django.conf.settings.DEFAULT_FROM_EMAIL
        to_addresses = ['george@example.org']
        with patch('requests.post', side_effect=mocked_requests_post):
            with self.assertRaises(django.conf.ImproperlyConfigured):
                backend.send_message(from_address, to_addresses, message)
            with self.settings(DJANGO_VOX_POSTMARK_TOKEN='token'):
                with self.assertRaises(RuntimeError):
                    backend.send_message(from_address, to_addresses,
                                         bad_message)
                backend.send_message(from_address, to_addresses, message)
                import requests
                check_model = requests.post.mock_calls[1][2]['json'][
                    'TemplateModel']
                assert check_model['line 1'] == 'poisson un'
                assert check_model['line 2'] == 'poisson deux'
                assert "c'est vide" in check_model


class TestJsonWebhookBackend(TestCase):

    TEXT = 'birthday : {{ birthday | date:"r" }}\n' \
           'empty: {{ null_value | default:"blank" }}\n' \
           'html: <i>{{ html }}</i>\n' \
           '\n'
    PARAMS = {
        'birthday': datetime(1984, 12, 11),
        'html': '<b>BOO!</b>',
        'null_value': None}
    MESSAGE = '<html>\n' \
              '<dl>\n' \
              '<dt>birthday</dt><dd>Tue, 11 Dec 1984 00:00:00 -0600</dd>\n' \
              '<dt>empty</dt><dd>blank</dd>\n' \
              '<dt>html</dt><dd><i>&lt;b&gt;BOO!&lt;/b&gt;</i></dd>\n' \
              '</dl>\n' \
              '</html>'
    PREVIEW = MESSAGE

    @classmethod
    def test_build_message(cls):
        backend = django_vox.backends.json_webhook.Backend()
        message = backend.build_message('', cls.TEXT, cls.PARAMS, [])
        assert cls.MESSAGE == message

    @classmethod
    def test_preview_message(cls):
        backend = django_vox.backends.json_webhook.Backend()
        message = backend.preview_message('', cls.TEXT, cls.PARAMS)
        assert cls.PREVIEW == message

    def test_send_message(self):
        backend = django_vox.backends.json_webhook.Backend()
        message = backend.build_message('', self.TEXT, self.PARAMS, [])
        bad_address = 'https://not.example'
        address = 'https://webhook.example'
        with patch('requests.post', side_effect=mocked_requests_post):
            with self.assertRaises(RuntimeError):
                backend.send_message('', [bad_address], message)
            backend.send_message('', [address], message)
            import requests
            check_model = requests.post.mock_calls[0][2]['json']
            assert check_model['birthday'] == \
                'Tue, 11 Dec 1984 00:00:00 -0600'
            assert check_model['empty'] == 'blank'
            # not sure if this is actually what we want, but it's what
            # currently happens
            assert check_model['html'] is None


class TestTemplateEmailBackend(TestCase):

    TEXT = '{% block text_body%}' \
           'Here is a message \n\n for {{ you }}' \
           '{% endblock %}' \
           '{% block html_body %}' \
           '<p>Here is a message <br/><br/> for {{ you }}' \
           '{% endblock %}' \
                   ''
    PARAMS = {'you': 'me'}
    SUBJECT = 'SUBJECT'
    MESSAGE = {'subject': 'SUBJECT',
               'text': 'Here is a message \n\n for me',
               'html': '<p>Here is a message <br/><br/> for me'}
    PREVIEW = '<p>Here is a message <br/><br/> for me'

    @classmethod
    def test_build_message(cls):
        backend = django_vox.backends.template_email.Backend()
        message = backend.build_message(cls.SUBJECT, cls.TEXT, cls.PARAMS, [])
        obj = json.loads(message)
        assert cls.MESSAGE == obj

    @classmethod
    def test_preview_message(cls):
        backend = django_vox.backends.template_email.Backend()
        message = backend.preview_message(cls.SUBJECT, cls.TEXT, cls.PARAMS)
        assert cls.PREVIEW == message

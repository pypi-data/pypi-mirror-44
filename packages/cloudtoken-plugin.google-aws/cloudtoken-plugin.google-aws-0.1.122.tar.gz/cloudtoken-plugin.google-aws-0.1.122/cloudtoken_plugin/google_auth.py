# Imported and Modified from aws-google-auth module under the MIT license
# https://github.com/cevoaustralia/aws-google-auth
# MIT License
#
# Copyright holders: (C) 2016 Cevo Australia Pty Ltd, 2018 Atlassian Pty Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
from u2flib_host import u2f, exc, appid
from u2flib_host.constants import APDU_USE_NOT_SATISFIED
import io
import json
import os
import sys
import requests
from PIL import Image
from distutils.spawn import find_executable
from bs4 import BeautifulSoup
from requests import HTTPError
from six import print_ as print
from six.moves import urllib_parse, input


class ExpectedGoogleException(Exception):
    def __init__(self, *args):
        super(ExpectedGoogleException, self).__init__(*args)


class Google:
    def __init__(self, args, session):
        self.config = args
        self.base_url = 'https://accounts.google.com'
        self.session = session
        self.cont = None
        self.version = '0.0.28'

    @property
    def login_url(self):
        return self.base_url + "/o/saml2/initsso?idpid={}&spid={}&forceauthn=false".format(
            self.config.idp_id, self.config.sp_id)

    def check_for_failure(self, sess):
        if isinstance(sess.reason, bytes):
            # We attempt to decode utf-8 first because some servers
            # choose to localize their reason strings. If the string
            # isn't utf-8, we fall back to iso-8859-1 for all other
            # encodings. (See PR #3538)
            try:
                reason = sess.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = sess.reason.decode('iso-8859-1')
        else:
            reason = sess.reason

        if sess.status_code == 403:
            raise ExpectedGoogleException(u'{} accessing {}'.format(
                reason, sess.url))

        try:
            sess.raise_for_status()
        except HTTPError as ex:

            if self.config.debug:
                print("Saving failure trace in 'failure.html'")
                with open("failure.html", 'w') as out:
                    out.write(sess.text)
            raise ex

        return sess

    def post(self, url, data=None, json_data=None):
        try:
            response = self.check_for_failure(self.session.post(url, data=data, json=json_data))
        except requests.exceptions.ConnectionError as e:
            print(
                'There was a connection error, check your network settings: {}'.
                format(e))
            sys.exit(1)
        except requests.exceptions.Timeout as e:
            print('The connection timed out, please try again: {}'.format(e))
            sys.exit(1)
        except requests.exceptions.TooManyRedirects as e:
            print('The number of redirects exceeded the maximum allowed: {}'.
                  format(e))
            sys.exit(1)

        return response

    def get(self, url):
        try:
            response = self.check_for_failure(self.session.get(url))
        except requests.exceptions.ConnectionError as e:
            print(
                'There was a connection error, check your network settings: {}'.
                format(e))
            sys.exit(1)
        except requests.exceptions.Timeout as e:
            print('The connection timed out, please try again: {}'.format(e))
            sys.exit(1)
        except requests.exceptions.TooManyRedirects as e:
            print('The number of redirects exceeded the maximum allowed: {}'.
                  format(e))
            sys.exit(1)

        return response

    @staticmethod
    def parse_error_message(sess):
        response_page = BeautifulSoup(sess.text, 'html.parser')
        error = response_page.find('span', {'id': 'errorMsg'})

        if error is None:
            return None
        else:
            return error.text

    def do_login(self):
        self.session.headers['User-Agent'] = "AWS Sign-in/{} (Cevo aws-google-auth)".format(self.version)
        sess = self.get(self.login_url)
        if 'SAMLResponse' in sess.text:
            self.session_state = sess
            return
        if self.config.daemon:
            print("Cannot start daemon mode without an existing session. Please run cloudtoken without --daemon first")
            exit(1)
        # Collect information from the page source
        first_page = BeautifulSoup(sess.text, 'html.parser')
        gxf = first_page.find('input', {'name': 'gxf'}).get('value')
        self.cont = first_page.find('input', {'name': 'continue'}).get('value')
        page = first_page.find('input', {'name': 'Page'}).get('value')
        sign_in = first_page.find('input', {'name': 'signIn'}).get('value')
        account_login_url = first_page.find('form', {'id': 'gaia_loginform'}).get('action')

        payload = {
            'bgresponse': 'js_disabled',
            'checkConnection': '',
            'checkedDomains': 'youtube',
            'continue': self.cont,
            'Email': self.config.username,
            'gxf': gxf,
            'identifier-captcha-input': '',
            'identifiertoken': '',
            'identifiertoken_audio': '',
            'ltmpl': 'popup',
            'oauth': 1,
            'Page': page,
            'Passwd': '',
            'PersistentCookie': 'yes',
            'ProfileInformation': '',
            'pstMsg': 0,
            'sarp': 1,
            'scc': 1,
            'SessionState': '',
            'signIn': sign_in,
            '_utf8': '?',
        }

        # GALX is sometimes not there
        try:
            galx = first_page.find('input', {'name': 'GALX'}).get('value')
            payload['GALX'] = galx
        except:
            pass

        # POST to account login info page, to collect profile and session info
        sess = self.post(account_login_url, data=payload)

        self.session.headers['Referer'] = sess.url

        # Collect ProfileInformation, SessionState, signIn, and Password Challenge URL
        challenge_page = BeautifulSoup(sess.text, 'html.parser')

        profile_information = challenge_page.find('input', {
            'name': 'ProfileInformation'
        }).get('value')
        session_state = challenge_page.find('input', {
            'name': 'SessionState'
        }).get('value')
        sign_in = challenge_page.find('input', {'name': 'signIn'}).get('value')
        passwd_challenge_url = challenge_page.find('form', {
            'id': 'gaia_loginform'
        }).get('action')

        # Update the payload
        payload['SessionState'] = session_state
        payload['ProfileInformation'] = profile_information
        payload['signIn'] = sign_in
        payload['Passwd'] = self.config.password

        # POST to Authenticate Password
        sess = self.post(passwd_challenge_url, data=payload)

        response_page = BeautifulSoup(sess.text, 'html.parser')
        error = response_page.find(class_='error-msg')
        cap = response_page.find('input', {'name': 'logincaptcha'})

        # Were there any errors logging in? Could be invalid username or password
        # There could also sometimes be a Captcha, which means Google thinks you,
        # or someone using the same outbound IP address as you, is a bot.
        if error is not None:
            raise ExpectedGoogleException('Invalid username or password')

        self.check_extra_step(response_page)

        # Process Google CAPTCHA verification request if present
        if cap is not None:
            self.session.headers['Referer'] = sess.url

            sess = self.handle_captcha(sess, payload)

            response_page = BeautifulSoup(sess.text, 'html.parser')
            error = response_page.find(class_='error-msg')
            cap = response_page.find('input', {'name': 'logincaptcha'})

            # Were there any errors logging in? Could be invalid username or password
            # There could also sometimes be a Captcha, which means Google thinks you,
            # or someone using the same outbound IP address as you, is a bot.
            if error is not None:
                raise ExpectedGoogleException('Invalid username or password')

            self.check_extra_step(response_page)

            if cap is not None:
                raise ExpectedGoogleException(
                    'Invalid captcha')

        self.session.headers['Referer'] = sess.url

        if "selectchallenge/" in sess.url:
            sess = self.handle_selectchallenge(sess)

        # Was there an MFA challenge?
        if "challenge/totp/" in sess.url:
            error_msg = ""
            while error_msg is not None:
                sess = self.handle_totp(sess)
                error_msg = self.parse_error_message(sess)
                if error_msg is not None:
                    print(error_msg)
        elif "challenge/ipp/" in sess.url:
            sess = self.handle_sms(sess)
        elif "challenge/az/" in sess.url:
            sess = self.handle_prompt(sess)
        elif "challenge/sk/" in sess.url:
            sess = self.handle_sk(sess)
        elif "challenge/iap/" in sess.url:
            sess = self.handle_iap(sess)
        elif "challenge/ootp/5" in sess.url:
            raise NotImplementedError(
                'Offline Google App OOTP not implemented')

        # ... there are different URLs for backup codes (printed)
        # and security keys (eg yubikey) as well
        # save for later
        self.session_state = sess

    @staticmethod
    def check_extra_step(response):
        extra_step = response.find(text='This extra step shows that it’s really you trying to sign in')
        if extra_step:
            if response.find(id='contactAdminMessage'):
                raise ValueError(response.find(id='contactAdminMessage').text)

    def handle_captcha(self, sess, payload):
        response_page = BeautifulSoup(sess.text, 'html.parser')

        # Collect ProfileInformation, SessionState, signIn, and Password Challenge URL
        profile_information = response_page.find('input', {
            'name': 'ProfileInformation'
        }).get('value')
        session_state = response_page.find('input', {
            'name': 'SessionState'
        }).get('value')
        sign_in = response_page.find('input', {'name': 'signIn'}).get('value')
        passwd_challenge_url = response_page.find('form', {
            'id': 'gaia_loginform'
        }).get('action')

        # Update the payload
        payload['SessionState'] = session_state
        payload['ProfileInformation'] = profile_information
        payload['signIn'] = sign_in
        payload['Passwd'] = self.config.password

        # Get all captcha challenge tokens and urls
        captcha_container = response_page.find('div', {'class': 'captcha-container'})
        captcha_logintoken = captcha_container.find('input', {'name': 'logintoken'}).get('value')
        captcha_url = captcha_container.find('input', {'name': 'url'}).get('value')
        captcha_logintoken_audio = captcha_container.find('input', {'name': 'logintoken_audio'}).get('value')
        captcha_url_audio = captcha_container.find('input', {'name': 'url_audio'}).get('value')

        open_image = True

        # Check if there is a display utility installed as Image.open(f).show() do not raise any exception if not
        # if neither xv or display are available just display the URL for the user to visit.
        if os.name == 'posix' and sys.platform != 'darwin':
            if find_executable('xv') is None and find_executable('display') is None:
                open_image = False

        print("Please visit the following URL to view your CAPTCHA: {}".format(captcha_url))

        if open_image:
            try:
                with requests.get(captcha_url) as url:
                    with io.BytesIO(url.content) as f:
                        Image.open(f).show()
            except Exception:
                pass

        captcha_input = input("Captcha (case insensitive): ") or None

        # Update the payload
        payload['logincaptcha'] = captcha_input
        payload['logintoken'] = captcha_logintoken
        payload['url'] = captcha_url
        payload['logintoken_audio'] = captcha_logintoken_audio
        payload['url_audio'] = captcha_url_audio

        return self.post(passwd_challenge_url, data=payload)

    def handle_sk(self, sess):
        response_page = BeautifulSoup(sess.text, 'html.parser')
        challenge_url = sess.url.split("?")[0]

        challenges_txt = response_page.find('input', {
            'name': "id-challenge"
        }).get('value')
        challenges = json.loads(challenges_txt)

        facet_url = urllib_parse.urlparse(challenge_url)
        facet = facet_url.scheme + "://" + facet_url.netloc
        app_id = challenges["appId"]
        u2f_challenges = []
        for c in challenges["challenges"]:
            c["appId"] = app_id
            u2f_challenges.append(c)

        # Prompt the user up to attempts_remaining times to insert their U2F device.
        attempts_remaining = 5
        auth_response = None
        while True:
            try:
                auth_response = json.dumps(u2f_auth(u2f_challenges, facet))
                break
            except RuntimeWarning:
                print("No U2F device found. {} attempts remaining.".format(
                    attempts_remaining))
                if attempts_remaining <= 0:
                    break
                else:
                    input(
                        "Insert your U2F device and press enter to try again..."
                    )
                    attempts_remaining -= 1

        # If we exceed the number of attempts, raise an error and let the program exit.
        if auth_response is None:
            raise ExpectedGoogleException(
                "No U2F device found. Please check your setup.")

        payload = {
            'challengeId':
            response_page.find('input', {
                'name': 'challengeId'
            }).get('value'),
            'challengeType':
            response_page.find('input', {
                'name': 'challengeType'
            }).get('value'),
            'continue':
            response_page.find('input', {
                'name': 'continue'
            }).get('value'),
            'scc':
            response_page.find('input', {
                'name': 'scc'
            }).get('value'),
            'sarp':
            response_page.find('input', {
                'name': 'sarp'
            }).get('value'),
            'checkedDomains':
            response_page.find('input', {
                'name': 'checkedDomains'
            }).get('value'),
            'pstMsg':
            response_page.find('input', {
                'name': 'pstMsg'
            }).get('value'),
            'TL':
            response_page.find('input', {
                'name': 'TL'
            }).get('value'),
            'gxf':
            response_page.find('input', {
                'name': 'gxf'
            }).get('value'),
            'id-challenge':
            challenges_txt,
            'id-assertion':
            auth_response,
            'TrustDevice':
            'on',
        }
        return self.post(challenge_url, data=payload)

    def handle_sms(self, sess):
        response_page = BeautifulSoup(sess.text, 'html.parser')
        challenge_url = sess.url.split("?")[0]

        sms_token = input("Enter SMS token: G-") or None

        payload = {
            'challengeId':
            response_page.find('input', {
                'name': 'challengeId'
            }).get('value'),
            'challengeType':
            response_page.find('input', {
                'name': 'challengeType'
            }).get('value'),
            'continue':
            response_page.find('input', {
                'name': 'continue'
            }).get('value'),
            'scc':
            response_page.find('input', {
                'name': 'scc'
            }).get('value'),
            'sarp':
            response_page.find('input', {
                'name': 'sarp'
            }).get('value'),
            'checkedDomains':
            response_page.find('input', {
                'name': 'checkedDomains'
            }).get('value'),
            'pstMsg':
            response_page.find('input', {
                'name': 'pstMsg'
            }).get('value'),
            'TL':
            response_page.find('input', {
                'name': 'TL'
            }).get('value'),
            'gxf':
            response_page.find('input', {
                'name': 'gxf'
            }).get('value'),
            'Pin':
            sms_token,
            'TrustDevice':
            'on',
        }

        # Submit IPP (SMS code)
        return self.post(challenge_url, data=payload)

    def handle_prompt(self, sess):
        response_page = BeautifulSoup(sess.text, 'html.parser')
        challenge_url = sess.url.split("?")[0]

        data_key = response_page.find('div', {
            'data-api-key': True
        }).get('data-api-key')
        data_tx_id = response_page.find('div', {
            'data-tx-id': True
        }).get('data-tx-id')

        # Need to post this to the verification/pause endpoint
        await_url = "https://content.googleapis.com/cryptauth/v1/authzen/awaittx?alt=json&key={}".format(
            data_key)
        await_body = {'txId': data_tx_id}

        self.check_prompt_code(response_page)

        print("Open the Google App, and tap 'Yes' on the prompt to sign in ...")

        self.session.headers['Referer'] = sess.url

        retry = True
        response = None
        while retry:
            try:
                response = self.post(await_url, json_data=await_body)
                retry = False
            except requests.exceptions.HTTPError as ex:

                if not ex.response.status_code == 500:
                    raise ex

        parsed_response = json.loads(response.text)

        payload = {
            'challengeId':
            response_page.find('input', {
                'name': 'challengeId'
            }).get('value'),
            'challengeType':
            response_page.find('input', {
                'name': 'challengeType'
            }).get('value'),
            'continue':
            response_page.find('input', {
                'name': 'continue'
            }).get('value'),
            'scc':
            response_page.find('input', {
                'name': 'scc'
            }).get('value'),
            'sarp':
            response_page.find('input', {
                'name': 'sarp'
            }).get('value'),
            'checkedDomains':
            response_page.find('input', {
                'name': 'checkedDomains'
            }).get('value'),
            'checkConnection':
            'youtube:1295:1',
            'pstMsg':
            response_page.find('input', {
                'name': 'pstMsg'
            }).get('value'),
            'TL':
            response_page.find('input', {
                'name': 'TL'
            }).get('value'),
            'gxf':
            response_page.find('input', {
                'name': 'gxf'
            }).get('value'),
            'token':
            parsed_response['txToken'],
            'action':
            response_page.find('input', {
                'name': 'action'
            }).get('value'),
            'TrustDevice':
            'on',
        }

        return self.post(challenge_url, data=payload)

    @staticmethod
    def check_prompt_code(response):
        """
        Sometimes there is an additional numerical code on the response page that needs to be selected
        on the prompt from a list of multiple choice. Print it if it's there.
        """
        num_code = response.find("div", {"jsname": "EKvSSd"})
        if num_code:
            print("numerical code for prompt: {}".format(num_code.string))

    def handle_totp(self, sess):
        response_page = BeautifulSoup(sess.text, 'html.parser')
        tl = response_page.find('input', {'name': 'TL'}).get('value')
        gxf = response_page.find('input', {'name': 'gxf'}).get('value')
        challenge_url = sess.url.split("?")[0]
        challenge_id = challenge_url.split("totp/")[1]

        mfa_token = input("MFA token: ") or None

        if not mfa_token:
            raise ValueError(
                "MFA token required for {} but none supplied.".format(
                    self.config.username))

        payload = {
            'challengeId': challenge_id,
            'challengeType': 6,
            'continue': self.cont,
            'scc': 1,
            'sarp': 1,
            'checkedDomains': 'youtube',
            'pstMsg': 0,
            'TL': tl,
            'gxf': gxf,
            'Pin': mfa_token,
            'TrustDevice': 'on',
        }

        # Submit TOTP
        return self.post(challenge_url, data=payload)

    def handle_iap(self, sess):
        response_page = BeautifulSoup(sess.text, 'html.parser')
        challenge_url = sess.url.split("?")[0]
        phone_number = input('Enter your phone number:') or None

        while True:
            try:
                choice = int(
                    input(
                        'Type 1 to receive a code by SMS or 2 for a voice call:'
                    ))
                if choice not in [1, 2]:
                    raise ValueError
            except ValueError:
                print("Not a valid (integer) option, try again")
                continue
            else:
                if choice == 1:
                    send_method = 'SMS'
                elif choice == 2:
                    send_method = 'VOICE'
                else:
                    continue
                break

        payload = {
            'challengeId':
            response_page.find('input', {
                'name': 'challengeId'
            }).get('value'),
            'challengeType':
            response_page.find('input', {
                'name': 'challengeType'
            }).get('value'),
            'continue':
            self.cont,
            'scc':
            response_page.find('input', {
                'name': 'scc'
            }).get('value'),
            'sarp':
            response_page.find('input', {
                'name': 'sarp'
            }).get('value'),
            'checkedDomains':
            response_page.find('input', {
                'name': 'checkedDomains'
            }).get('value'),
            'pstMsg':
            response_page.find('input', {
                'name': 'pstMsg'
            }).get('value'),
            'TL':
            response_page.find('input', {
                'name': 'TL'
            }).get('value'),
            'gxf':
            response_page.find('input', {
                'name': 'gxf'
            }).get('value'),
            'phoneNumber':
            phone_number,
            'sendMethod':
            send_method,
        }

        # Submit phone number and desired method (SMS or voice call)
        sess = self.post(challenge_url, data=payload)

        response_page = BeautifulSoup(sess.text, 'html.parser')
        challenge_url = sess.url.split("?")[0]

        token = input("Enter " + send_method + " token: G-") or None

        payload = {
            'challengeId':
            response_page.find('input', {
                'name': 'challengeId'
            }).get('value'),
            'challengeType':
            response_page.find('input', {
                'name': 'challengeType'
            }).get('value'),
            'continue':
            response_page.find('input', {
                'name': 'continue'
            }).get('value'),
            'scc':
            response_page.find('input', {
                'name': 'scc'
            }).get('value'),
            'sarp':
            response_page.find('input', {
                'name': 'sarp'
            }).get('value'),
            'checkedDomains':
            response_page.find('input', {
                'name': 'checkedDomains'
            }).get('value'),
            'pstMsg':
            response_page.find('input', {
                'name': 'pstMsg'
            }).get('value'),
            'TL':
            response_page.find('input', {
                'name': 'TL'
            }).get('value'),
            'gxf':
            response_page.find('input', {
                'name': 'gxf'
            }).get('value'),
            'pin':
            token,
        }

        # Submit SMS/VOICE token
        return self.post(challenge_url, data=payload)

    def handle_selectchallenge(self, sess):
        response_page = BeautifulSoup(sess.text, 'html.parser')
        # Known mfa methods, 5 is disabled till its implemented
        auth_methods = {
            2: 'TOTP (Google Authenticator)',
            3: 'SMS',
            4: 'OOTP (Google Prompt)'
            # 5: 'OOTP (Google App Offline Security Code)'
        }

        unavailable_challenge_ids = [
            int(i.attrs.get('data-unavailable'))
            for i in response_page.find_all(
                lambda tag: tag.name == 'form' and 'data-unavailable' in tag.attrs
            )
        ]

        # ootp via google app offline code isn't implemented. make sure its not valid.
        unavailable_challenge_ids.append(5)

        challenge_ids = [
            int(i.get('value'))
            for i in response_page.find_all('input', {'name': 'challengeId'})
            if int(i.get('value')) not in unavailable_challenge_ids
        ]

        challenge_ids.sort()

        auth_methods = {
            k: auth_methods[k]
            for k in challenge_ids
            if k in auth_methods and k not in unavailable_challenge_ids
        }

        print('Choose MFA method from available:')
        print('\n'.join(
            '{}: {}'.format(*i) for i in list(auth_methods.items())))

        selected_challenge = input("Enter MFA choice number ({}): ".format(
            challenge_ids[-1:][0])) or None

        if selected_challenge is not None and int(selected_challenge) in challenge_ids:
            challenge_id = int(selected_challenge)
        else:
            # use the highest index as that will default to prompt, then sms, then totp, etc.
            challenge_id = challenge_ids[-1:][0]

        print("MFA Type Chosen: {}".format(auth_methods[challenge_id]))

        # We need the specific form of the challenge chosen
        challenge_form = response_page.find(
            'form', {'data-challengeentry': challenge_id})

        payload = {
            'challengeId':
            challenge_id,
            'challengeType':
            challenge_form.find('input', {
                'name': 'challengeType'
            }).get('value'),
            'continue':
            challenge_form.find('input', {
                'name': 'continue'
            }).get('value'),
            'scc':
            challenge_form.find('input', {
                'name': 'scc'
            }).get('value'),
            'sarp':
            challenge_form.find('input', {
                'name': 'sarp'
            }).get('value'),
            'checkedDomains':
            challenge_form.find('input', {
                'name': 'checkedDomains'
            }).get('value'),
            'pstMsg':
            challenge_form.find('input', {
                'name': 'pstMsg'
            }).get('value'),
            'TL':
            challenge_form.find('input', {
                'name': 'TL'
            }).get('value'),
            'gxf':
            challenge_form.find('input', {
                'name': 'gxf'
            }).get('value'),
            'subAction':
            challenge_form.find('input', {
                'name': 'subAction'
            }).get('value'),
        }
        if challenge_form.find('input', {'name': 'SendMethod'}) is not None:
            payload['SendMethod'] = challenge_form.find(
                'input', {
                    'name': 'SendMethod'
                }).get('value')

        # POST to google with the chosen challenge
        return self.post(
            self.base_url + challenge_form.get('action'), data=payload)


"""
The facet/appID used by Google auth does not seem to be valid
Need to apply some patches to u2flib_host to not validate the
content type when fetching the appId and don't validate the
returned facets (appID & facet list is hosted at
https://www.gstatic.com/securitykey/origins.json which is not
valid for the facet https://accounts.google.com)
"""


def __appid_verifier__fetch_json(app_id):
    target = app_id
    while True:
        resp = requests.get(target, allow_redirects=False, verify=True)

        # If the server returns an HTTP redirect (status code 3xx) the
        # server must also send the header "FIDO-AppID-Redirect-Authorized:
        # true" and the client must verify the presence of such a header
        # before following the redirect. This protects against abuse of
        # open redirectors within the target domain by unauthorized
        # parties.
        if 300 <= resp.status_code < 400:
            if resp.headers.get('FIDO-AppID-Redirect-Authorized') != \
                    'true':
                raise ValueError('Redirect must set '
                                 'FIDO-AppID-Redirect-Authorized: true')
            target = resp.headers['location']
        else:
            return resp.json()


def __appid_verifier__valid_facets(app_id, facets):
    return facets


def u2f_auth(challenges, facet):
    devices = u2f.list_devices()
    for device in devices[:]:
        try:
            device.open()
        except:
            devices.remove(device)

    try:
        prompted = False
        while devices:
            removed = []
            for device in devices:
                remove = True
                for challenge in challenges:
                    try:
                        return u2f.authenticate(device, json.dumps(challenge),
                                                facet)
                    except exc.APDUError as e:
                        if e.code == APDU_USE_NOT_SATISFIED:
                            remove = False
                            if not prompted:
                                print('Touch the flashing U2F device to '
                                      'authenticate...')
                                prompted = True
                        else:
                            pass
                    except exc.DeviceError:
                        pass
                if remove:
                    removed.append(device)
            devices = [d for d in devices if d not in removed]
            for d in removed:
                d.close()
            time.sleep(0.25)
    finally:
        for device in devices:
            device.close()
    raise RuntimeWarning("U2F Device Not Found")


appid.verifier.fetch_json = __appid_verifier__fetch_json
appid.verifier.valid_facets = __appid_verifier__valid_facets

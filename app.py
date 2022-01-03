import streamlit as st

from collections import defaultdict

from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

API_KEY = 'Ve7-0om6kuW6tZnahDgcKW927DS5FTbs8tchE141oRwr'
API_URL = 'https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/1c5e98d3-0fc4-4a07-a439-e59429dcf6c2'


def translate(text, source, target):
    model_id = languages_to_code[source] + '-' + languages_to_code[target]
    result = language_translator.translate(text=text, model_id=model_id).get_result()["translations"][0]["translation"]
    return result

authenticator = IAMAuthenticator(API_KEY)
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

language_translator.set_service_url(API_URL)

languages_to_code = {}
code_to_languages = {}
for o in language_translator.list_languages().get_result()['languages']:
    code_to_languages[o['language']] = o['language_name']
    languages_to_code[o['language_name']] = o['language']

language_models = []
language_to_language = defaultdict(lambda : [])
for model in language_translator.list_models().get_result()['models']:
    language_models.append(model['model_id'])
    language_to_language[code_to_languages[model['source']]].append(code_to_languages[model['target']])
language_to_language = dict(language_to_language)

source = st.selectbox('Source Language', list(language_to_language.keys()))
target = st.selectbox('Target Language', language_to_language[source])
text = st.text_area('Enter Text')

ok = st.button('Translate')

if text and ok:
    result = translate(text, source, target)
    st.write(result)
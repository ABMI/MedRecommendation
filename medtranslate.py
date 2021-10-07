from google.cloud import translate_v3
import os
import pandas as pd
import numpy as np
import csv
from oauth2client.service_account import ServiceAccountCredentials
from pyasn1.debug import Scope,scope
import json
from collections import OrderedDict

os.chdir('D:/test/')
project_id = "acquired-rite-317207" ## GCP project id 
glossary_id = "med_test" ## name you want to give this glossary resource
location = 'us-central1'
gcs_glossary_uri = 'gs://example2_test/test_glossary.csv'

# 워크로드 아이덴티티 제휴로 키사용하지않고 리소스에 액세스 가능 (보안 강화필요 시 확인할 것)
file_data = OrderedDict()
file_data["type"] = "service_account"
file_data["project_id"] = "acquired-rite-317207"
file_data["private_key_id"] = "726ff656b30aaab24ce010f2b6d3de91cd38fbfb"
file_data["private_key"] = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDZny+oBBbbZZGg\neyqj7UK309Px0aLkSF5TPI7WeClVSYPH/eRKYIQDHSxkDW6j1v0gY2uxbCsVoYf9\npXMhFZKKwCJVke01rlv2E8cobn6iY1APbQjOkz+pgXKCOLnEfcdX2UaDHWXgHbku\nxJbxhmH0PcbTg5kWOdXZbUH3Et3vaLhURRQp/jLeQKW4MzVhcW9eWpSAgx8gJPHp\nJHhWvBSmpkVrJy9RMXmXOrsCa3VoY6OXuv3jJDyizqoKa6FGqaIHXFjECfWg9Vsz\nnWnai9ql/0OUhuJGgZWejXhuk+cy++LXG4F/OQvDCyorCR8ncuzH6mhM8O3peK/U\nkj/ttK8VAgMBAAECggEAByGZ3UVfCLWmxJhspgkIbT+I2+KCVj053BE+tAVQLhjg\niOKcwxmFEe4NjkIeF0qG/8ifluWOxuDEyk7MO5q6SIeHHdXll6NST6QdHAnSPAOJ\nntZ0RK1bbMmkD+OIe4l3SWgXu68Fr4cB0mgY8yqzwIjFYG6DoHsTiH0K/Zagb6/S\naklX219UrAJZMFCaw6N4ZRiUqKCIvKfCGzoLwQ7zVDqwNkh2QT+VFVgKhD0r3PKn\ndAMq4GAmBliJQfeExQeFsZ6EJ0XaLRoaLHSIpPGapgcXjvFABmdzLOhpb168o3il\nxg6RyG2j3ZxmIVdY0HJ7I7Fhk//Kx0ExuGWpEE0/KQKBgQDzz53FmVcOcJ96zr20\n2q9inklx8+OpKIE5fWxOOzYUePhzLaoUr8hxsCLJGEh8QsgR+eTiI3tTnR1d1iSA\n0X2kVRbd9OybJ2af2hUYp+GPMclUNsfXWVVYYNIKqx99zQOsedC0/x46r1Flrimg\no1rz3taAoTrIeCyynIDdRNnoWQKBgQDkgGQZPs6dAxGkgAxD+MIlKMU9yE+hX+nh\nXnrEUyrNqg5dCViacQhvsDSKbBsdDYGxixZNjQPdWdLDABVUviElixFsunjMeAjI\nkxLAI7mmrcRxWpIJhv0GahhoE+B9HyDhnbDbOOtjY71LhuYXa1p81BNYnuH9dsiR\n6jFB1+SlHQKBgQCLvfTk++Ws7hpKblLHZQxfTvAzsyFKpF+kzuGT2VY+17M3ePXi\nE3qkxtq5PgTVzAUWYI+ymbmnDAd38DRN7UTBOs/3edlfeG7Wsk2jKx4aT+PgM+HI\n6XgERsI8wSY0mZxAcDWSeCMgaboSuIc9fkO0QYXahg7GNjMQUKl/qWXoSQKBgDn4\nxOyOvbaiF7DHd9Uq4H6y+E+zaViEz/6IjNcQTpS9J0W9YEhWkxBbAQl5YeueCKB1\nrCPiue9Hoawtcjv8vMYcoUAXkxw0++1/OsuahLhf763ej5xxLfKZqjWFjXfRFPOI\noV0M9NNTc6wcvnWEnAF9gKcEMEuw/jPe2b5durmVAoGAWUdgWDKrb8GzKsgiUe4b\nerafMIPd3Io6I9ceM3R9D37tgQhHqaqw/YPyPObvqhVncC7Wcf9ty5FsKNsuPja7\n2bWLeIPFdMqkx0vqshZoDGUogKGdbC3wUPOlFP+3ag6UlHJNETxwCCleCJ9taIj9\nQkmCvilgkOFflYGT/jyGX2E=\n-----END PRIVATE KEY-----\n"
file_data["client_email"] = "host-629@acquired-rite-317207.iam.gserviceaccount.com"
file_data["client_id"] = "100098296159535260880"
file_data["auth_uri"] = "https://accounts.google.com/o/oauth2/auth"
file_data["token_uri"] = "https://oauth2.googleapis.com/token"
file_data["auth_provider_x509_cert_url"] = "https://www.googleapis.com/oauth2/v1/certs"
file_data["client_x509_cert_url"] = "https://www.googleapis.com/robot/v1/metadata/x509/host-629%40acquired-rite-317207.iam.gserviceaccount.com"
 
with open('acquired-rite-317207-726ff656b30a.json', 'w', encoding="utf-8") as make_file:
    json.dump(file_data, make_file, ensure_ascii=False, indent='\t')

credential_file = "D:/test/acquired-rite-317207-726ff656b30a.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credential_file

def create_glossary(
    project_id="YOUR_PROJECT_ID",
    input_uri="YOUR_INPUT_URI",
    glossary_id="YOUR_GLOSSARY_ID",
    timeout=180,
):
    """
    Create a equivalent term sets glossary. Glossary can be words or
    short phrases (usually fewer than five words).
    https://cloud.google.com/translate/docs/advanced/glossary#format-glossary
    """
    client = translate_v3.TranslationServiceClient()

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    source_lang_code = "ko"
    target_lang_code = "en"
    location = "us-central1"  # The location of the glossary

    name = client.glossary_path(project_id, location, glossary_id)
    language_codes_set = translate_v3.types.Glossary.LanguageCodesSet(
        language_codes=[source_lang_code, target_lang_code]
    )

    gcs_source = translate_v3.types.GcsSource(input_uri=input_uri)

    input_config = translate_v3.types.GlossaryInputConfig(gcs_source=gcs_source)

    glossary = translate_v3.types.Glossary(
        name=name, language_codes_set=language_codes_set, input_config=input_config
    )

    parent = f"projects/{project_id}/locations/{location}"
    # glossary is a custom dictionary Translation API uses
    # to translate the domain-specific terminology.
    operation = client.create_glossary(parent=parent, glossary=glossary)

    result = operation.result(timeout)
    print("Created: {}".format(result.name))
    print("Input Uri: {}".format(result.input_config.gcs_source.input_uri))

def get_glossary(project_id=project_id, glossary_id=glossary_id):
    """Get a particular glossary based on the glossary ID."""

    client = translate_v3.TranslationServiceClient()

    name = client.glossary_path(project_id, "us-central1", glossary_id)

    response = client.get_glossary(name=name)
    # print(u"Input URI: {}".format(response.input_config.gcs_source.input_uri))

def list_glossaries(project_id="YOUR_PROJECT_ID"):
    """List Glossaries."""

    client = translate_v3.TranslationServiceClient()

    location = "us-central1"

    parent = f"projects/{project_id}/locations/{location}"

    # Iterate over all results
    for glossary in client.list_glossaries(parent=parent):
        print("Name: {}".format(glossary.name))
        print("Entry count: {}".format(glossary.entry_count))
        print("Input uri: {}".format(glossary.input_config.gcs_source.input_uri))

        # Note: You can create a glossary using one of two modes:
        # language_code_set or language_pair. When listing the information for
        # a glossary, you can only get information for the mode you used
        # when creating the glossary.
        for language_code in glossary.language_codes_set.language_codes:
            print("Language code: {}".format(language_code))


def delete_glossary(
    project_id="YOUR_PROJECT_ID",
    glossary_id="YOUR_GLOSSARY_ID",
    timeout=180,
):
    """Delete a specific glossary based on the glossary ID."""
    client = translate_v3.TranslationServiceClient()

    name = client.glossary_path(project_id, "us-central1", glossary_id)

    operation = client.delete_glossary(name=name)
    result = operation.result(timeout)
    print("Deleted: {}".format(result.name))


def translate_word_with_glossary(
    text,
    project_id,
    glossary_id
):
    get_glossary(project_id=project_id, glossary_id=glossary_id)
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path(project_id, location)

    glossary = client.glossary_path(
        project_id, location, glossary_id  # The location of the glossary
    )

    glossary_config = translate_v3.types.TranslateTextGlossaryConfig(
        glossary=glossary)

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    response = client.translate_text(
        contents=[text],
        source_language_code="ko",
        target_language_code="en",
        parent=parent,
        glossary_config=glossary_config,
    )
    
    translated_output = response.glossary_translations[0].translated_text
    return translated_output

# list_glossaries(project_id=project_id)
# # create_glossary(project_id=project_id,input_uri=gcs_glossary_uri,glossary_id=glossary_id)
# print(translate_word_with_glossary('실험1',project_id,glossary_id))


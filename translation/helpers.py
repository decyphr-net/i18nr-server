from deepdiff import DeepDiff
import requests

URL = "https://decyphr.uc.r.appspot.com/api/v1/text-to-text/"


def convert(s, j):
    s = s.replace("root", "")
    s = s.replace("[", "")
    s = s.replace("'", "")
    keys = s.split("]")[:-1]
    d = {}
    for k in reversed(keys):
        if not d:
            d[k] = None
        else:
            d = {k: d}
    v = None
    v_ref = d
    for i, k in enumerate(keys, 1):
        if not v:
            v = j.get(k)
        else:
            v = v.get(k)
        if i < len(keys):
            v_ref = v_ref.get(k)
    v_ref[k] = v
    return d


def get_new_items_as_dict(translation, source):
    diff = DeepDiff(translation, source, ignore_order=False)
    added = diff["dictionary_item_added"]

    added_dict = {}
    for added_str in added:
        added_dict.update(convert(added_str, translation))

    return added_dict


def map_to_source_dict(new_dict, source):
    new_structure = {}
    for key in new_dict:
        new_structure.update({key: source[key]})

    return new_structure


def add_to_translation_dict(new_structure, translations, lang_code):
    for item in new_structure:
        if not isinstance(new_structure[item], dict):
            data = {"target_language_code": lang_code, "text": new_structure[item]}
            response = requests.post(URL, data)
            translations.update({item: response.json()["translated_text"]})
        else:
            translations.update({item: new_structure[item]})
            add_to_translation_dict(new_structure[item], translations[item], lang_code)
    return translations

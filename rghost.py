#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Upload a file to RGhost (http://rghost.net) from the command-line.

    $ rghost.py --tags="picture nature" \
                     --description="Lucy in the sky with diamonds" \
                     --removal_code="remove_later" \
                     --password="secret" \
                     --lifespan=1 \
                     --public="0" \
                     test.txt
    http://rghost.ru/private/47783143/2d2573410be063a1f588e63cfe9b4a6a
"""


import mechanize
import re
import traceback


def create_browser():
    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders = [('User-agent', 'Firefox')]
    return br

def is_edit_form(form, uploaded_url):
    action = form.attrs.get('action')
    if not action:
        return False
    return uploaded_url.endswith(action)

def upload(filename, upload_filename=None, upload_params=None):
    ''' Upload file `filename` to rghost.
    upload_filename is how it will be named after upload
    upload_params is a dictionary of items as tags, description, etc '''
    upload_filename = upload_filename or filename
    browser = create_browser()
    browser.open("http://rghost.ru/")
    browser.select_form(predicate=lambda form:form.attrs.get('id')=='upload_form')
    with open(filename, 'rb') as f:
        browser.form.add_file(f, 'text/plain', upload_filename)
        browser.submit()
    uploaded_url = browser.geturl()
    not_hidden_lambda = lambda elem:elem.type != 'hidden'
    if upload_params:
        browser.select_form(predicate=lambda form, uploaded_url=uploaded_url:is_edit_form(form, uploaded_url))
        for name, value in upload_params.iteritems():
            control_name = 'fileset[%s]'%name
            try:
                control = browser.form.find_control(name=control_name)
            except mechanize.AmbiguityError:
                control = browser.form.find_control(name=control_name, predicate=not_hidden_lambda, nr=0)
            if isinstance(control, mechanize.CheckboxControl):
                control.items[0].selected = value
            else:
                control.value = value
        browser.submit()
    return browser.geturl()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    upload_params_list = frozenset(['tags', 'description', 'removal_code', 'password', 'lifespan', 'public'])
    parser.add_argument('--tags', help='file tags, 10 at most, separate with commas.')
    parser.add_argument('--description', help='file description.')
    parser.add_argument('--removal_code', help='password to delete file.')
    parser.add_argument('--password', help='password to download file.')
    parser.add_argument('--lifespan', help='storage life in days since last download.',
                        type=str, choices=map(str, [1, 5, 14, 30]), action='append')
    parser.add_argument('--public', help='if not public, only those, who have the link, can download it.',
                        type=lambda val:bool(int(val)), choices=[0, 1])
    parser.add_argument('--upload_filename', help="how file will be named after upload.")
    parser.add_argument('filename', nargs='+', help='file to upload.')
    
    namespace = parser.parse_args()
    upload_params = {name:value for name,value in namespace._get_kwargs() if value is not None
                                                                   and name in upload_params_list}
    for filename in namespace.filename:
        print upload(filename, upload_params=upload_params)
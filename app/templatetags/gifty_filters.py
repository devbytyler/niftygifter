from django import template

register = template.Library()

def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')

def upto(value, delimiter=None):
    return value.split(delimiter)[0]

url_target_blank = register.filter(url_target_blank, is_safe = True)
upto = register.filter(upto, is_safe = True)
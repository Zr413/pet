from django import template
import random

register = template.Library()


@register.filter()
def censor(value):
    chars = ["*", "#", "%", "&", "?", "@", "*", "#", "%", "&", "?", "@"]
    base_mat = ["хакер", "борода"]
    value = value.lower().split(' ')
    for word in value:
        if word in base_mat:
            temp = random.sample(chars, len(word))
            i = ''.join(temp)
            value = [x.replace(word, i) for x in value]
    value = ' '.join(value)

    return f'{value}'

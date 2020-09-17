from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_item_v_first(dictionary, key):
    dst_list = dictionary.get(key)
    if dst_list and len(dst_list) != 0:
        return dst_list[0]
    else:
        return None

@register.filter
def pop_item(dictionary, key):
    return dictionary.pop(key)

class SetVarNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""

def set_var(parser, token):
    """
        {% set <var_name> = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")
    return SetVarNode(parts[1], parts[3])

register.tag('set', set_var)


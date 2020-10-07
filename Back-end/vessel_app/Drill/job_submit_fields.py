class JobSubmitForm:

    def __init__(self, model_name):
        self.model_name = model_name
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

    def get_form_html(self):
        return '\n'.join([field.get_html() for field in self.fields])

    def get_fields(self):
        return [field.input_name for field in self.fields]


class NumberField:
    def __init__(self, label, input_name, min="", max="", placeholder="", value=""):

        self.label = label
        self.input_name = input_name
        self.min = min
        self.max = max
        self.placeholder = placeholder
        self.value = value
    
    def get_html(self):
        return f'''
        <label for="{self.input_name}" class='form-text-h3 colors-on-surface'>{self.label}</label>\n
        <input class="form-control" style="width: 10%; margin-bottom: 2%; margin: auto;" type="number" name="{self.input_name}" min="{self.min}" max="{self.max}" placeholder="{self.placeholder}" value="{self.value}">
        '''

class DropdownField:
    def __init__(self, label, input_name, options):

        self.label = label
        self.input_name = input_name
        self.options = options # dict of value, label for dropdown
    
    def get_html(self):
        dropdown_options = ''''''
        for k, v in self.options.items():
            dropdown_options += f'<option value="{v}">{k}</option>\n'

        html =  f'''
        <label for="{self.input_name}" class='form-text-h3 colors-on-surface'>{self.label}</label>
        <select class="form-control" name="{self.input_name}" style="width: 35%; margin: auto;">
        {dropdown_options}
        </select>
        '''

        return html
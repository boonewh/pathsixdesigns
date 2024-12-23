import json
import os
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SelectField, 
                    DateField, EmailField, FloatField, TelField)
from wtforms.validators import DataRequired

def load_form_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)  # Move up to pathsix_crm
    config_path = os.path.join(parent_dir, 'config', 'form_fields.json')
    
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Print the paths to help debug
        print(f"Current directory: {current_dir}")
        print(f"Parent directory: {parent_dir}")
        print(f"Attempted config path: {config_path}")
        raise FileNotFoundError(f"Could not find form_fields.json at {config_path}")

def create_dynamic_form(model_type):
    form_config = load_form_config()
    
    if model_type not in form_config:
        raise ValueError(f"No configuration for {model_type}")

    class DynamicForm(FlaskForm):
        pass

    for field_name, field_config in form_config[model_type].items():
        field_type = field_config['type']
        validators = []
        if field_config['required']:
            validators.append(DataRequired())

        if field_type == 'select':
            validators = []
            setattr(
                DynamicForm,
                field_name,
                SelectField(
                    field_config['label'],
                    choices=[('', field_config.get('placeholder', ''))],
                    validators=validators
                )
            )
        elif field_type == 'date':
            setattr(DynamicForm, field_name, 
                   DateField(field_config['label'], 
                           validators=validators,
                           format='%Y-%m-%d',
                           render_kw={'type': 'date'}))
        elif field_type == 'number':
            setattr(DynamicForm, field_name,
                   FloatField(field_config['label'],
                            validators=validators))
        elif field_type == 'textarea':
            setattr(DynamicForm, field_name,
                   TextAreaField(field_config['label'],
                               validators=validators))
        else:  # default to StringField
            setattr(DynamicForm, field_name,
                   StringField(field_config['label'],
                             validators=validators))

    return DynamicForm()

# Make sure the function is exported
__all__ = ['create_dynamic_form']
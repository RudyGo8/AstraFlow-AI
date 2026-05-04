

import re
from pathlib import Path
from typing import Dict, List, Any

#  # (description)
BASE_DIR = Path(__file__).parent.parent.parent
MODELS_DIR = BASE_DIR / "models"

#  # (description)
FIELD_TYPE_MAPPING = {
    "CharField": {
        "import": "fields.CharField",
        "params": ["max_length", "null", "default", "description", "source_field"],
        "required": ["max_length"]
    },
    "TextField": {
        "import": "fields.TextField",
        "params": ["null", "default", "description", "source_field"],
        "required": []
    },
    "IntField": {
        "import": "fields.IntField",
        "params": ["null", "default", "description", "source_field"],
        "required": []
    },
    "SmallIntField": {
        "import": "fields.SmallIntField",
        "params": ["null", "default", "description", "source_field"],
        "required": []
    },
    "BigIntField": {
        "import": "fields.BigIntField",
        "params": ["null", "default", "description", "source_field"],
        "required": []
    },
    "FloatField": {
        "import": "fields.FloatField",
        "params": ["null", "default", "description", "source_field"],
        "required": []
    },
    "DecimalField": {
        "import": "fields.DecimalField",
        "params": ["max_digits", "decimal_places", "null", "default", "description", "source_field"],
        "required": ["max_digits", "decimal_places"]
    },
    "BooleanField": {
        "import": "fields.BooleanField",
        "params": ["null", "default", "description", "source_field"],
        "required": []
    },
    "DateField": {
        "import": "fields.DateField",
        "params": ["null", "default", "auto_now", "auto_now_add", "description", "source_field"],
        "required": []
    },
    "DatetimeField": {
        "import": "fields.DatetimeField",
        "params": ["null", "default", "auto_now", "auto_now_add", "description", "source_field"],
        "required": []
    },
    "TimeField": {
        "import": "fields.TimeField",
        "params": ["null", "default", "auto_now", "auto_now_add", "description", "source_field"],
        "required": []
    },
    "JSONField": {
        "import": "fields.JSONField",
        "params": ["null", "default", "description", "source_field"],
        "required": []
    },
    "UUIDField": {
        "import": "fields.UUIDField",
        "params": ["pk", "null", "default", "description", "source_field"],
        "required": []
    },
    "ForeignKeyField": {
        "import": "fields.ForeignKeyField",
        "params": ["model", "related_name", "null", "on_delete", "description", "source_field"],
        "required": ["model"]
    },
    "OneToOneField": {
        "import": "fields.OneToOneField",
        "params": ["model", "related_name", "null", "on_delete", "description", "source_field"],
        "required": ["model"]
    },
    "ManyToManyField": {
        "import": "fields.ManyToManyField",
        "params": ["model", "related_name", "through", "description"],
        "required": ["model"]
    }
}


def create_model(model_name: str, table_name: str, table_description: str, field_definitions: List[Dict]) -> str:
    """
      ?
    
    Args:
        model_name: 
        table_name: ?
        table_description:    ?
        field_definitions: 
        
    Returns:
        
    """
    try:
        #  # (description)
        if not model_name or not table_name:
            return "   "
        
        if not field_definitions:
            return ""
        
        #  # (description)
        model_code = generate_model_code(model_name, table_name, table_description, field_definitions)
        
        #  # (description)
        file_name = f"{table_name}.py"
        model_file = MODELS_DIR / file_name
        
        if model_file.exists():
            return f"Model file {file_name} already exists"
        
        #  # (description)
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        
        #  # (description)
        model_file.write_text(model_code, encoding="utf-8")
        
        #  # (description)
        update_models_init(model_name, file_name)
        
        return f"? {model_name} ? {file_name}"
        
    except Exception as e:
        return f": {str(e)}"


def generate_model_code(model_name: str, table_name: str, table_description: str, field_definitions: List[Dict]) -> str:
    """g"""
    
    #  # (description)
    code = f"""# _*_ coding : UTF-8 _*_
# @Time : {__import__('datetime').datetime.now().strftime('%Y/%m/%d %H:%M')}
# @Author : sonder
# @File : {table_name}.py
# @Comment : {table_description}

from models.sa_orm import fields
from models.common import BaseModel


class {model_name}(BaseModel):
    \"\"\"
    {table_description}
    \"\"\"

"""
    
    #  # (description)
    for field_def in field_definitions:
        field_code = generate_field_code(field_def["name"], field_def["type"], field_def)
        code += field_code + "\n"
    
    #  # (description)
    code += f"""
    class Meta:
        table = "{table_name}"
        table_description = "{table_description}"
        ordering = ["-created_at"]
"""
    
    return code


def generate_field_code(field_name: str, field_type: str, params: Dict[str, Any]) -> str:
    """g"""
    
    if field_type not in FIELD_TYPE_MAPPING:
        raise ValueError(f": {field_type}")
    
    field_info = FIELD_TYPE_MAPPING[field_type]
    
    #  # (description)
    param_parts = []
    
    for param_name in field_info["params"]:
        if param_name in params:
            value = params[param_name]
            
            #  # (description)
            if isinstance(value, str):
                if param_name == "model":
                    param_parts.append(f'{param_name}="{value}"')
                else:
                    param_parts.append(f'{param_name}="{value}"')
            elif isinstance(value, bool):
                param_parts.append(f'{param_name}={str(value)}')
            elif value is None:
                param_parts.append(f'{param_name}=None')
            else:
                param_parts.append(f'{param_name}={value}')
    
    #  # (description)
    if "source_field" not in params:
        param_parts.append(f'source_field="{field_name}"')
    
    param_str = ",\n        ".join(param_parts)
    
    #  # (description)
    field_code = f"""    {field_name} = fields.{field_type}(
        {param_str}
    )"""
    
    #  # (description)
    description = params.get("description", "")
    if description:
        field_code += f'''
    """
    {description}
    """'''
    
    return field_code


def update_models_init(model_name: str, file_name: str) -> None:
    """models/__init__.py"""
    
    init_file = MODELS_DIR / "__init__.py"
    
    if not init_file.exists():
        return
    
    content = init_file.read_text(encoding="utf-8")
    
    #  # (description)
    module_name = file_name.replace(".py", "")
    import_line = f"from models.{module_name} import {model_name}"
    
    #  # (description)
    import_match = re.search(r'(from models\.\w+ import [^\n]+\n)', content)
    if import_match:
        #  # (description)
        last_import_end = import_match.end()
        new_content = content[:last_import_end] + f"{import_line}\n" + content[last_import_end:]
    else:
        #  # (description)
        new_content = f"{import_line}\n" + content
    
    #  # (description)
    all_match = re.search(r'__all__ = \[(.*?)\]', new_content, re.DOTALL)
    if all_match:
        all_content = all_match.group(1)
        if f"'{model_name}'" not in all_content:
            #  # (description)
            new_all_content = all_content.rstrip() + f",\n    '{model_name}'"
            new_content = new_content.replace(all_match.group(1), new_all_content)
    
    init_file.write_text(new_content, encoding="utf-8")


def list_models():
    """
    
    
    Returns:
        
    """
    try:
        models = []
        
        if not MODELS_DIR.exists():
            return "Model directory does not exist"
        
        for file_path in MODELS_DIR.glob("*.py"):
            if file_path.name in ["__init__.py", "common.py"]:
                continue
            
            content = file_path.read_text(encoding="utf-8")
            
            #  # (description)
            class_matches = re.findall(r'class\s+(\w+)\(BaseModel\):', content)
            
            if class_matches:
                models.append({
                    "file": file_path.name,
                    "classes": class_matches
                })
        
        if not models:
            return "No models found"
        
        result = "  ?\n"
        for model in models:
            result += f"\n {model['file']}\n"
            for class_name in model['classes']:
                result += f"    {class_name}\n"
        
        return result
        
    except Exception as e:
        return f": {str(e)}"


def get_model_info(model_name: str) -> str:
    """
    ?
    
    Args:
        model_name: 
        
    Returns:
        
    """
    try:
        if not MODELS_DIR.exists():
            return "Model directory does not exist"
        
        for file_path in MODELS_DIR.glob("*.py"):
            if file_path.name in ["__init__.py", "common.py"]:
                continue
            
            content = file_path.read_text(encoding="utf-8")
            
            #  # (description)
            class_pattern = rf'class\s+{model_name}\(BaseModel\):(.*?)(?=class\s+\w+|$)'
            class_match = re.search(class_pattern, content, re.DOTALL)
            
            if class_match:
                class_content = class_match.group(1)
                
                #  # (description)
                field_matches = re.findall(r'(\w+)\s*=\s*fields\.(\w+)\((.*?)\)', class_content, re.DOTALL)
                
                result = f": {model_name}\n"
                result += f": {file_path.name}\n\n"
                result += ":\n"
                
                for field_name, field_type, field_params in field_matches:
                    result += f"  ?{field_name}: {field_type}\n"
                    if field_params.strip():
                        result += f"    : {field_params.strip()}\n"
                
                return result
        
        return f"  ? {model_name}"
        
    except Exception as e:
        return f": {str(e)}"


if __name__ == "__main__":
    #  # (description)
    print("   ")


def register(mcp):
    """Register model tools with MCP service"""
    
    @mcp.tool()
    def create_database_model(
        model_name: str,
        table_name: str,
        table_description: str,
        field_definitions: list
    ) -> str:
        """
        Create a database model

        Args:
            model_name: Model class name
            table_name: Database table name
            table_description: Table description
            field_definitions: Field definition list, each field contains name, type and other params

        Returns:
            Creation result info
        """
        return create_model(model_name, table_name, table_description, field_definitions)
    
    @mcp.tool()
    def list_database_models() -> str:
        """
        List all defined database models

        Returns:
            Model list info
        """
        return list_models()
    
    @mcp.tool()
    def get_database_model_info(model_name: str) -> str:
        """
        Get detailed info of a specified model

        Args:
            model_name: Model class name

        Returns:
            Model detail info
        """
        return get_model_info(model_name)



import re
from pathlib import Path
from typing import Dict, List, Any

#  # (description)
BASE_DIR = Path(__file__).parent.parent.parent
SCHEMAS_DIR = BASE_DIR / "schemas"
MODELS_DIR = BASE_DIR / "models"

# SQLAlchemy  # (description)
FIELD_TYPE_MAPPING = {
    "CharField": "str",
    "TextField": "str", 
    "IntField": "int",
    "SmallIntField": "int",
    "BigIntField": "int",
    "FloatField": "float",
    "DecimalField": "float",
    "BooleanField": "bool",
    "DateField": "str",  # ?
    "DatetimeField": "str",  # ?
    "TimeField": "str",  # ?
    "JSONField": "dict",
    "UUIDField": "str",
    "ForeignKeyField": "Optional[str]",  # D
    "OneToOneField": "Optional[str]",
    "ManyToManyField": "List[str]"  # D      
}


def analyze_model_file(model_file_path: Path) -> List[Dict[str, Any]]:
    """Analyze model file, extract model information"""
    if not model_file_path.exists():
        return []
    
    content = model_file_path.read_text(encoding="utf-8")
    models = []
    
    #  # (description)
    class_pattern = r'class\s+(\w+)\(BaseModel\):(.*?)(?=class\s+\w+|$)'
    class_matches = re.findall(class_pattern, content, re.DOTALL)
    
    for class_name, class_content in class_matches:
        # Extract class docstring - improved regex
        doc_match = re.search(r'"""(.*?)"""', class_content, re.DOTALL)
        if doc_match:
            # Clean docstring, remove extra whitespace and newlines
            description = doc_match.group(1).strip()
            # Take first line as short description
            description = description.split('\n')[0].strip()
            if not description:
                description = f"{class_name} model"
        else:
            description = f"{class_name} model"
        
        #  # (description)
        fields = []
        field_pattern = r'(\w+)\s*=\s*fields\.(\w+)\((.*?)\)'
        field_matches = re.findall(field_pattern, class_content, re.DOTALL)
        
        for field_name, field_type, field_params in field_matches:
            field_info = parse_field_params(field_name, field_type, field_params)
            fields.append(field_info)
        
        models.append({
            "name": class_name,
            "description": description,
            "fields": fields,
            "file": model_file_path.name
        })
    
    return models


def parse_field_params(field_name: str, field_type: str, params_str: str) -> Dict[str, Any]:
    """f"""
    field_info = {
        "name": field_name,
        "type": field_type,
        "pydantic_type": FIELD_TYPE_MAPPING.get(field_type, "str"),
        "required": True,
        "default": None,
        "description": "",
        "max_length": None,
        "null": False
    }
    
    #  # (description)
    if "null=True" in params_str:
        field_info["null"] = True
        field_info["required"] = False
    
    if "default=" in params_str:
        field_info["required"] = False
        #  # (description)
        default_match = re.search(r'default=([^,\n)]+)', params_str)
        if default_match:
            field_info["default"] = default_match.group(1).strip()
    
    #  # (description)
    desc_match = re.search(r'description="([^"]*)"', params_str)
    if desc_match:
        field_info["description"] = desc_match.group(1)
    
    #  # (description)
    max_length_match = re.search(r'max_length=(\d+)', params_str)
    if max_length_match:
        field_info["max_length"] = int(max_length_match.group(1))
    
    #  # (description)
    if field_type in ["ForeignKeyField", "OneToOneField"]:
        field_info["pydantic_type"] = "Optional[str]"
        field_info["required"] = False
    
    #  # (description)
    if field_info["null"] and field_info["pydantic_type"] != "Optional[str]":
        if not field_info["pydantic_type"].startswith("Optional"):
            field_info["pydantic_type"] = f"Optional[{field_info['pydantic_type']}]"
    
    return field_info


def generate_schema_code(model_info: Dict[str, Any], schema_types: List[str]) -> str:
    """schemag"""
    model_name = model_info["name"]
    description = model_info["description"]
    fields = model_info["fields"]
    
    #  # (description)
    simple_description = description.split('\n')[0].strip() if description else f"{model_name}"
    
    code = f"""# _*_ coding : UTF-8 _*_
# @Time : {__import__('datetime').datetime.now().strftime('%Y/%m/%d %H:%M')}
# @Author : sonder
# @File : {model_name.lower().replace('system', '')}.py
# @Comment : {simple_description}

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from schemas.common import BaseResponse, ListQueryResult, DataBaseModel

"""
    
    #  # (description)
    for schema_type in schema_types:
        if schema_type == "info":
            code += generate_info_schema(model_name, simple_description, fields)
        elif schema_type == "add":
            code += generate_add_schema(model_name, simple_description, fields)
        elif schema_type == "update":
            code += generate_update_schema(model_name, simple_description, fields)
        elif schema_type == "list":
            code += generate_list_schemas(model_name, simple_description)
        elif schema_type == "response":
            code += generate_response_schemas(model_name, simple_description)
    
    return code


def generate_info_schema(model_name: str, description: str, fields: List[Dict]) -> str:
    """schema"""
    class_name = f"{model_name.replace('System', '')}Info"
    
    code = f"""
class {class_name}(DataBaseModel):
    \"\"\"
    {description}
    \"\"\"
    model_config = ConfigDict()
"""
    
    for field in fields:
        field_name = field["name"]
        pydantic_type = field["pydantic_type"]
        description = field["description"]
        max_length = field["max_length"]
        default = field["default"]
        required = field["required"]
        
        #  # (description)
        field_params = []
        if not required:
            if default is not None:
                field_params.append(f"default={default}")
            else:
                field_params.append("default=None")
        else:
            field_params.append("...")
        
        if max_length:
            field_params.append(f"max_length={max_length}")
        
        if description:
            field_params.append(f'description="{description}"')
        
        field_def = f"Field({', '.join(field_params)})"
        
        code += f"    {field_name}: {pydantic_type} = {field_def}\n"
    
    code += "\n"
    return code


def generate_add_schema(model_name: str, description: str, fields: List[Dict]) -> str:
    """schema"""
    class_name = f"Add{model_name.replace('System', '')}Params"
    
    code = f"""
class {class_name}(BaseModel):
    \"\"\"
    {description}
    \"\"\"
    model_config = ConfigDict()
"""
    
    for field in fields:
        #  # (description)
        if field["name"] in ["id", "created_at", "updated_at", "is_del"]:
            continue
            
        field_name = field["name"]
        pydantic_type = field["pydantic_type"]
        description = field["description"]
        max_length = field["max_length"]
        default = field["default"]
        required = field["required"]
        
        #  # (description)
        if field["name"] in ["password"] and field["null"]:
            required = True
            pydantic_type = pydantic_type.replace("Optional[", "").replace("]", "")
        
        #  # (description)
        field_params = []
        if not required:
            if default is not None:
                field_params.append(f"default={default}")
            else:
                field_params.append("default=None")
        else:
            field_params.append("...")
        
        if max_length:
            field_params.append(f"max_length={max_length}")
        
        if description:
            field_params.append(f'description="{description}"')
        
        field_def = f"Field({', '.join(field_params)})"
        
        code += f"    {field_name}: {pydantic_type} = {field_def}\n"
    
    code += "\n"
    return code


def generate_update_schema(model_name: str, description: str, fields: List[Dict]) -> str:
    """schema"""
    class_name = f"Update{model_name.replace('System', '')}Params"
    
    code = f"""
class {class_name}(BaseModel):
    \"\"\"
    {description}
    \"\"\"
    model_config = ConfigDict()
"""
    
    for field in fields:
        #  # (description)
        if field["name"] in ["id", "created_at", "updated_at", "is_del"]:
            continue
            
        field_name = field["name"]
        pydantic_type = field["pydantic_type"]
        description = field["description"]
        max_length = field["max_length"]
        
        #  # (description)
        if not pydantic_type.startswith("Optional"):
            pydantic_type = f"Optional[{pydantic_type}]"
        
        #  # (description)
        field_params = ["default=None"]
        
        if max_length:
            field_params.append(f"max_length={max_length}")
        
        if description:
            field_params.append(f'description="{description}"')
        
        field_def = f"Field({', '.join(field_params)})"
        
        code += f"    {field_name}: {pydantic_type} = {field_def}\n"
    
    code += "\n"
    return code


def generate_list_schemas(model_name: str, description: str) -> str:
    """schema"""
    base_name = model_name.replace('System', '')
    
    code = f"""
class Get{base_name}ListResult(ListQueryResult):
    \"\"\"
    {description}
    \"\"\"
    result: List[{base_name}Info] = Field(default=[], description="{description}")

"""
    return code


def generate_response_schemas(model_name: str, description: str) -> str:
    """schema"""
    base_name = model_name.replace('System', '')
    
    code = f"""
class Get{base_name}InfoResponse(BaseResponse):
    \"\"\"
    {description}
    \"\"\"
    data: {base_name}Info = Field(default=None, description="{description}")


class Get{base_name}ListResponse(BaseResponse):
    \"\"\"
    {description}
    \"\"\"
    data: Get{base_name}ListResult = Field(default=None, description="")

"""
    return code


def create_schema_file(model_name: str, schema_types: List[str]) -> str:
    """schema"""
    try:
        #  # (description)
        model_file = None
        for file_path in MODELS_DIR.glob("*.py"):
            if file_path.name in ["__init__.py", "common.py"]:
                continue
            
            content = file_path.read_text(encoding="utf-8")
            if f"class {model_name}(BaseModel):" in content:
                model_file = file_path
                break
        
        if not model_file:
            return f"  ?{model_name}"
        
        #  # (description)
        schema_filename = f"{model_name.lower().replace('system', '')}.py"
        schema_file = SCHEMAS_DIR / schema_filename
        
        if schema_file.exists():
            return f" Schema {schema_filename}     create_schema_from_model_force    "
        
        #  # (description)
        models = analyze_model_file(model_file)
        target_model = None
        
        for model in models:
            if model["name"] == model_name:
                target_model = model
                break
        
        if not target_model:
            return f"   ?{model_file.name}  {model_name}"
        
        #  # (description)
        schema_code = generate_schema_code(target_model, schema_types)
        
        #  # (description)
        SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)
        
        #  # (description)
        schema_file.write_text(schema_code, encoding="utf-8")
        
        return f"?Schema {schema_filename} "
        
    except Exception as e:
        return f"schema: {str(e)}"


def list_available_models() -> str:
    """List available models"""
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
                    "models": class_matches
                })
        
        if not models:
            return "No models found"
        
        result = ":\n"
        for model_info in models:
            result += f"\n {model_info['file']}\n"
            for model_name in model_info['models']:
                result += f"    {model_name}\n"
        
        return result
        
    except Exception as e:
        return f": {str(e)}"


def list_existing_schemas() -> str:
    """chema"""
    try:
        if not SCHEMAS_DIR.exists():
            return "Schemas directory does not exist"
        
        schema_files = []
        for file_path in SCHEMAS_DIR.glob("*.py"):
            if file_path.name == "__init__.py":
                continue
            schema_files.append(file_path.name)
        
        if not schema_files:
            return "chema"
        
        result = "Schema:\n"
        for filename in sorted(schema_files):
            result += f"  ?{filename}\n"
        
        return result
        
    except Exception as e:
        return f"schema: {str(e)}"


def create_schema_file_force(model_name: str, schema_types: List[str]) -> str:
    """schema"""
    try:
        #  # (description)
        model_file = None
        for file_path in MODELS_DIR.glob("*.py"):
            if file_path.name in ["__init__.py", "common.py"]:
                continue
            
            content = file_path.read_text(encoding="utf-8")
            if f"class {model_name}(BaseModel):" in content:
                model_file = file_path
                break
        
        if not model_file:
            return f"  ?{model_name}"
        
        #  # (description)
        models = analyze_model_file(model_file)
        target_model = None
        
        for model in models:
            if model["name"] == model_name:
                target_model = model
                break
        
        if not target_model:
            return f"   ?{model_file.name}  {model_name}"
        
        #  # (description)
        schema_code = generate_schema_code(target_model, schema_types)
        
        #  # (description)
        schema_filename = f"{model_name.lower().replace('system', '')}.py"
        schema_file = SCHEMAS_DIR / schema_filename
        
        #  # (description)
        SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)
        
        #  # (description)
        schema_file.write_text(schema_code, encoding="utf-8")
        
        status = "" if schema_file.exists() else ""
        return f"?Schema {schema_filename} {status}"
        
    except Exception as e:
        return f"schema: {str(e)}"
def register(mcp):
    """Register schema tools with MCP service"""
    
    @mcp.tool()
    def create_schema_from_model(
        model_name: str,
        schema_types: list = None
    ) -> str:
        """
        Create schema file from model (without overwriting existing files)

        Args:
            model_name: Model class name (e.g. SystemUser)
            schema_types: Schema types to generate, options: ["info", "add", "update", "list", "response"]
                         Default: generate all types

        Returns:
            Creation result info
        """
        if schema_types is None:
            schema_types = ["info", "add", "update", "list", "response"]
        
        return create_schema_file(model_name, schema_types)
    
    @mcp.tool()
    def create_schema_from_model_force(
        model_name: str,
        schema_types: list = None
    ) -> str:
        """
        schema
        
        Args:
            model_name: ystemUser?
            schema_types: schema["info", "add", "update", "list", "response"]
                        ?
        
        Returns:
            
        """
        if schema_types is None:
            schema_types = ["info", "add", "update", "list", "response"]
        
        return create_schema_file_force(model_name, schema_types)
    
    @mcp.tool()
    def list_available_models_for_schema() -> str:
        """
        chema  ?
        
        Returns:
            
        """
        return list_available_models()
    
    @mcp.tool()
    def list_existing_schema_files() -> str:
        """
        chema
        
        Returns:
            schema
        """
        return list_existing_schemas()
    
    @mcp.tool()
    def analyze_model_structure(model_name: str) -> str:
        """
        ?
        
        Args:
            model_name: 
            
        Returns:
            
        """
        try:
            #  # (description)
            model_file = None
            for file_path in MODELS_DIR.glob("*.py"):
                if file_path.name in ["__init__.py", "common.py"]:
                    continue
                
                content = file_path.read_text(encoding="utf-8")
                if f"class {model_name}(BaseModel):" in content:
                    model_file = file_path
                    break
            
            if not model_file:
                return f"  ?{model_name}"
            
            #  # (description)
            models = analyze_model_file(model_file)
            target_model = None
            
            for model in models:
                if model["name"] == model_name:
                    target_model = model
                    break
            
            if not target_model:
                return f"   ?{model_file.name}  {model_name}"
            
            #  # (description)
            result = f": {model_name}\n"
            result += f": {target_model['description']}\n"
            result += f": {target_model['file']}\n\n"
            result += ":\n"
            
            for field in target_model['fields']:
                result += f"  ?{field['name']}: {field['type']} -> {field['pydantic_type']}\n"
                if field['description']:
                    result += f"    : {field['description']}\n"
                if field['max_length']:
                    result += f"    Max length: {field['max_length']}\n"
                result += f"    Required: {'Yes' if field['required'] else 'No'}\n"
                if field['default'] is not None:
                    result += f"    Default: {field['default']}\n"
                result += "\n"
            
            return result
            
        except Exception as e:
            return f": {str(e)}"


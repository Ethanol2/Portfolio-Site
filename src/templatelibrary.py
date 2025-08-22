import os

class TemplateLibrary:
    def __init__(self, templates_path: str, base_path: str) -> None:
        
        if not os.path.exists(templates_path):
            raise Exception(f'Templates folder doesn\'t exist. "{templates_path}"')
        
        templates = self.__import_templates(templates_path)
        
        if len(templates) == 0:
            raise Exception(f'Error: No templates found in the templates folder. "{templates_path}"')
        
        if "default" not in templates.keys():
            first_key = next(iter(templates))
            templates["default"] = templates[first_key]
        
        for template in templates.keys():
            template_contents = templates[template]
            
            template_contents = template_contents.replace('href="/', f'href="{base_path}')
            template_contents = template_contents.replace('src="/', f'src="{base_path}')
            
            templates[template] = template_contents
        
        self.__templates = templates
        
    def __import_templates(self, templates_path: str) -> dict:
        
        templates = {}
        
        for item in os.listdir(templates_path):
            
            path = os.path.join(templates_path, item)
            
            if os.path.isfile(path):
                if '.html' in item:
                    
                    with open(path) as f:
                        template_contents = f.read()
                        f.close()
                    
                    templates[item[:-5].lower()] = template_contents
            else:
                templates = templates | self.__import_templates(path)
        
        return templates
    
    def get_template(self, template_name: str) -> str:
        
        if template_name not in self.__templates.keys():
            raise Exception(f'Error: Missing template "{template_name}"')
        
        return self.__templates[template_name]
from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from execute.execute import execute
from root import root
import os


def generate(template_name, output_name, render_vars):
    env = Environment(trim_blocks = True, lstrip_blocks = True, loader = PackageLoader("generation", "templates"))
    template = env.get_template(template_name)
    rendered = template.render(render_vars)
    print(rendered)
    #i pisemo u fajl
    file_name = os.path.join(root, "output", output_name)
    print(file_name)
    with open(file_name, "w+") as f:
        f.write(rendered)

def main(debug = False):
    
    model = execute(os.path.join(root, "forms"), 'forms.tx', 'example.form', debug, debug)
    generate("form_template.html", "form.html", {"form" : model})
    
if __name__ == '__main__':
    main(True)


    
                    
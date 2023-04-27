from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())

template_name = "login"
template_file = f"{template_name}.j2"
template = env.get_template(template_file)


output_file = f"tmp_{template_name}.html"
f = open(output_file, "w")
f.write(template.render(title="Login"))
f.close()

print(f"Template {template_file} rendered to {output_file}")

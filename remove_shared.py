
import os
import shutil
import toml

# TODO: - Implement as plugin

project_paths = [
    'shared',
    'l2-shared',
    'projects/base/linear-regression'
]


if __name__ == '__main__':
    for project in project_paths:
        toml_file = os.path.join(project, 'pyproject.toml')

        with open(toml_file, "r") as f:
            data = toml.load(f)
            data = data['tool']['kedro']
            
            package_name = data['package_name']
            
            if 'pull' not in data['micropkg']:
                continue
            
            pull = data['micropkg']['pull']
            
            for key, value in pull.items():
                destination = value['destination']
                alias = value['alias']
                
                source_path = os.path.join(project, 'src', package_name, destination, alias)
                tests_path = os.path.join(project, 'src', 'tests', destination, alias)
                
                try:
                    shutil.rmtree(source_path)
                    shutil.rmtree(tests_path)
                except Exception as exc:
                    print(exc)

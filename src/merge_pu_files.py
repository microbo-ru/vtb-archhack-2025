import os
import glob
import re


def merge_files(directory, mask, output_file, exclude_phrases, header, footer):
    files = []

    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if glob.fnmatch.fnmatch(filename, mask):
                files.append(os.path.join(root, filename))

    with open(output_file, 'w') as outfile:
        content_set = set()
        for file in files:
            with open(file) as infile:
                content = infile.read()
                for phrase in exclude_phrases:
                    content = content.replace(phrase, '')
                    # Разделение содержимого файла на секции

                # Разделение содержимого файла на секции вида 'class ... {...}'
                class_sections = re.findall(r'class\s+.*?\}', content, flags=re.DOTALL)
                enum_sections = re.findall(r'enum\s+.*?\}', content, flags=re.DOTALL)

                for section in class_sections:
                    section = section.strip()
                    print(section)
                    content_set.add(section)

                for section in enum_sections:
                    section = section.strip()
                    print(section)
                    content_set.add(section)

        outfile.write(header)
        # Запись уникальных секций в выходной файл
        for section in content_set:
            outfile.write(section + '\n\n')
        outfile.write(footer)


def extract_entity_names(plantuml_file):
    with open(plantuml_file, 'r') as f:
        content = f.read()

        # Извлечение названий классов и enum-ов
        class_names = re.findall(r'class\s+(\w+)', content)
        enum_names = re.findall(r'enum\s+(\w+)', content)

        return class_names + enum_names


def generate_dependencies(plantuml_file):
    entities = set(extract_entity_names(plantuml_file))

    with open(plantuml_file, 'r') as f:
        content = f.read()

        # Извлечение классов и их атрибутов
        classes = re.findall(r'class\s+(\w+)\s*{([^}]*)}', content)

        # Генерация зависимостей
        dependencies = []
        for class_name, attributes in classes:
            attribute_classes = re.findall(r'\+\w+\s*:\s*(\w+)', attributes)
            for attribute_class in attribute_classes:
                if attribute_class in entities:
                    dependencies.append(f'{class_name} --> {attribute_class}')

        return dependencies

def write_dependencies(output_file):
    dependencies = generate_dependencies(output_file)

    with open(output_file, 'a') as f:
        f.write("' Dependencies:\n")
        for dependency in dependencies:
            f.write(f'{dependency}\n')

# Пример использования
exclude = ['@startuml', '@enduml']
header = '@startuml\n\n'
footer = '\n\n@enduml'

output_file = './../generated/merged.pu'

merge_files('./../generated', '*.pu', output_file, exclude, header, footer)
write_dependencies(output_file)

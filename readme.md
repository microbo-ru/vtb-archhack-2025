# См. решение в папке plantuml


## xsd to plantuml

```shell
 xsdata generate "./in/cbdc_album_v2025.07/xsd_2025.07" -r  --output plantuml
```

this will produce a new folder, named 'generated', which has a structure similar to file patterns&
each folder will have a .pu file, representing a plantuml diagram

unfortunately, the generated file doesn't have a dependencies of the object.
To achieve that we use a LLM to generate and additional dependencies section:

prompt: 
"Ты - помощник разработчика. Добавь в существующий plantuml файл все связи между объектами. Связи должны быть направленными. Признак множественности связей указывай только для коллекций."

## plantuml to .png

```shell
# для обхода всех директорий
plantuml "./generated/**/*.pu"

# или для одного файла
plantuml "./generated/merged.pu" -DPLANTUML_LIMIT_SIZE=64000
```

Will produce a .png file next to the each .pu file.

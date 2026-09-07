#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Create or update a text file

version_added: "1.0.0"

description:
    - Creates a text file at the specified path.
    - Writes specified content to the file.
    - Does not change the file if its content is already correct.

options:
    path:
        description:
            - Path to the text file.
        required: true
        type: path

    content:
        description:
            - Content that should be written to the file.
        required: true
        type: str

author:
    - Your Name
'''

EXAMPLES = r'''
- name: Create text file
  my_own_module:
    path: /tmp/example.txt
    content: "Hello world!"
'''

RETURN = r'''
path:
    description: Path to the managed file.
    type: str
    returned: always

message:
    description: Result message.
    type: str
    returned: always
'''

import os

from ansible.module_utils.basic import AnsibleModule


def run_module():

    module_args = dict(
        path=dict(
            type='path',
            required=True
        ),
        content=dict(
            type='str',
            required=True
        )
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    current_content = None

    # Если файл уже существует - читаем его
    if os.path.exists(path):

        if not os.path.isfile(path):
            module.fail_json(
                changed=False,
                msg='Specified path exists but is not a regular file',
                path=path
            )

        try:
            with open(path, 'r', encoding='utf-8') as file:
                current_content = file.read()

        except OSError as error:
            module.fail_json(
                changed=False,
                msg='Unable to read file: {0}'.format(error),
                path=path
            )

    # Если содержимое уже правильное - ничего не меняем
    if current_content == content:
        module.exit_json(
            changed=False,
            path=path,
            message='File is already up to date'
        )

    # Проверка check mode
    if module.check_mode:
        module.exit_json(
            changed=True,
            path=path,
            message='File would be created or updated'
        )

    # Получаем родительскую директорию
    parent_directory = os.path.dirname(path)

    # Если директории нет - создаём
    if parent_directory:
        try:
            os.makedirs(
                parent_directory,
                exist_ok=True
            )

        except OSError as error:
            module.fail_json(
                changed=False,
                msg='Unable to create directory: {0}'.format(error),
                path=path
            )

    # Создаём или перезаписываем файл
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)

    except OSError as error:
        module.fail_json(
            changed=False,
            msg='Unable to write file: {0}'.format(error),
            path=path
        )

    module.exit_json(
        changed=True,
        path=path,
        message='File created or updated'
    )


def main():
    run_module()


if __name__ == '__main__':
    main()

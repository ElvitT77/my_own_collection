## Example playbook

```yaml
---
- name: Use my own collection role
  hosts: localhost
  connection: local
  gather_facts: false

  roles:
    - my_own_namespace.yandex_cloud_elk.my_own_role
```

## Build

```bash
ansible-galaxy collection build
```

## Install

```bash
ansible-galaxy collection install my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz
```

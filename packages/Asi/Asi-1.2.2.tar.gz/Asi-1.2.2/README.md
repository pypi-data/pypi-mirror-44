### 说明

这是一个Ansible Python Api的封装。

### 安装

```bash
$ python setup.py install
```

### 简单使用

```python
from Asi import Api


if __name__ == "__main__":
	hosts = [
		{
			"hostname": "localhost",
			"port": 22,
			"vars": {
				"ansible_ssh_user": "root",
				"ansible_ssh_pass": "p@ssw0rd"
			}
		},
		{
			"hostname": "192.168.152.142",
			"port": 22,
			"vars": {
				"ansible_ssh_user": "root",
				"ansible_ssh_pass": "p@ssw0rd"
			}
		}
	]

	Api().module("shell", args="ls", register='shell_out', task_name="test")\
		 .module("debug", args={"msg":"{{shell_out.stdout}}"})\
		 .run(hosts)	
```

### 获取返回数据

在`run`方法前面调用`json`方法，并且`run`方法中`callback`参数需为`None`，如果自己实现`callback`, 则需要在`callback`增添属性`results`

```python
from Asi import Api
import json


if __name__ == "__main__":
	hosts = [
		dict(hostname="127.0.0.1", port=22)
	]

	api = Api()
	api = api.module("shell", args="ls", register="shell_out")
	api = api.module("debug", args=dict(msg="{{shell_out}}"))
	api = api.json()
	print("result")
	print(json.dumps(api.run(hosts), indent=4))
```

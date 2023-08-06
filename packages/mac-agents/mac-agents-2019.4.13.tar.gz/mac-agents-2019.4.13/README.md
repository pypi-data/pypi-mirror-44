<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-agents.svg?longCache=True)](https://pypi.org/project/mac-agents/)

#### Installation
```bash
$ [sudo] pip install mac-agents
```

#### Classes
class|`__doc__`
-|-
`mac_agents.Agent` |launchd.plist generator. Capital letter attrs/props as launchd.plist keys

#### Functions
function|`__doc__`
-|-
`mac_agents.jobs()` |return a list of launchctl Job objects (`pid`, `status`, `label`)
`mac_agents.read(path)` |return a dictionary with plist file data
`mac_agents.update(path, **kwargs)` |update plist file data
`mac_agents.write(path, data)` |write data dictionary to a plist file

#### Executable modules
usage|`__doc__`
-|-
`python -m mac_agents.create path ...` |generate launchd.plist from python file(s)
`python -m mac_agents.tag [path]` |set Finder tags. `red` - status, `orange` - stderr, `gray` - unloaded

#### Examples
`~/Library/LaunchAgents/file.py`
```python
import mac_agents

class Agent(mac_agents.Agent):
    StartInterval = 5  # capital letter

    def run(self):
        pass

if __name__ == "__main__":
    Agent().run()
```

```bash
$ find ~/Library/LaunchAgents -name "*.py" | xargs python -m mac_agents.create "$@"
$ find ~/Library/LaunchAgents -name "*.plist" | xargs launchctl load # or launchctl unload
$ launchctl list | grep .py$ | awk '{print $3}' | xargs -I '{}' launchctl remove {}
$ find ~/Library/LaunchAgents -name "*.py.plist" -exec rm {} +
```

#### Links
+   [launchd.plist](https://www.real-world-systems.com/docs/launchd.plist.5.html)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>
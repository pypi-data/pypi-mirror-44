<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install launchd-exec
```

#### Scripts usage
```bash
usage: launchd-exec command [args ...]
```

#### Examples
```bash
$ launchd-exec bash -l path/to/script.sh
```

logs:
```
~/Library/Logs/launchd-exec/bash/<datetime>.<pid>/launchd.plist
~/Library/Logs/launchd-exec/bash/<datetime>.<pid>/out.log
~/Library/Logs/launchd-exec/bash/<datetime>.<pid>/err.log
```

#### Related projects
+   [`launchd-env` - launchd.plist environment variables](https://pypi.org/project/launchd-env/)
+   [`launchd-exec` - execute script via launchd](https://pypi.org/project/launchd-exec/)
+   [`launchd-generator` - launchd.plist generator](https://pypi.org/project/launchd-generator/)
+   [`launchd-logs` - launchd.plist logs](https://pypi.org/project/launchd-logs/)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>
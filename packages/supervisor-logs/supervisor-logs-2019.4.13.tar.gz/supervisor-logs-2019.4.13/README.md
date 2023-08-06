<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/supervisor-logs.svg?longCache=True)](https://pypi.org/project/supervisor-logs/)

#### Installation
```bash
$ [sudo] pip install supervisor-logs
```

#### Executable modules
usage|`__doc__`
-|-
`python -m supervisor_logs.add path ...` |add stdout_logfile and stderr_logfile to supervisor config sections
`python -m supervisor_logs.clear path ...` |clear log files
`python -m supervisor_logs.mkdir path ...` |create stdout_logfile and stderr_logfile dirs

#### Examples
`file.ini` before
```
[program:name]
```

```bash
$ export SUPERVISOR_LOGS=~/Library/Logs
$ python -m supervisor_logs.add file.ini
```

`file.ini` after
```
[program:name]
stderr_logfile = ~/Library/Logs/supervisor/name/err.log
stdout_logfile = ~/Library/Logs/supervisor/name/out.log
```

```bash
$ find . -name "*.ini" -exec supervisor_logs.add {} \;  # add logs to program sections
$ find . -name "*.ini" -exec supervisor_logs.mkdir {} \;  # make log directories
$ find . -name "*.ini" -exec supervisor_logs.clear {} \;  # clear log files
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>
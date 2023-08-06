<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install travis-exec
```

#### Features
+   `{}` replaced with repo name

#### Scripts usage
```bash
usage: travis-exec args ...
```

#### Examples
```bash
$ travis-exec travis status -r {}
$ travis-exec python -m travis_cron.add {} master daily no
$ travis-exec python -m travis_env.set {} WEBHOOK_URL "$WEBHOOK_URL"
```

#### Related projects
+   [`travis-generator` - `.travis.yml` generator](https://pypi.org/project/travis-generator/)
+   [`travis-cron` - manage travis cron](https://pypi.org/project/travis-cron/)
+   [`travis-env` - manage travis environment variables](https://pypi.org/project/travis-env/)
+   [`travis-exec` - execute command for all travis repos](https://pypi.org/project/travis-exec/)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>
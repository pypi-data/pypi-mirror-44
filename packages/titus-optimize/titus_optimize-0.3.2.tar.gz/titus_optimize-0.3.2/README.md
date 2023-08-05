## Virtual Environment
Setup a virtual environment before executing any build/test/release opearations.

```bash
$ virtualenv --python=python3.6 venv
...
Installing setuptools, pip, wheel...
done.
$ . venv/bin/activate
```

## Test
We use tox to run tests. After setting up a virtual environment, requirements and tox must be installed.

```bash
(venv) $ pip3 install -r requirements.txt
(venv) $ pip3 install tox
(venv) $ tox
...
  py36: commands succeeded
  linters: commands succeeded
  congratulations :)
```

## Build a development package
To build a package for development purposes, do the following.
```bash
(venv) $ python3 setup.py sdist bdist_wheel
running sdist
running egg_info
...
adding 'titus_optimize-0.0.14+hlocal.g34f75d0.dirty.dist-info/METADATA'
adding 'titus_optimize-0.0.14+hlocal.g34f75d0.dirty.dist-info/WHEEL'
adding 'titus_optimize-0.0.14+hlocal.g34f75d0.dirty.dist-info/top_level.txt'
adding 'titus_optimize-0.0.14+hlocal.g34f75d0.dirty.dist-info/RECORD'
removing build/bdist.macosx-10.9-x86_64/wheel
```

The packages will be in the generated `dist` directory
```bash
(venv) $ ls dist
titus_optimize-0.0.14+hlocal.g34f75d0.dirty-py3-none-any.whl titus_optimize-0.0.14+hlocal.g34f75d0.dirty.tar.gz
```

## Release
1. Checkout the `master` branch
```bash
$ git checkout master
$ git pull
```

2. Update the `VERSION` variabled in `setup.py`
```bash
$ git diff HEAD~1 setup.py
diff --git a/setup.py b/setup.py
index f1a9f38..3078372 100755
--- a/setup.py
+++ b/setup.py
@@ -5,7 +5,7 @@ from setuptools import setup
 from setuptools.command.install import install


-VERSION = "0.1.4"
+VERSION = "0.1.5"

 def readme():
     """print long description"""
```

3. Commit that change
```bash
$ git add setup.py
$ git commit -m "Release 0.1.5"
```

4. Tag the commit with the same version in `setup.py`
```bash
$ git tag 0.1.5
```

5. Push the commit to `master`
```bash
$ git push origin master
```

6. Push the tags to `master`
```bash
$ git push --tags
```

This will kick off a CI job which will publish to [pypi](https://pypi.org/project/titus-optimize/).

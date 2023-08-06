Use this mini-tool to manage python script `argparse` arguments in modularized
fashion. Supports `yml` and `json` formats.

For example, a script that accepts two sets of argument groups (e.g. the first
group has arguments `--foo1` and `--foo2` and the second group has arguments
`--bar1` and `--bar2`) can be run by the following command:

```
python -m runscript foobar.py --args foo.yml --args bar.yml
```

where `foo.yml` and `bar.yml` specifies arguments using `yaml` format:

```yaml
foo1: hello
foo2: world
```

This is equivalent to directly calling the script with following arguments:

```
python foobar.py --foo1 hello --foo2 world --bar1 ... --bar2 ...
````

The advantage of such approach is that arguments can be managed separately and
in modularized fashion without resorting to off-shelf `argparse`-variant
packages.

Also supports calling individual modules (i.e. `python -m <module>`). To use
the functionality, specify `--run-module` and `--module-path` if the module
is not part of any package and sits somewhere else.

All arguments to `script-runner` can be organized in a single argument file, e.g.

```
python -m runscript @some.args
```

where `some.args` is a text file that contains an argument token for each line.
This is standard [`fromfile_prefix_chars`](https://docs.python.org/3/library/argparse.html#fromfile-prefix-chars)
behavior.


### Installing ###

`python setup.py develop` or `python setup.py install` will do.


### Main Features ###

For standalone scripts, the main syntax is as follows.

```
python -m runscript <path-to-script> [--python PYTHON] [--args ARGS]* [--<any-arg> <val>?]*
```

 * `python`: python executable. defaults to `/usr/bin/env python`
 * `args`: path to an argument file. supports `yml` and `json` format. can be multiple.
 * other arguments: any additional arguments will be passed down to the script.


### Additional Features ###

Adding an additional layer of abstraction on argument parsing allows declaration
and management of variables. For example, running

```
python -m runscript train.py --ckpt-path "model-e{epoch}" --log-path "logs-e{epoch}.txt" --epoch 12
```

will ensure that `epoch` variable is resolved and the script is called with following arguments:

```
python train.py --ckpt-path model-e12 --log-path logs-e12.txt --epoch 12
```

There are also pre-defined keywords such as

  * `{%module-name%}`: name of the running module
  * `{%working-dir%}`: current running directory
  * `{%config-dir%}`: current config file directory.
  * `{%config-name%}`: name of the current config file
   
Note that there is no way for `runscript` to distinguish valid arguments of the script, hence all arguments, including `--epoch` in above example, will be passed
down to script arguments indiscriminately. In such cases, the script should be modified to [partially parse arguments](https://docs.python.org/3/library/argparse.html#partial-parsing) to avoid errors.


### Misc. ###

This package was developed to make managing deep learning experiments easier.
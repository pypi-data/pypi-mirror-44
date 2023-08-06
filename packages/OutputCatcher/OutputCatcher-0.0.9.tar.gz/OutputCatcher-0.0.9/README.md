# OutputCatcher

Provides a context manager that catches/suppresses output from `sys.stderr` and
`sys.stdout` (StdOutCatcher, StdErrCatcher). Also provides an easy way to
gather both stdout and stderr from processes while optionally piping stdin
to the process as a `str` or `bytes`.

## API

### StdOutCatcher / StdErrCatcher

```python
StdOutCatcher(escaped=False, max_length=0)
```

This will suppress any output running through `sys.stdout` or `sys.stderr`,
and save it in an attribute for possible future use.

#### Arguments

- `escaped`: If truthy, output is "encoded" using `repr()`, but without quotes.
Default: `False`
- `max_length`: If non-zero, final output will not exceed `max_length`.
Once `max_length` is reached, further `write()` calls will be ignored.
Default: `0`

#### Usage

```python
from outputcatcher import StdErrCatcher, StdOutCatcher

# Catching stdout
with StdOutCatcher() as fakeout:
    print('This is a test. you shouldn\'t see it right away.')
print('Captured stdout: {}'.format(fakeout.output))

# Catching stderr
with StdErrCatcher() as fakeerr:
    print('Testing stderr output.', file=sys.stderr)
print('Captured stderr: {}'.format(fakeerr.output))
```

### ProcessOutput

```python
ProcessOutput(args, stdin_data=None, timeout=None, **popenkwargs)
```

This runs an external process using `subprocess.Popen` and gathers both the
`stdout` and `stderr` output in an attribute for future use.
`stdin` data can be piped to the process initially, by providing the data as
a `str` or `bytes` during initialization.

After initializing a `ProcessOutput` object with a command to run, and optional
stdin input data, it can either be used as a context manager or the `run()`
method must be called.

`timeout` is passed to `self.proc.wait()` before returning
the output.

**Note**: As of Python 3.5,
[subprocess.run()](https://docs.python.org/3/library/subprocess.html?highlight=subprocess.run#subprocess.run)
can do much of this through the `input` argument and the
[subprocess.CompletedProcess](https://docs.python.org/3/library/subprocess.html?highlight=subprocess.CompletedProcess#subprocess.CompletedProcess)
return value.
Though `ProcessOutput` does provide a handy method for iterating over output
as it is received (`iter_stdout`, and `iter_stderr`).

#### Arguments

- `args `: Command arguments, same as subprocess.Popen.
- `stdin_data`: str or bytes to send to command as stdin. Default: `None`
- `timeout`: Time to wait for process after collecting data. Default: `None`
- `**popenkwargs`: Any extra kwargs for Popen(). `stdin`, `stdout`, and `stderr` are ignored.

#### Usage
```python
from outputcatcher import ProcessOutput

# Basic usage:
with ProcessOutput(['ls']) as p:
    print(p.stdout.decode())

# Checking for stdout and stderr:
with ProcessOutput(['ls', '/totally_nonexistent_dir']) as p:
    if p.stdout:
        print('Wow, it really does exist: {}'.format(p.stdout.decode()))
    else:
        print(p.stderr.decode())

# Without a context manager:
p = ProcessOutput(['ls'])
stdout, stderr = p.run()

# Sending stdin data to a process:
stdin_data = 'Hello cat!'
with ProcessOutput(['cat'], stdin_data=stdin_data) as p:
    assert p.stdout.decode() == stdin_data
    # cat received the data, and piped it back.
    print(p.stdout.decode())

# Iterating over stdout data:
p = ProcessOutput(['ls'])
for line in p.iter_stdout():
    print(line)
```

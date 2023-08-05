Easy context prefixes for messages.


Dynamic message prefixes providing execution context.

The primary facility here is Pfx,
a context manager which maintains a per thread stack of context prefixes.

Usage is like this:

    from cs.pfx import Pfx
    ...
    def parser(filename):
      with Pfx("parse(%r)", filename):
        with open(filename) as f:
          for lineno, line in enumerate(f, 1):
            with Pfx("%d", lineno) as P:
              if line_is_invalid(line):
                raise ValueError("problem!")
              P.info("line = %r", line)

This produces log messages like:

    datafile: 1: line = 'foo\n'

and exception messages like:

    datafile: 17: problem!

which lets one put just the relevant complaint in exception and log
messages and get useful calling context on the output.
This does make for wordier logs and exceptions
but used with a little discretion produces far more debugable results.

## Function `gen(func)`

Decorator for generators to manage the Pfx stack.

Before running the generator the current stack height is
noted.  After yield, the stack above that height is trimmed
and saved, and the value yielded.  On recommencement the saved
stack is reapplied to the current stack (which may have
changed) and the generator continued.

## Class `Pfx`

A context manager to maintain a per-thread stack of message prefixes.

## Function `pfx(func)`

Decorator for functions that should run inside:

    with Pfx(func_name):

Use:

    @pfx
    def f(...):

## Function `pfx_iter(tag, iterable)`

Wrapper for iterables to prefix exceptions with `tag`.

## Class `PfxCallInfo`

MRO: `Pfx`  
Subclass of Pfx to insert current function an caller into messages.

## Function `pfxtag(tag, loggers=None)`

Decorator for functions that should run inside:

    with Pfx(tag, loggers=loggers):

Use:

    @pfxtag(tag)
    def f(...):

## Function `PfxThread(target=None, **kw)`

Factory function returning a Thread
which presents the current prefix as context.

## Function `prefix()`

Return the current Pfx prefix.

## Function `PrePfx(tag, *args)`

Push a temporary value for Pfx._state._ur_prefix to enloundenify messages.

## Function `XP(msg, *args, **kwargs)`

Variation on `cs.x.X`
which prefixes the message with the currrent Pfx prefix.

## Function `XX(prepfx, msg, *args, **kwargs)`

Trite wrapper for `XP()` to transiently insert a leading prefix string.

Example:

    XX("NOTE!", "some message")

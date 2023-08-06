# qz7.subprocess_w

A Popen wrapper for graceful process termination

This package provides a Popen wrapper class
called PopenW that termimates subprocess cleanly,
instead of leaving zombie or orphan processes
when the parent process raises an unexpected exception.

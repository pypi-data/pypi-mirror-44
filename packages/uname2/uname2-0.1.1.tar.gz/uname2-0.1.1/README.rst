uname2
======

Print system information.

Install
-------

::

    pip install uname2


Usage
-----

::

    PS E:\code\uname2> uname2 --help
    Usage: uname2 [OPTIONS]

    Print certain system information.  With no OPTION, same as -s.

    Options:
    -a, --all             print all information
    -s, --kernel-name     print the kernel name
    -n, --nodename        print the network node hostname
    -r, --kernel-release  print the kernel release
    -v, --kernel-version  print the kernel version
    -m, --machine         print the machine hardware name
    -p, --processor       print the hardware platform or "unknown"
    --help                Show this message and exit.
    PS E:\code\uname2>

Example
-------

::

    PS E:\code\uname2> uname2
    Windows
    PS E:\code\uname2> uname2 -a
    Windows DESKTOP-OR9GS4G 10 10.0.16299 AMD64 Intel64 Family 6 Model 60 Stepping 3, GenuineIntel
    PS E:\code\uname2> uname2 -snrvmp
    Windows DESKTOP-OR9GS4G 10 10.0.16299 AMD64 Intel64 Family 6 Model 60 Stepping 3, GenuineIntel
    PS E:\code\uname2>

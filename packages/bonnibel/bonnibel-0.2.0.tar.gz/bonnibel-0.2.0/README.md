# Bonnibel

Bonnibel (`pb` for short) builds [Ninja][] build files for a set of modules.
Bonnibel is a thin wrapper around [Jinja][] templates defining both _modules_
to be built and the _targets_ to build them for. This allows expressive power
in using Ninja's simple but otherwise very powerful build definition language.

For example, Bonnibel was created for [Popcorn][], where I needed the ability
to build tools for my local native environment, use those tools to make output
files used by other build stages, and build the bootloader, kernel and
user-space applications all with different compiler and linker options.
Complicating things even more, several libraries need to be built and used by
applications on multiple target environments.

[Ninja]: https://ninja-build.org
[Jinja]: https://jinja.pocoo.org
[Popcorn]: https://github.com/justinian/popcorn

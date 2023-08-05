# Give me `cached_property`!

The `cached_property` decorator is not in the standard library,
but it's so useful that it has been implemented all over the place.

It seems that some implementations have reference to the `bottle` package,
so I guess it's where everything started.

Then we have a standalone package called `cached_property`,
but it has a rather complicated implementation (async, timeout, etc.)
that we don't necessarily need.

The simple version is included in a lot of popular libraries,
such as `django`,
and distribution libraries like `distlib`, `distro` and `pip`.
All of them have very similar if not identical implementation.

What if you just want to use the `cached_property` decorator
without worrying about dependencies?

What if you are a library creator
and you don't want to include unnecessary dependencies,
nor do you want to copy-paste the implementation yourself?

```python
from gimme_cached_property import cached_property
```

This will look at your installed packages
and attempt to import the decorator for you.
If none available, it will raise an `ImportError`.

## Installation

```bash
pip install gimme_cached_property
```

## Supported implementations

| Name | Package | Location |
| --- | --- | --- |
| `bottle` | `bottle` | `bottle.cached_property` |
| `cached_property` | `cached_property` | `cached_property.cached_property` |
| `distlib` | `distlib` | `distlib.util.cached_property` |
| `distro` | `distro` | `distro.cached_property` |
| `django` | `Django` | `django.utils.functional.cached_property` |
| `pip_internal` | `pip` | `pip._internal.utils.misc.cached_property` |
| `pip_vendor_distlib` | `pip` | `pip._vendor.distlib.util.cached_property` |
| `pip_vendor_distro` | `pip` | `pip._vendor.distro.cached_property` |
| `werkzeug` | `Werkzeug` | `werkzeug.utils.cached_property` |

Kudos to PyCharm for helping me find them...

## Precedence

By default, the try order is:

* Original implementation (presumably)
    * `bottle`
* Web frameworks
    * `django`
    * `werkzeug`
* Standalone
    * `cached_property`
* Distribution libraries
    * `distlib`
    * `distro`
    * `pip_internal`
    * `pip_vendor_distlib`
    * `pip_vendor_distro`

Which means you won't run out of options as long as you still have `pip`.

You can customize the order by using the `CACHED_PROPERTY_TRY_ORDER` environment variable, e.g.

```bash
CACHED_PROPERTY_TRY_ORDER=django,cached_property
```

Which will reorder and/or limit the choices to your liking.

## License

I'm including the MIT License here because I always do it.

I didn't check the licenses for the supported packages,
esp. if any of them uses GPL,
and neither do I know if I need to change my license
because I tried to import from them.
Any legal advice is appreciated.

In any case, if you are using this package,
you should check the licenses underlying dependencies yourself
since you'll be using one of them.

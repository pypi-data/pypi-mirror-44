Quick start
===========

This document should help you get up and running with `dataclass_structor`.

Start by installing the package by installation_


Lets say that you have these two dataclasses::

    @dataclasses.dataclass
    class Invite:
        email: str
        guests: typing.List["Guest"]


    @dataclasses.dataclass
    class Guest:
        first_name: typing.Optional[str] = None

You want to be able to put them in a format that you can serialze but you don't
want to have to find an encoder that knows how to deal with all of the various
kinds of attributes in your class.

Lets say that you have an instance `Invite`::

    value_type = Invite(
        email="testing",
        guests=[
          Guest(first_name="John"),
          Guest(),
        ],
    )

This value type is what youy want to pass between layers of your system,
however when you get to an edge (e.g. A cache, or responding to a request) you
will need to convert it to a format that other systems can use. This is where
`unstructure` comes in::

    x = unstructure(value_type)
    # `x` is a value that we could either put in the cache or return to a user
    assert x == {"email": "", "guests": [{"first_name": "John"}, {"first_name": None}]}

`unstructure` returns a dictionary composed of types that are serializeable
with the default `json.dumps` (i.e. without having to specify an encoder)

If we had used `unstructure` to put something into the cache, we will want to
be able to put it back into a format that we can pass between methods after we
get it out of the cache. This is where `sturcture` comes in::

    assert structure(x, Invite) == value_type

`structure` takes a dictionary and a type and will attempt to convert the
dictionary into the given type.

import itertools
from typing import Any, Dict, Tuple


def merge_args_and_kwargs(
    event_abi: Dict[str, Any], args: Any, kwargs: Any
) -> Tuple[Any, ...]:
    """
    Borrowed / modified from
    https://github.com/ethereum/web3.py/blob/master/web3/_utils/abi.py
    """
    if len(args) + len(kwargs) > len(event_abi.get("inputs", [])):
        raise TypeError(
            "Incorrect argument count.  Expected <= '{0}'.  Got '{1}'".format(
                len(event_abi["inputs"]), len(args) + len(kwargs)
            )
        )

    if not kwargs and not args:
        raise TypeError("No kwargs or args provided.")

    if not kwargs:
        return args

    args_as_kwargs = {
        arg_abi["name"]: arg for arg_abi, arg in zip(event_abi["inputs"], args)
    }
    duplicate_keys = set(args_as_kwargs).intersection(kwargs.keys())
    if duplicate_keys:
        raise TypeError(
            "{fn_name}() got multiple values for argument(s) '{dups}'".format(
                fn_name=event_abi["name"], dups=", ".join(duplicate_keys)
            )
        )

    sorted_arg_names = [arg_abi["name"] for arg_abi in event_abi["inputs"]]

    unknown_kwargs = {key for key in kwargs.keys() if key not in sorted_arg_names}
    if unknown_kwargs:
        if event_abi.get("name"):
            raise TypeError(
                "{fn_name}() got unexpected keyword argument(s) '{dups}'".format(
                    fn_name=event_abi.get("name"), dups=", ".join(unknown_kwargs)
                )
            )
        # show type instead of name in the error message incase key 'name' is missing.
        raise TypeError(
            "Type: '{_type}' got unexpected keyword argument(s) '{dups}'".format(
                _type=event_abi.get("type"), dups=", ".join(unknown_kwargs)
            )
        )

    sorted_args = list(
        zip(
            *sorted(
                itertools.chain(kwargs.items(), args_as_kwargs.items()),
                key=lambda kv: sorted_arg_names.index(kv[0]),
            )
        )
    )
    if sorted_args:
        return sorted_args[1]
    else:
        return tuple()

"""Description compilation."""

from collections.abc import Mapping

from preacher.core.description import Description
from .error import CompilationError
from .predicate import compile as compile_predicate
from .extraction import compile as compile_extraction
from .util import run_on_key, map_on_key


_KEY_DESCRIBE = 'describe'
_KEY_IT = 'it'


def compile(obj: Mapping) -> Description:
    """
    >>> from unittest.mock import patch, sentinel
    >>> extraction_patch = patch(
    ...     f'{__name__}.compile_extraction',
    ...     return_value=sentinel.extraction,
    ... )
    >>> predicate_patch = patch(
    ...     f'{__name__}.compile_predicate',
    ...     return_value=sentinel.predicate,
    ... )

    >>> compile({})
    Traceback (most recent call last):
        ...
    preacher.compilation.error.CompilationError: Description.describe ...

    >>> with extraction_patch as extraction_mock, \\
    ...      predicate_patch as predicate_mock:
    ...     description = compile({
    ...         'describe': 'foo',
    ...         'it': 'string',
    ...     })
    ...     extraction_mock.assert_called_with({'jq': 'foo'})
    ...     predicate_mock.assert_called_once_with('string')
    >>> description.extraction
    sentinel.extraction
    >>> description.predicates
    [sentinel.predicate]

    >>> with extraction_patch as extraction_mock, \\
    ...      predicate_patch as predicate_mock:
    ...     description = compile({
    ...         'describe': 'foo',
    ...         'it': {'key': 'value'}
    ...     })
    ...     extraction_mock.call_args
    ...     predicate_mock.call_args_list
    call({'jq': 'foo'})
    [call({'key': 'value'})]
    >>> description.extraction
    sentinel.extraction
    >>> description.predicates
    [sentinel.predicate]

    >>> with extraction_patch as extraction_mock, \\
    ...      predicate_patch as predicate_mock:
    ...     description = compile({
    ...         'describe': {'key': 'value'},
    ...         'it': [{'key1': 'value1'}, {'key2': 'value2'}]
    ...     })
    ...     extraction_mock.call_args
    ...     predicate_mock.call_args_list
    call({'key': 'value'})
    [call({'key1': 'value1'}), call({'key2': 'value2'})]
    >>> description.extraction
    sentinel.extraction
    >>> description.predicates
    [sentinel.predicate, sentinel.predicate]
    """
    extraction_obj = obj.get(_KEY_DESCRIBE)
    if isinstance(extraction_obj, str):
        extraction_obj = {'jq': extraction_obj}  # HACK: move
    if not isinstance(extraction_obj, Mapping):
        raise CompilationError(
            message='Description.describe must be a mapping',
            path=[_KEY_DESCRIBE],
        )
    extraction = run_on_key(_KEY_DESCRIBE, compile_extraction, extraction_obj)

    predicate_objs = obj.get(_KEY_IT, [])
    if not isinstance(predicate_objs, list):
        predicate_objs = [predicate_objs]
    predicates = list(map_on_key(_KEY_IT, compile_predicate, predicate_objs))

    return Description(extraction=extraction, predicates=predicates)

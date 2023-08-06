from pytest import mark, raises

from loggingex.context import (
    ContextChange,
    ContextChangeAlreadyStartedException,
    ContextChangeNotStartedException,
    ContextInvalidNameException,
)
from .helpers import InitializedContextBase


def test_default_constructor_initializes_context_changes():
    change = ContextChange()
    assert change.context_fresh is False
    assert change.context_remove == set()
    assert change.context_update == {}
    assert change.context_restore_token is None


@mark.parametrize("value", [None, 1337, 13.37, b"bytes", [], {}, set(), ()])
def test_validate_context_variable_name_raises_when_not_a_string(value):
    assert raises(
        ContextInvalidNameException,
        ContextChange.validate_context_variable_name,
        value,
    )


@mark.parametrize("value", ["?", "!", "foo.bar", "foo bar", "foo-bar"])
def test_validate_context_variable_name_raises_when_not_identifier(value):
    assert raises(
        ContextInvalidNameException,
        ContextChange.validate_context_variable_name,
        value,
    )


@mark.parametrize("value", ["foo", "foo_bar", "fooBar", "_foo", "bar_"])
def test_validate_context_variable_name_passes_when_name_is_valid(value):
    ContextChange.validate_context_variable_name(value)


def test_validate_context_variable_names_validates_each_name(mocker):
    names = ["foo", "foo_bar", "fooBar", "_foo", "bar_"]
    with mocker.spy(ContextChange, "validate_context_variable_name"):
        ContextChange.validate_context_variable_names(names)
        spy = ContextChange.validate_context_variable_name
        assert spy.call_count == len(names)
        for name in names:
            assert spy.called_with(name)


def test_started_returns_false_when_token_is_not_assigned():
    change = ContextChange()
    assert change.started is False


def test_started_returns_true_when_token_is_assigned():
    change = ContextChange(context_restore_token="not a None")
    assert change.started is True


def test_can_change_returns_true_when_token_is_not_assigned():
    change = ContextChange()
    assert change.can_change() is True


def test_can_change_returns_true_when_token_is_not_assigned_with_raise():
    change = ContextChange()
    assert change.can_change(raise_on_fail=True) is True


def test_can_change_raises_when_token_is_assigned_with_raise():
    change = ContextChange(context_restore_token="not a None")
    assert raises(
        ContextChangeAlreadyStartedException,
        change.can_change,
        raise_on_fail=True,
    )


@mark.parametrize("value", [True, False])
def test_fresh_changes_context_fresh(value):
    change = ContextChange(context_fresh=not value)
    assert change.context_fresh is not value
    change.fresh(value)
    assert change.context_fresh is value


def test_fresh_raises_when_token_is_assigned():
    change = ContextChange(context_restore_token="not a None")
    assert raises(ContextChangeAlreadyStartedException, change.fresh, True)


@mark.parametrize(
    "init,update,result",
    [
        (None, {"foo", "bar"}, {"foo", "bar"}),
        ({"foo"}, {"bar"}, {"foo", "bar"}),
        ({"foo"}, {"foo", "bar"}, {"foo", "bar"}),
    ],
)
def test_remove_updates_context_remove_set(init, update, result):
    change = ContextChange(context_remove=init)
    change.remove(*update)
    assert change.context_remove == result


def test_remove_raises_when_token_is_assigned():
    change = ContextChange(context_restore_token="not a None")
    assert raises(ContextChangeAlreadyStartedException, change.remove, "foo")


@mark.parametrize("name", [None, 1, "foo-bar", "with space"])
def test_remove_raises_when_name_is_not_valid(name):
    change = ContextChange()
    assert raises(ContextInvalidNameException, change.remove, name)


@mark.parametrize(
    "init,update,result",
    [
        (None, {"foo": "bar"}, {"foo": "bar"}),
        ({"foo": 1}, {"bar": 2}, {"foo": 1, "bar": 2}),
        ({"foo": 1}, {"foo": 2, "bar": 4}, {"foo": 2, "bar": 4}),
    ],
)
def test_update_extends_context_update_dict(init, update, result):
    change = ContextChange(context_update=init)
    change.update(**update)
    assert change.context_update == result


def test_update_raises_when_token_is_assigned():
    change = ContextChange(context_restore_token="not a None")
    assert raises(ContextChangeAlreadyStartedException, change.update, foo=1)


@mark.parametrize("name", ["foo-bar", "with space"])
def test_update_raises_when_name_is_not_valid(name):
    change = ContextChange()
    assert raises(ContextInvalidNameException, change.update, **{name: 1})


def test_apply_returns_same_dict_when_no_changes():
    change = ContextChange()
    assert change.apply({"foo": 1}) == {"foo": 1}


def test_apply_removes_variables():
    change = ContextChange().remove("foo")
    assert change.apply({"foo": 1}) == {}


def test_apply_replaces_variables():
    change = ContextChange().update(foo=2)
    assert change.apply({"foo": 1}) == {"foo": 2}


def test_apply_starts_fresh_when_fresh():
    change = ContextChange().fresh().update(bar=1)
    assert change.apply({"foo": 1}) == {"bar": 1}


def test_apply_combines_removes_and_updates():
    change = ContextChange().remove("foo", "bar").update(baz=1337, new=True)
    initial = {"foo": 1, "baz": 2, "old": "yes"}
    expected = {"old": "yes", "baz": 1337, "new": True}
    assert change.apply(initial) == expected


class StartAndStopTests(InitializedContextBase):
    def test_start_applies_context_change_and_saves_token(self, store):
        change = ContextChange().update(foo=1, bar=2.3, baz=True)
        change.start()
        assert change.started is True
        assert change.context_restore_token is not None
        assert store.get() == {"foo": 1, "bar": 2.3, "baz": True}

    def test_start_raises_when_change_already_started(self):
        change = ContextChange(context_restore_token="not a None")
        assert raises(ContextChangeAlreadyStartedException, change.start)

    def test_stop_restores_context_and_clears_token(self, store):
        change = ContextChange(
            context_update={"foo": 1},
            context_restore_token=store.replace({"foo": 1}),
        )
        change.stop()
        assert change.started is False
        assert change.context_restore_token is None
        assert store.get() == {}

    def test_stop_raises_when_change_was_not_started(self):
        change = ContextChange(context_update={"foo": 1})
        assert raises(ContextChangeNotStartedException, change.stop)


class ContextChangeAsContextManagerTests(InitializedContextBase):
    def test_can_be_used_as_context_manager(self, store):
        with ContextChange().update(foo=1, bar=2.3):
            assert store.get() == {"foo": 1, "bar": 2.3}
        assert store.get() == {}

    def test_context_manager_does_not_swallow_exceptions(self):
        exception_raised = False
        try:
            with ContextChange().update(foo=1):
                raise ValueError("test")
        except ValueError:
            exception_raised = True
        assert exception_raised


class ContextChangeAsDecoratorTests(InitializedContextBase):
    def test_can_be_used_as_decorator(self, store):
        change = ContextChange().update(func="foo")

        @change
        def foo(a, b, c, d, e, f):
            assert store.get() == {"func": "foo"}
            return a + b + c + d + e + f

        assert foo(1, 2, 3, 4, 5, 6) == 21
        assert store.get() == {}

    def test_decorator_does_not_swallow_exceptions(self):
        change = ContextChange().update(func="foo")

        @change
        def foo():
            raise ValueError("test")

        exception_raised = False
        try:
            foo()
        except ValueError:
            exception_raised = True
        assert exception_raised

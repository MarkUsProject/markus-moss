import pytest
from unittest.mock import patch
from contextlib import ExitStack
from markus_moss import MarkusMoss


@pytest.fixture
def action_patches():
    with ExitStack() as stack:
        actions = {}
        for action in MarkusMoss.ACTIONS:
            actions[action] = stack.enter_context(patch.object(MarkusMoss, action))
        yield actions


class TestRun:
    def test_run_no_args(self, action_patches):
        MarkusMoss().run()
        assert all([p.called for p in action_patches.values()])

    def test_run_valid_action(self, action_patches):
        actions = ["download_starter_files", "run_moss"]
        MarkusMoss().run(actions=actions)
        assert all([p.called for a, p in action_patches.items() if a in actions])
        assert not any([p.called for a, p in action_patches.items() if a not in actions])

    def test_run_invalid_action(self):
        actions = ["this_is_not_an_option"]
        with pytest.raises(AttributeError):
            MarkusMoss().run(actions=actions)

# TODO: finish tests

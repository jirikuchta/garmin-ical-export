import pytest

from garminicalexport import cmd


def parse(argv):
    return cmd.build_parser().parse_args(argv)


def test_resolve_credentials_from_args():
    args = parse(["me@example.com", "hunter2"])
    parser = cmd.build_parser()
    assert cmd.resolve_credentials(args, parser) == ("me@example.com", "hunter2")


def test_resolve_credentials_from_env_vars(monkeypatch):
    monkeypatch.setenv(cmd.EMAIL_ENV_VAR, "env@example.com")
    monkeypatch.setenv(cmd.PASSWORD_ENV_VAR, "env-password")
    args = parse([])
    parser = cmd.build_parser()
    assert cmd.resolve_credentials(args, parser) == ("env@example.com", "env-password")


def test_args_take_priority_over_env_vars(monkeypatch):
    monkeypatch.setenv(cmd.EMAIL_ENV_VAR, "env@example.com")
    monkeypatch.setenv(cmd.PASSWORD_ENV_VAR, "env-password")
    args = parse(["arg@example.com", "arg-password"])
    parser = cmd.build_parser()
    assert cmd.resolve_credentials(args, parser) == ("arg@example.com", "arg-password")


def test_resolve_credentials_prompts_when_interactive(monkeypatch):
    monkeypatch.delenv(cmd.EMAIL_ENV_VAR, raising=False)
    monkeypatch.delenv(cmd.PASSWORD_ENV_VAR, raising=False)
    monkeypatch.setattr(cmd.sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda prompt="": "prompted@example.com")
    monkeypatch.setattr(cmd.getpass, "getpass", lambda prompt="": "prompted-password")

    args = parse([])
    parser = cmd.build_parser()
    assert cmd.resolve_credentials(args, parser) == (
        "prompted@example.com", "prompted-password")


def test_resolve_credentials_errors_when_missing_and_non_interactive(monkeypatch):
    monkeypatch.delenv(cmd.EMAIL_ENV_VAR, raising=False)
    monkeypatch.delenv(cmd.PASSWORD_ENV_VAR, raising=False)
    monkeypatch.setattr(cmd.sys.stdin, "isatty", lambda: False)

    args = parse([])
    parser = cmd.build_parser()
    with pytest.raises(SystemExit):
        cmd.resolve_credentials(args, parser)

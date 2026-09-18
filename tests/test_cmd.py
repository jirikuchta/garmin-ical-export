import pytest

from garminicalexport import cmd


def parse(argv):
    return cmd.build_parser().parse_args(argv)


def test_resolve_credentials_email_from_arg_password_from_env(monkeypatch):
    monkeypatch.setenv(cmd.PASSWORD_ENV_VAR, "env-password")
    args = parse(["me@example.com"])
    parser = cmd.build_parser()
    assert cmd.resolve_credentials(args, parser) == ("me@example.com", "env-password")


def test_resolve_credentials_from_env_vars(monkeypatch):
    monkeypatch.setenv(cmd.EMAIL_ENV_VAR, "env@example.com")
    monkeypatch.setenv(cmd.PASSWORD_ENV_VAR, "env-password")
    args = parse([])
    parser = cmd.build_parser()
    assert cmd.resolve_credentials(args, parser) == ("env@example.com", "env-password")


def test_email_arg_takes_priority_over_env_var(monkeypatch):
    monkeypatch.setenv(cmd.EMAIL_ENV_VAR, "env@example.com")
    monkeypatch.setenv(cmd.PASSWORD_ENV_VAR, "env-password")
    args = parse(["arg@example.com"])
    parser = cmd.build_parser()
    assert cmd.resolve_credentials(args, parser) == ("arg@example.com", "env-password")


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


def test_resolve_credentials_errors_on_empty_interactive_input(monkeypatch):
    monkeypatch.delenv(cmd.EMAIL_ENV_VAR, raising=False)
    monkeypatch.delenv(cmd.PASSWORD_ENV_VAR, raising=False)
    monkeypatch.setattr(cmd.sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda prompt="": "")

    args = parse([])
    parser = cmd.build_parser()
    with pytest.raises(SystemExit):
        cmd.resolve_credentials(args, parser)


def test_password_is_not_a_positional_argument():
    with pytest.raises(SystemExit):
        parse(["me@example.com", "extra-positional"])

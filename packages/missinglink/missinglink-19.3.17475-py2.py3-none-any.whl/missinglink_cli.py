#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
import click
# DON'T PUT HERE ANY MISSINGLINK import directly, use local imports


def main():
    os.environ['MISSINGLINKAI_DISABLE_EXCEPTION_HOOK'] = '1'
    os.environ['MISSINGLINKAI_DISABLE_LOGGING_HOOK'] = '1'

    from missinglink.commands import add_commands, cli
    from missinglink.commands.global_cli import self_update, set_pre_call_hook, setup_sentry_sdk, setup_pre_call
    from missinglink.core.exceptions import MissingLinkException
    from missinglink.legit.gcp_services import GooglePackagesMissing, GoogleAuthError

    setup_sentry_sdk()
    set_pre_call_hook(setup_pre_call)

    if sys.argv[0].endswith('/mali') and not os.environ.get('ML_DISABLE_DEPRECATED_WARNINGS'):
        click.echo('instead of mali use ml (same tool with a different name)', err=True)

    if os.environ.get('MISSINGLINKAI_ENABLE_SELF_UPDATE'):
        self_update()

    add_commands()
    try:
        cli()
    except GooglePackagesMissing:
        click.echo('you to run "pip install missinglink[gcp]" in order to run this command', err=True)
    except GoogleAuthError:
        click.echo('Google default auth credentials not found, run gcloud auth application-default login', err=True)
    except MissingLinkException as ex:
        click.echo(ex, err=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.
# https://realpython.com/installable-django-app/#running-management-commands-with-your-installable-django-app

import argparse
import json
import os
import sys
from inspect import getmembers, isfunction

import django
from django.core.management import call_command

import emoji
import rich

import boot_django
import constants

boot_django.boot()
from tasks.update_db_from_json import init_dbs_from_json  # noqa: E402
from django_cloud_provider_zones.serializers import serialize_azs, serialize_regions  # noqa: E402


def print_status(message, error=False):
    print(
        f"{emoji.emojize(':right_arrow:')} Running on DB:\n  {constants.TEST_DB_PATH}"
    )
    if error:
        print(f"{emoji.emojize(':cross_mark:')} {message}")
    else:
        print(f"{emoji.emojize(':check_mark_button:')} {message}")


def django_createsuperuser():
    """Create a superuser for the Django admin - for testing only of course"""
    username = password = "admin"
    os.environ["DJANGO_SUPERUSER_USERNAME"] = username
    os.environ["DJANGO_SUPERUSER_PASSWORD"] = password
    os.environ["DJANGO_SUPERUSER_EMAIL"] = "admin@example.com"
    print(f"Creating superuser: '{username}' with password '{password}'...")
    try:
        call_command("createsuperuser", "--noinput")
        print_status(f"Superuser created: '{username}' with password '{password}'")
    except django.core.management.base.CommandError as e:
        print_status(f"Superuser not created: {e}", error=True)


def django_update_fixture_from_json():
    """Create Django fixture from the loaded data"""
    django_migrate()
    init_dbs_from_json()
    create_fixture(
        constants.APP_NAME,
        model_name="CloudProvider",
        natural_primary_key=False,
        natural_foreign_key=False,
    )
    create_fixture(
        constants.APP_NAME, model_name="CloudRegion", natural_foreign_key=False
    )
    create_fixture(constants.APP_NAME, model_name="CloudAvailabilityZone")


def create_fixture(
    app_name, model_name=None, natural_primary_key=True, natural_foreign_key=True
):
    if model_name is None:
        fixture_file = constants.FIXTURES_DIR / f"{constants.APP_NAME}.json"
        fixture_target = app_name
    else:
        fixture_file = (
            constants.FIXTURES_DIR / f"{constants.APP_NAME}-{model_name}.json"
        )
        fixture_target = f"{app_name}.{model_name}"
    base_command = [
        "dumpdata",
        "--format",
        "json",
        "--indent",
        "4",
    ]
    if natural_foreign_key:
        base_command.append("--natural-foreign")
    if natural_primary_key:
        base_command.append("--natural-primary")
    cmd = base_command + [
        "--output",
        fixture_file,
        fixture_target,
    ]
    call_command(*cmd)
    print_status(f"Fixture created: {str(fixture_file)} from '{fixture_target}'")


def django_makemigrations():
    call_command("makemigrations")


def django_migrate():
    django_makemigrations()
    call_command("migrate")
    print_status(f"Migrations complete on {constants.TEST_DB_PATH}")


def django_load_fixture():
    django_migrate()
    call_command("loaddata", "--app", constants.APP_NAME, constants.APP_NAME)


def django_runserver():
    django_load_fixture()
    django_createsuperuser()
    call_command("runserver")


def django_test():
    call_command("test", "django_cloud_provider_zones")


def django_shell():
    call_command("shell_plus")


def django_serialize_regions():
    rich.print_json(json.dumps(serialize_regions()))


def django_serialize_azs():
    rich.print_json(json.dumps(serialize_azs()))


def django_graph_models():
    # this doesn't work here but works in a normal Django shell
    png_file = constants.PROJECT_ROOT_DIR / "django_models.png"
    call_command("graph_models", "django_cloud_provider_zones", "-g", "-o", png_file)
    # --rankdir BT --theme django2018 -l twopi
    print_status(f"Model graph created: {str(png_file)}")


if __name__ == "__main__":
    commands = set()
    for name, obj in getmembers(sys.modules[__name__]):
        if isfunction(obj):
            if "django_" in name:
                commands.add(name)
    commands = sorted(commands)

    help_text = "Command required:\n " + "\n ".join(commands)

    parser = argparse.ArgumentParser(description="Run Django management commands")
    parser.add_argument("command", help=help_text)
    args = parser.parse_args()
    if args.command not in commands:
        print_status(help_text, error=True)
    else:
        globals()[args.command]()

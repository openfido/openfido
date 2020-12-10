import argparse
import json
import logging
import posix
import requests
import sys

from . import schemas, services

logger = logging.getLogger('openfido.script')


def main():
    parser = argparse.ArgumentParser(
        description="Interract with openFIDO services"
    )

    parser.add_argument(
        '--log', '-l', default="WARN",
        help="Log level (default: WARN)")

    parser.add_argument(
        '--app-service', '-ss', default="https://api-staging.openfido.org",
        help="App API URL")

    parser.add_argument(
        '--auth-service', '-as', default="https://auth-staging.openfido.org",
        help="Auth API URL")

    parser.add_argument('--email', '-e', help="OpenFIDO email", required=True)
    parser.add_argument('--password', '-p', help="OpenFIDO password", required=True)
    parser.add_argument('--app-key', '-ak', help="OpenFIDO App API application token", required=True)

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    workflow_parser = subparsers.add_parser(
        'workflow', help='Manage Workflows',
        description='Create and monitory workflows.')
    workflow_subparsers = workflow_parser.add_subparsers(help='workflow commands', dest='subcommand')

    view_workflow_parser = workflow_subparsers.add_parser(
        'view', help='View a Workflow',
        description='View a Workflow.')
    view_workflow_parser.add_argument('uuid', type=str, help="Workflow UUID")

    create_workflow_parser = workflow_subparsers.add_parser(
        'create', help='Create a Workflow',
        description='Create a new Workflow.')
    create_workflow_parser.add_argument('json_file', type=argparse.FileType('r'), help="Workflow JSON definition.")

    update_workflow_parser = workflow_subparsers.add_parser(
        'update', help='Update a Workflow',
        description='Update an existing Workflow.')
    # TODO enforce str is a UUID
    update_workflow_parser.add_argument('uuid', type=str, help="Workflow UUID")
    update_workflow_parser.add_argument('json_file', type=argparse.FileType('r'), help="Workflow JSON definition.")

    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log))

    if not args.command or not args.subcommand:
        print('You must supply a command. See --help for more information')
        sys.exit(posix.EX_USAGE)

    logger.debug(args)

    app_session = requests.Session()
    app_session.headers['Workflow-API-Key'] = args.app_key
    auth_session = requests.Session()
    auth_session.headers['Workflow-API-Key'] = args.app_key

    services.login(auth_session, app_session, args.auth_service, args.email, args.password)

    if args.command == 'workflow':
        if args.subcommand == 'view':
            return services.view_workflow(app_session, args.app_service, args.uuid)
        if args.subcommand == 'create':
            json_data = json.load(args.json_file)
            create_workflow_data = schemas.CreateWorkflowSchema().load(json_data)
            return services.create_workflow(app_session, args.app_service, create_workflow_data)
        elif args.subcommand == 'update':
            json_data = json.load(args.json_file)
            create_workflow_data = schemas.CreateWorkflowSchema().load(json_data)
            return services.update_workflow(app_session, args.app_service, args.uuid, create_workflow_data)

    print('Unknown command or subcommand supplied. See --help for usage.')
    sys.exit(posix.EX_USAGE)

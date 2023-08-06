import click
import requests
import time
import sys

from requests.auth import HTTPBasicAuth

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

def report_teamcity_test_run(test_run):
    if test_run['status'] == 'FAIL':
        print("##teamcity[buildProblem description='%s: %s passing, %s failing out of %s total']" % (test_run['status'], test_run['passCount'], test_run['failCount'], test_run['totalCount']))
    else:
        print("##teamcity[buildStatus text='%s: %s passing, %s failing out of %s total']" % (test_run['status'], test_run['passCount'], test_run['failCount'], test_run['totalCount']))


def api_wait_test_run(api_url, username, token, test_run_id, output, fail_on_failure):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    test_run = requests.get(api_url + '/test-run-results/' + str(test_run_id), auth=HTTPBasicAuth(username, token), headers=headers).json()

    while test_run['status'] not in ['PASS','FAIL']:

        test_run = requests.get(api_url + '/test-run-results/' + str(test_run_id), auth=HTTPBasicAuth(username, token), headers=headers).json()
        print(test_run)
        report_teamcity_test_run(test_run)
        time.sleep(10);

    if output == "teamcity":
        report_teamcity_test_run(test_run)
    else:
        print(test_run)

    if test_run['status'] == 'FAIL' and fail_on_failure:
        sys.exit(1);


@click.group()
def cli():
    """
    Testery CLI\n
    Kick off test runs from your CI/CD platform and run them on Testery's next-generation, cloud-based testing grid.
    """
    pass

@click.command('verify-token')
@click.option('--api-url', default='https://api.testery.io/api', help='The URL for the Testery API. Only required for development purposes.')
@click.option('--username', help='Your Testery username.')
@click.option('--token', help='Your Testery API token.')
def verify_token(api_url, username, token):
    """
    Verifies your username and authentication token are valid.
    """

    response = requests.get(api_url + '/users/me', auth=HTTPBasicAuth(username, token))

    print(response.json())

@click.command('create-test-run-platform')
@click.option('--api-url', default='https://api.testery.io/api', help='The URL for the Testery API. Only required for development purposes.')
@click.option('--username', help='Your Testery username.')
@click.option('--token', help='Your Testery API token.')
@click.option('--suite-id', help='The suite id to run.')
@click.option('--wait-for-results', is_flag=True, help='If set, the command will poll until the test run is complete.')
@click.option('--output', default='json', help='The format for outputting results [json,pretty,teamcity,appveyor]')
@click.option("--fail-on-failure", is_flag=True, help='When set, the testery command will return exit code 1 if there are test failures.')
def create_test_run_platform(api_url, username, token, suite_id, wait_for_results, output, fail_on_failure):
    """
    Creates a platform-based (non-git) test run.
    """

    test_run_request = {"copies": 1, "suites": [{"id": suite_id}]}

    test_run = requests.post(api_url + '/test-run-requests',
                             auth=HTTPBasicAuth(username, token),
                             headers=headers,
                             json=test_run_request).json()

    print(test_run)

    test_run_id = str(test_run['id'])

    click.echo("Test run submitted with id: %s" %test_run_id)

    if wait_for_results:
        api_wait_test_run(api_url, username, token, test_run_id, output, fail_on_failure)


@click.command('create-test-run')
@click.option('--api-url', default='https://api.testery.io/api', help='The URL for the Testery API. Only required for development purposes.')
@click.option('--username', help='Your Testery username.')
@click.option('--token', help='Your Testery API token.')
@click.option('--git-org', help='Your git organization name.')
@click.option('--git-repo', help='Your git repository name.')
@click.option('--git-ref', help='The git commit hash of the build being tested.')
@click.option('--wait-for-results', is_flag=True, help='If set, the command will poll until the test run is complete.')
@click.option('--project', help='A unique identifier for your project.')
@click.option('--environment', help='Which environment you would like to run your tests against.')
@click.option('--build-id', help='A unique identifier that identifies this build in your system.')
@click.option('--output', default='json', help='The format for outputting results [json,pretty,teamcity,appveyor]')
@click.option("--fail-on-failure", is_flag=True, help='When set, the testery command will return exit code 1 if there are test failures.')
def create_test_run(api_url, username, token, git_org, git_repo, git_ref, wait_for_results, output, project, environment, build_id, fail_on_failure):
    """
    Submits a Git-based test run to the Testery platform.
    """
    test_run_request = {"owner":git_org, "repository":git_repo, "ref":git_ref, "project":project, "environment":environment, "buildId":build_id}

    test_run = requests.post(api_url + '/test-run-requests-build',
         auth=HTTPBasicAuth(username, token),
         headers=headers,
         json=test_run_request).json()

    print(test_run)

    test_run_id = str(test_run['id'])

    click.echo("test_run_id: %s" %test_run_id)

    if wait_for_results:
        api_wait_test_run(api_url, username, token, test_run_id, output, fail_on_failure)


@click.command('monitor-test-run')
@click.option('--api-url', default='https://api.testery.io/api', help='The URL for the Testery API. Only required for development purposes.')
@click.option('--username', help='Your Testery username.')
@click.option('--token', help='Your Testery API token.')
@click.option('--test-run-id', help='The ID for the test run you would like to monitor and wait for.')
@click.option("--fail-on-failure", is_flag=True, help='When set, the testery command will return exit code 1 if there are test failures.')
@click.option('--output', default='json', help='The format for outputting results [json,pretty,teamcity,appveyor]')
def monitor_test_run(api_url, username, token, test_run_id, output, fail_on_failure):
    api_wait_test_run(api_url, username, token, test_run_id, output, fail_on_failure)


cli.add_command(create_test_run)
cli.add_command(create_test_run_platform)
cli.add_command(monitor_test_run)
cli.add_command(verify_token)

if __name__ == '__main__':
    cli()
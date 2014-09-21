from os import system
from os.path import join, abspath
from pulsar.daemon import ArgumentParser, PulsarConfigBuilder

DESCRIPTION = "Change ownership of a job working directory."
# Switch this to true to tighten up security somewhat in production mode,
# better increase of security can be had by simply restricting sudoers rule
# to only allow chown -R of directories of form ${staging_directory}/${job_id}
FORCE_PRODUCTION = False


def main():
    arg_parser = ArgumentParser(description=DESCRIPTION)
    arg_parser.add_argument("--user", required=True)
    arg_parser.add_argument("--job_id")
    arg_parser.add_argument("--job_directory")
    args = arg_parser.parse_args()
    user = args.user
    job_id = args.job_id

    if args.job_id:
        staging_directory = PulsarConfigBuilder().load()['staging_directory']
        job_directory = abspath(join(staging_directory, job_id))
        assert job_directory.startswith(staging_directory)
    elif FORCE_PRODUCTION:
        raise Exception("In production mode, must specify a job_id instead of a working directory.")
    else:
        job_directory = abspath(args.job_directory)
        assert job_directory
    command = "chown -R '%s' '%s'" % (user, job_directory)
    system(command)

if __name__ == "__main__":
    main()

import click
import logging, coloredlogs
from conu import DockerRunBuilder, DockerBackend, ConuException
from termcolor import colored

import os
import sys

coloredlogs.install(level='DEBUG')

# usage:
#python3 soit/main.py --image quay.io/jkremser/openshift-spark --tag 2.4.0

@click.command()
@click.option('--image', '-i', prompt='container image', help='Container image with Spark.')
@click.option('--tag', '-t', prompt='tag', default='latest', help='Specific tag of the image.')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output.')
@click.option('--full', '-f', is_flag=True, help='Full mode including spawning master and worker and testing if they can connect.')
@click.option('--silent', '-s', is_flag=True, help='Do not output anything to standard output.')
def check(image, tag, verbose, full, silent):
    """Simple verification tool that check the compatibility with Spark Operator"""

    logging_level = logging.DEBUG if verbose else logging.ERROR
    logging.getLogger("urllib3").setLevel(logging_level)
    logging.getLogger("docker").setLevel(logging_level)

    if silent:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    with DockerBackend(logging_level=logging_level) as backend:
        results = {}

        # the image will be pulled if it's not present
        try:
            i = backend.ImageClass(image, tag=tag)
        except ConuException:
            print('Ubable to pull image: %s:%s' % (image, tag))
            exit(1)

        run_params = DockerRunBuilder(additional_opts=['--entrypoint', ''], command=['sleep', '3600'])
        container = i.run_via_binary(run_params)

        assert container.is_running(), "Container must be running"
        try:
            with container.mount() as fs:
                if os.path.lexists(fs.p('/opt/spark')):
                    resolved_spark_home = os.readlink(fs.p('/opt/spark'))
                else:
                    resolved_spark_home = '/opt/spark'

                launch_script_is_present = fs.file_is_present('/launch.sh') or fs.file_is_present(resolved_spark_home + '/bin/launch.sh')
                results["launch_script_is_present"] = {"result": launch_script_is_present, "message": "File /launch.sh should be present on the image"}

                if launch_script_is_present:
                    launch_script = fs.read_file('/launch.sh') if fs.file_is_present('/launch.sh') else fs.read_file(resolved_spark_home + '/bin/launch.sh')
                    metrics_support = 'SPARK_METRICS_ON' in launch_script
                    master_address_support = 'SPARK_MASTER_ADDRESS' in launch_script
                else:
                    metrics_support = master_address_support = False

                results["metrics_support"] = {"result": metrics_support, "message": "File /launch.sh does contain SPARK_METRICS_ON"}
                results["master_address_support"] = {"result": master_address_support, "message": "File /launch.sh does contain SPARK_MASTER_ADDRESS"}

                entrypoint_present = fs.file_is_present('/entrypoint')
                results["entrypoint_present"] = {"result": entrypoint_present, "message": "File /entrypoint should be present on the image"}

                spark_home_present = fs.directory_is_present(resolved_spark_home)
                results["spark_home_present"] = {"result": spark_home_present, "message": "Directory /opt/spark should be present on the image"}

                if spark_home_present:
                    config_directory_present = fs.directory_is_present(resolved_spark_home + '/conf')
                    default_config_present = config_directory_present and fs.file_is_present(resolved_spark_home + '/conf/spark-defaults.conf')
                    spark_class_present = fs.file_is_present(resolved_spark_home + '/bin/spark-class')
                    release_file_present = fs.file_is_present(resolved_spark_home + '/RELEASE')
                    if release_file_present:
                        release = fs.read_file(resolved_spark_home + '/RELEASE') + "\n"
                else:
                    config_directory_present = default_config_present = spark_class_present = release_file_present = False

                results["config_directory_present"] = {"result": config_directory_present, "message": "Directory /opt/spark/conf/ is present on the image"}
                results["default_config_present"] = {"result": default_config_present, "message": "Default config spark-defaults.conf is on the right place"}
                results["spark_class_present"] = {"result": spark_class_present, "message": "File /opt/spark/bin/spark-class should be present on the image"}
                results["release_file_present"] = {"result": release_file_present, "message": "File /opt/spark/RELEASE should be present on the image"}

                curl_output = container.execute(["curl", "--help"], blocking=False)
                curl_installed = 'Usage: curl' in (b'\n'.join(curl_output)).decode("utf-8")
                results["curl_installed"] = {"result": curl_installed, "message": "The image should have the curl installed"}

                bash_output = container.execute(["bash", "-c", "echo Spark rocks!"], blocking=False)
                bash_output = 'Spark rocks!' in (b'\n'.join(bash_output)).decode("utf-8")
                results["bash_output"] = {"result": bash_output, "message": "The image should have the bash installed"}            
        finally:
            container.kill()
            container.delete()

        if full:
            e2e_case(i, results)

        print_result(results)

        if release_file_present:
            print(colored("Apache Spark info:", "yellow"))
            print(release)

def e2e_case(i, results):
    # run master
    master = i.run_via_binary()
    master_started = master.is_running()
    results["master_started"] = {"result": master_started, "message": "It should be possible to start the master."}

    master.wait_for_port(8080, timeout=15)
    http_response = master.http_request(path="/json", port=8080)
    master_http_ok = http_response.ok
    results["master_http_ok"] = {"result": master_http_ok, "message": "Master should start the web ui on port 8080"}

    master_alive = 'ALIVE' in http_response.content.decode("utf-8")
    results["master_alive"] = {"result": master_alive, "message": "Master should be alive."}

    if master_started and master.get_IPv4s():
        master_ip = master.get_IPv4s()[0]
        # run worker
        run_params_worker = DockerRunBuilder(additional_opts=['-e', 'SPARK_MASTER_ADDRESS=' + master_ip + ':7077', '-e', 'SPARK_MASTER_UI_ADDRESS=http://' + master_ip + ':8080'])
        worker = i.run_via_binary(run_params_worker)
        worker_started = worker.is_running()
        results["worker_started"] = {"result": worker_started, "message": "It should be possible to start the worker."}
        worker.wait_for_port(8081, timeout=15)

        http_response = worker.http_request(path="/json", port=8081)
        worker_http_ok = http_response.ok
        results["worker_http_ok"] = {"result": worker_http_ok, "message": "Worker should start the web ui on port 8081"}

        worker_registered_web_ui = 'spark://%s:7077' % master_ip in http_response.content.decode("utf-8")
        results["worker_registered_web_ui"] = {"result": worker_registered_web_ui, "message": "Worker web ui should contain the master's ip"}

        worker_registered_logs = 'Registering worker' in (b'\n'.join(master.logs())).decode("utf-8")
        results["worker_registered_logs"] = {"result": worker_registered_logs, "message": "In the master's log file there should be worker registration message"}

        master_registered_logs = 'registered with master' in (b'\n'.join(worker.logs())).decode("utf-8")
        results["master_registered_logs"] = {"result": master_registered_logs, "message": "In the worker's log file master registration should be mentioned"}

def print_result(results):
    all_ok = all(map(lambda r: r["result"], results.values()))
    if all_ok:
        print("Radley approves!")
        import os
        f = open(os.path.join(os.path.dirname(__file__), 'radley.ascii'), 'r')
        for line in f:
            print(line, end='')
    else:
        print("\nThe image is not spark-operator compatible 👎")
        exit(1)

    print("\n%s" % colored("RESULTS:", "yellow"))
    for key in results:
        print("[ %s ] ... %s" % (colored("✓", "green") if results[key]["result"] else colored("✕", "red"), results[key]["message"]))
    print("\n")

if __name__ == '__main__':
    check()

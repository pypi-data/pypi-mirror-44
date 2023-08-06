# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# The cli wrapper for experiment commands. This wrapper is base_sdk_common across
# azure.cli and azureml._cli.
# TODO: Not sure if we need to use correlation_id for azureml._cli
import json
import os
from time import sleep

from azureml._base_sdk_common.common import set_correlation_id, CLICommandOutput
from azureml.core.script_run import ScriptRun
from azureml.core.script_run_config import ScriptRunConfig
from azureml.core import Experiment, Run, is_compute_target_prepared
from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core import prepare_compute_target
from azureml.exceptions import UserErrorException
from azureml._project.project import Project
from ._common import get_cli_specific_auth, get_cli_specific_output, get_workspace_or_default, \
    _parse_key_values


# CLI Command handler functions:
#
# Note: The function argument names in each of the CLI command
# handler functions should match with azureml._cli.argument.Argument.function_arg_name


# In the CLI command handler functions, the positional arguments are the required CLI parameters
# and key-based are the optional parameters.

def prepare_run(run_configuration,
                project=".", conda_dependencies=None, spark_dependencies=None, untracked=None,
                run_async=None, target=None, wait=False, check=False):
    """
    Prepares a target.
    :param run_configuration:
    :param project:
    :param conda_dependencies:
    :param spark_dependencies:
    :param untracked:
    :param run_async:
    :param target:
    :param wait:
    :param check:
    :return:
    """

    # TODO: User specified run_id, wait and check is not yet supported.
    # Set correlation id
    set_correlation_id()

    # TODO: Need to replace project="." with None and check here.
    auth = get_cli_specific_auth()
    project_object = Project(auth=auth, directory=project)

    run_config_object = RunConfiguration.load(project_object.project_directory, run_configuration)

    if conda_dependencies:
        run_config_object.environment.python.conda_dependencies_file = conda_dependencies
        run_config_object.environment.python.conda_dependencies = CondaDependencies(
            os.path.join(project_object.project_directory, conda_dependencies))

    if spark_dependencies:
        RunConfiguration._modify_runconfig_using_spark_config(spark_dependencies,
                                                              run_config_object, project_object.project_directory)

    if target:
        run_config_object.target = target

    run_config_object.history.output_collection = not untracked

    if check:
        experiment = Experiment(project_object.workspace, project_object.history.name)
        is_prepared = is_compute_target_prepared(
            experiment=experiment, source_directory=project, run_config=run_config_object)
        command_output = CLICommandOutput("")
        if is_prepared:
            command_output.append_to_command_output("The compute target already prepared for the specified "
                                                    "run configuration.")
        else:
            command_output.append_to_command_output("The compute target is not prepared for the specified "
                                                    "run configuration.")

        command_output.set_do_not_print_dict()
        return get_cli_specific_output(command_output)
    else:
        experiment = Experiment(project_object.workspace, project_object.history.name)
        run_object = prepare_compute_target(
            experiment=experiment, source_directory=project, run_config=run_config_object)

        if not run_async:
            run_object.wait_for_completion(show_output=True, wait_post_processing=wait)
        else:
            command_output = CLICommandOutput("")
            command_output.append_to_command_output("RunId:" + run_object.id)
            azureml_cli_output = {"RunId": run_object.id}
            command_output.merge_dict(azureml_cli_output)
            command_output.set_do_not_print_dict()

            return get_cli_specific_output(command_output)


def start_run(run_configuration, driver_arguments,
              project=".", conda_dependencies=None, spark_dependencies=None, untracked=False,
              run_async=None, target=None, prepare=None, wait=False):
    """
    Starts a run.
    :param run_configuration:
    :param driver_arguments:
    :param project:
    :param conda_dependencies:
    :param spark_dependencies:
    :param untracked:
    :param run_async:
    :param target:
    :param prepare:
    :param wait:
    :return:
    """
    # Set correlation id
    set_correlation_id()

    # TODO: User specified run_id and wait is not yet supported.

    if not driver_arguments or len(driver_arguments) == 0:
        raise UserErrorException("Please specify the script to run, with its arguments if any.")

    auth = get_cli_specific_auth()
    project_object = Project(auth=auth, directory=project)
    run_config_object = RunConfiguration.load(project_object.project_directory, run_configuration)
    telemetry_values = _get_telemetry_values()

    if conda_dependencies:
        run_config_object.environment.python.conda_dependencies_file = conda_dependencies

    if spark_dependencies:
        RunConfiguration._modify_runconfig_using_spark_config(spark_dependencies,
                                                              run_config_object, project_object.project_directory)
    if target:
        run_config_object.target = target

    run_config_object.history.output_collection = not untracked

    if prepare:
        run_config_object.auto_prepare_environment = prepare

    run_config_object.script = driver_arguments[0]
    script_run_config = ScriptRunConfig(project,
                                        run_config=run_config_object,
                                        arguments=driver_arguments[1:],
                                        _telemetry_values=telemetry_values)
    experiment = Experiment(project_object.workspace, project_object.history.name)
    run_object = experiment.submit(script_run_config)

    if not run_async:
        run_object.wait_for_completion(show_output=True, wait_post_processing=wait)
    else:
        command_output = CLICommandOutput("")
        command_output.append_to_command_output("RunId:" + run_object.id)
        azureml_cli_output = {"RunId": run_object.id}
        command_output.merge_dict(azureml_cli_output)
        command_output.set_do_not_print_dict()

        return get_cli_specific_output(command_output)


def return_results(run_id, target, project=".", overwrite=None):
    """Return experiment results"""
    # Set correlation id
    set_correlation_id()
    raise Exception("Not yet implemented.")
    from azureml._execution.commands import return_results
    command_output = return_results(run_id, target, project=project, overwrite=overwrite)
    return get_cli_specific_output(command_output)


def cancel_run(run_id, project="."):
    """Cancel executing run"""
    # Set correlation id
    set_correlation_id()

    auth = get_cli_specific_auth()
    project_object = Project(auth=auth, directory=project)
    experiment = Experiment(project_object.workspace, project_object.history.name)

    run_object = ScriptRun(experiment, run_id, directory=project)
    run_object.cancel()

    command_output = CLICommandOutput("Experiment run canceled successfully.")

    command_output.set_do_not_print_dict()

    return get_cli_specific_output(command_output)


def get_run_status(run_id, project="."):
    """Get status of a run"""
    # Set correlation id
    set_correlation_id()

    auth = get_cli_specific_auth()
    project_object = Project(auth=auth, directory=project)
    experiment = Experiment(project_object.workspace, project_object.history.name)
    run_object = ScriptRun(experiment, run_id, directory=project)
    status_str = json.dumps(run_object.get_details(), indent=4)
    command_output = CLICommandOutput("")
    command_output.append_to_command_output(status_str)
    command_output.set_do_not_print_dict()
    return get_cli_specific_output(command_output)


def clean(target=None, project=".", run_id=None, all=False):
    """Clean temporary data."""
    # Set correlation id
    set_correlation_id()
    if run_id and all:
        raise UserErrorException("Both run id and --all should not be specified together.")

    if not run_id and not all:
        raise UserErrorException("Please specify run id or set flag to --all")

    auth = get_cli_specific_auth()
    project_object = Project(auth=auth, directory=project)
    command_output = CLICommandOutput("")
    output_list = list()
    if all:
        if not target:
            raise UserErrorException("Target should be specified when using the all flag.")
        output_list = Run.clean_all(project_object, target)

    if run_id:
        experiment = Experiment(project_object.workspace, project_object.history.name)
        run_object = ScriptRun(experiment, run_id, directory=project)
        output_list = run_object.clean()

    for output in output_list:
        command_output.append_to_command_output(output)

    command_output.set_do_not_print_dict()
    return get_cli_specific_output(command_output)


def monitor_runs(run_id, project=".", tensorboard=False, port=6006, local_root=None):
    """Monitor an experiment"""
    set_correlation_id()

    command_output = CLICommandOutput("")
    command_output.set_do_not_print_dict()

    if not tensorboard:
        output = "Currently only experimental Tensorboard monitoring is supported. " \
                 "Add --tensorboard to start a Tensorboard instance that monitors this run."
        command_output.append_to_command_output(output)
        return get_cli_specific_output(command_output)

    try:
        from azureml.tensorboard import Tensorboard
    except ImportError as ex:
        output = "Unable to import Tensorboard runner library: {}".format(ex)
        command_output.append_to_command_output(output)
        return get_cli_specific_output(command_output)

    tb = None
    try:
        auth = get_cli_specific_auth()
        project_object = Project(auth=auth, directory=project)
        run_objects = map(lambda r: Run(project_object.workspace, project_object.history.name, r), run_id)
        tb = Tensorboard(run_objects, port=port, local_root=local_root)
        print("Starting a Tensorboard instance against the RunID(s): {}\n"
              "To stop it, press CTRL-C.".format(run_id))
        url = tb.start()
        print("Tensorboard started at: {}".format(url))
        while True:
            sleep(1)
    except KeyboardInterrupt:
        if tb:
            print("Stopping Tensorboard...")
            tb.stop()
            print("Tensorboard stopped.")

    return get_cli_specific_output(command_output)


def _get_telemetry_values():
    telemetry_values = {}
    telemetry_values['amlClientType'] = 'azureml-cli'
    return telemetry_values


def submit_pipeline(pipeline_id, pipeline_params=None, datapath_params=None, experiment_name=None,
                    workspace_name=None, resource_group_name=None):
    """
    Submit a pipeline run based on a published pipeline ID
    """
    set_correlation_id()

    workspace_object = get_workspace_or_default(workspace_name=workspace_name, resource_group=resource_group_name)

    from azureml.pipeline.core import PublishedPipeline
    pipeline = PublishedPipeline.get(workspace_object, pipeline_id)
    if experiment_name is None or experiment_name == '':
        # Use the pipeline name as the experiment name
        experiment_name = pipeline._sanitize_name()

    assigned_params = _parse_key_values(pipeline_params, 'Parameter assignment')

    datapaths = _parse_key_values(datapath_params, 'Datapath assignment')
    for datapath_param_name in datapaths:
        datastore_with_path = datapaths[datapath_param_name]
        if '/' not in datastore_with_path:
            raise UserErrorException("Datapath value %s should have format datastore/path" % datastore_with_path)
        path_tokens = datastore_with_path.split('/', 1)
        from azureml.core import Datastore
        from azureml.data.datapath import DataPath
        datastore = Datastore(workspace_object, path_tokens[0])
        assigned_params[datapath_param_name] = DataPath(datastore=datastore, path_on_datastore=path_tokens[1])

    pipeline_run = pipeline.submit(pipeline_parameters=assigned_params, workspace=workspace_object,
                                   experiment_name=experiment_name)

    command_output = CLICommandOutput("Pipeline was submitted with run ID %s" % pipeline_run.id)
    command_output.set_do_not_print_dict()

    return get_cli_specific_output(command_output)


def list_runs(pipeline_id=None, experiment_name=None, run=None, workspace_name=None, resource_group_name=None):
    """
    List runs that were generated from a published pipeline ID

    TODO:  Also support listing runs by experiment name or parent run ID
    """
    set_correlation_id()

    workspace_object = get_workspace_or_default(workspace_name=workspace_name, resource_group=resource_group_name)

    if experiment_name is not None or run is not None:
        raise NotImplementedError('Run listing by experiment name or parent run ID is not supported')

    if pipeline_id is None:
        raise UserErrorException("Pipeline ID must be provided")

    from azureml.pipeline.core import PipelineRun
    pipeline_runs = PipelineRun.get_pipeline_runs(workspace=workspace_object, pipeline_id=pipeline_id)
    serialized_run_list = []
    for pipeline_run in pipeline_runs:
        info_dict = pipeline_run._get_base_info_dict()

        # Fill in additional properties for a pipeline run
        if hasattr(pipeline_run._internal_run_dto, 'start_time_utc') \
                and pipeline_run._internal_run_dto.start_time_utc is not None:
            info_dict['StartDate'] = pipeline_run._internal_run_dto.start_time_utc.isoformat()

        if hasattr(pipeline_run._internal_run_dto, 'end_time_utc') \
                and pipeline_run._internal_run_dto.end_time_utc is not None:
            info_dict['EndDate'] = pipeline_run._internal_run_dto.end_time_utc.isoformat()

        properties = pipeline_run.get_properties()
        if 'azureml.pipelineid' in properties:
            info_dict['PiplineId'] = properties['azureml.pipelineid']
        serialized_run_list.append(info_dict)

    command_output = CLICommandOutput("")
    command_output.merge_dict(serialized_run_list)

    return get_cli_specific_output(command_output)

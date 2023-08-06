# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import argparse

from azureml._cli import abstract_subgroup
from azureml._cli import cli_command
from azureml._cli import argument


class ExperimentSubGroup(abstract_subgroup.AbstractSubGroup):
    """This class defines the experiment sub group."""

    def get_subgroup_name(self):
        """Returns the name of the subgroup.
        This name will be used in the cli command."""
        return "run"

    def get_subgroup_title(self):
        """Returns the subgroup title as string. Title is just for informative purposes, not related
        to the command syntax or options. This is used in the help option for the subgroup."""
        return "run subgroup commands"

    def get_nested_subgroups(self):
        """Returns sub-groups of this sub-group."""
        return super(ExperimentSubGroup, self).compute_nested_subgroups(__package__)

    def get_commands(self):
        """ Returns commands associated at this sub-group level."""
        # TODO: Adding commands to a list can also be automated, if we assume the
        # command function name to start with a certain prefix, like _command_*
        commands_list = [
            self._command_experiment_submit(),
            self._command_experiment_prepare(),
            # TODO: Return is not yet implemented correctly.
            # self._command_experiment_return(),
            self._command_experiment_cancel(),
            self._command_experiment_status(),
            self._command_experiment_clean(),
            self._command_experiment_monitor(),
            self._command_submit_pipeline(),
            self._command_list_runs()
        ]
        return commands_list

    def _command_experiment_submit(self):
        # Note: "driver_argument" name should match with the argument name in
        # "azureml._execution.commands.start"
        # Using nargs=argparse.REMAINDER and not nargs=+ or * so that the user program
        # can also have (non) positional arguments. But, those should always be specified
        # at the end of a command.

        driver_option = argument.Argument("driver_arguments", "driver_arguments", "",
                                          help="The run submit arguments, like script name and script arguments.",
                                          nargs=argparse.REMAINDER, positional_argument=True)
        function_path = "azureml._base_sdk_common.cli_wrapper.cmd_experiment#start_run"

        argument_list = [argument.RUN_CONFIGURATION_OPTION.get_required_true_copy(),
                         argument.TARGET_OPTION, argument.ASYNC_OPTION, argument.CONDA_DEPENDENCY_OPTION,
                         argument.SPARK_DEPENDENCY_OPTION, argument.UNTRACKED_RUN_OPTION,
                         argument.PROJECT_OPTION, argument.WAIT_OPTION, driver_option,
                         argument.PREPARE_RUN_OPTION]

        return cli_command.CliCommand("submit", "Submit an experiment for execution.", argument_list, function_path)

    def _command_experiment_prepare(self):
        check_option = argument.Argument("check", "--check", "",
                                         help="The command only checks the prepare status, i.e., if the experiment is "
                                         "already prepared or not. The command doesn't perform an actual prepare. "
                                         "--async and --untracked flags have no effect when used along with --check.",
                                         required=False,
                                         action="store_true",
                                         default=False)
        function_path = "azureml._base_sdk_common.cli_wrapper.cmd_experiment#prepare_run"

        argument_list = [argument.RUN_CONFIGURATION_OPTION.get_required_true_copy(), argument.TARGET_OPTION,
                         argument.ASYNC_OPTION, argument.CONDA_DEPENDENCY_OPTION, argument.SPARK_DEPENDENCY_OPTION,
                         argument.UNTRACKED_RUN_OPTION, argument.PROJECT_OPTION, argument.WAIT_OPTION, check_option]

        return cli_command.CliCommand("prepare", "Prepare an experiment for execution.", argument_list, function_path)

    def _command_experiment_return(self):
        overwrite_option = argument.Argument("overwrite", "--overwrite", "-f", required=False, action="store_true",
                                             help="Overwrite existing files.")

        function_path = "azureml._base_sdk_common.cli_wrapper.cmd_experiment#return_results"

        return cli_command.CliCommand("return", "Return an experiment's results.",
                                      [argument.RUN_ID_OPTION.get_required_true_copy(),
                                       argument.TARGET_OPTION.get_required_true_copy(),
                                       argument.PROJECT_OPTION, overwrite_option], function_path)

    def _command_experiment_cancel(self):
        function_path = "azureml._base_sdk_common.cli_wrapper.cmd_experiment#cancel_run"

        return cli_command.CliCommand("cancel", "Cancel an executing experiment.",
                                      [argument.RUN_ID_OPTION.get_required_true_copy(),
                                       argument.PROJECT_OPTION], function_path)

    def _command_experiment_status(self):
        function_path = "azureml._base_sdk_common.cli_wrapper.cmd_experiment#get_run_status"

        return cli_command.CliCommand("status", "Get status of an experiment.",
                                      [argument.RUN_ID_OPTION.get_required_true_copy(),
                                       argument.PROJECT_OPTION], function_path)

    def _command_experiment_clean(self):
        function_path = "azureml._base_sdk_common.cli_wrapper.cmd_experiment#clean"

        run_id_option_not_required = argument.RUN_ID_OPTION.clone()
        run_id_option_not_required.required = False

        clean_all_option = argument.Argument("all", "--all", "-a", required=False, action="store_true",
                                             help="Cleans all temporary data, including data shared by"
                                                  " multiple runs .")
        return cli_command.CliCommand("clean", "Clean up temporary files for experiments.",
                                      [argument.RUN_ID_OPTION, argument.TARGET_OPTION,
                                       argument.PROJECT_OPTION, clean_all_option],
                                      function_path)

    def _command_experiment_monitor(self):
        tensorboard_option = argument.Argument("tensorboard", "--tensorboard", "", required=False, action="store_true",
                                               help="Launch Tensorboard to monitor the run(s) (experimental)")
        port_option = argument.Argument("port", "--port", "", required=False, default=6006,
                                        help="Set the port to launch Tensorboard on.")
        root_option = argument.Argument("local_root", "--root-path", "", required=False, default=None,
                                        help="Set the filesystem root to download Tensorboard logs to.")
        function_path = "azureml._base_sdk_common.cli_wrapper.cmd_experiment#monitor_runs"

        multi_run_id_option = argument.RUN_ID_OPTION.get_required_true_copy()
        multi_run_id_option.action = 'append'
        multi_run_id_option.help += " (Can be specified multiple times.)"

        return cli_command.CliCommand("monitor", "Monitor an experiment.",
                                      [multi_run_id_option,
                                       argument.PROJECT_OPTION,
                                       tensorboard_option, port_option, root_option],
                                      function_path)

    def _command_submit_pipeline(self):
        function_path = "azureml._base_sdk_common.cli_wrapper.cmd_experiment#submit_pipeline"
        pipeline_id = argument.Argument("pipeline_id", "--pipeline-id", "-i", required=True,
                                        help="ID of the pipeline to submit (guid)")
        name = argument.Argument("experiment_name", "--experiment-name", "-n", required=False,
                                 help="Experiment name for run submission. If unspecified, use the pipeline name")
        pipeline_params = \
            argument.Argument("pipeline_params", "--parameters", "-p", required=False,
                              help="Comma-separated list of name=value pairs for pipeline parameter assignments")
        datapath_params = \
            argument.Argument("datapath_params", "--datapaths", "-d", required=False,
                              help="Comma-separated list of name=datastore/path pairs for " +
                                   "datapath parameter assignments")

        return cli_command.CliCommand("submit-pipeline", "Submit a pipeline for execution.",
                                      [pipeline_id,
                                       name,
                                       pipeline_params,
                                       datapath_params,
                                       argument.RESOURCE_GROUP_NAME,
                                       argument.WORKSPACE_NAME], function_path)

    def _command_list_runs(self):
        function_path = "azureml._base_sdk_common.cli_wrapper.cmd_experiment#list_runs"
        # TODO:  Support listing runs by experiment name or parent run ID.  Currently, only pipeline ID is supported.
        pipeline_id = argument.Argument("pipeline_id", "--pipeline-id", "-i", required=False,
                                        help="ID of the pipeline to list the runs of (guid)")
        experiment_name = argument.Argument("experiment_name", "--experiment-name", "-n", required=False,
                                            help="Experiment name to list the runs of")
        run = argument.Argument("run", "--run", "-r", required=False,
                                help="Parent run ID to list the child runs of")
        return cli_command.CliCommand("list", "List the runs generated from a source",
                                      [argument.RESOURCE_GROUP_NAME,
                                       argument.WORKSPACE_NAME,
                                       pipeline_id,
                                       experiment_name,
                                       run], function_path)

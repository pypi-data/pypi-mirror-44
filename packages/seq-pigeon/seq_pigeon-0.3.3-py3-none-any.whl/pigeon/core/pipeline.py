import sys
import os
from os.path import splitext, basename, exists, join
from pigeon.utils.parseconfig import ParseConfig
from pigeon.utils.runpipe import RunPipe


class Pipe():

    """Docstring for seqPipe. """

    def __init__(self, pipeline_config, dryrun=False, verbose=False, read_from='file'):
        """TODO: to be defined1. """

        pipe_configs = ParseConfig(pipeline_config, read_from=read_from)
        self.general_args = pipe_configs.general_args
        self.task_args = pipe_configs.task_args
        self.task_list = pipe_configs.task_list
        self.output_dir = self.general_args['output_dir']

        if 'project_name' in self.general_args:
            self.project_name = self.general_args['project_name']
        else:
            self.project_name = ''

        self.cmd_feed = {}
        self.input_feed = {
            'input_files': self.general_args['input_files'].split(' ')}

        if 'input_names' in self.general_args.keys():
            self.input_names = {
                'input_names': self.general_args['input_names'].split(' ')}

        self.dryrun = dryrun
        self.verbose = verbose
        self.create_pipeline()

    def in_out_feed(self, task, input_files):

        if 'dump_dir' in self.task_args[task].keys():
            dump_dir = self.task_args[task]['dump_dir']
            if self.dryrun is not True:
                mkdir(join(self.output_dir, dump_dir))
        else:
            dump_dir = ''

        if 'ext' in self.task_args[task].keys():
            ext = self.task_args[task]['ext']
        else:
            ext = ''
        if 'suffix' in self.task_args[task].keys():
            suffix = self.task_args[task]['suffix']
        else:
            suffix = ''

        if 'input_multi' in self.task_args[task].keys() and (self.task_args[task]['input_multi'] == 'paired' or self.task_args[task]['input_multi'] == 'all'):
            in_out = join(self.output_dir, dump_dir, splitext(
                basename(input_files[0]))[0] + suffix + '.' + ext)
        else:
            in_out = join(self.output_dir, dump_dir, splitext(
                basename(input_files))[0] + suffix + '.' + ext)

        # add newly created output files to input feed to be used by next task
        if 'paired_output' in self.task_args[task].keys():
            if task not in self.input_feed.keys():
                self.input_feed[task] = [input_files, in_out]
            # if it exists append the output
            else:
                self.input_feed[task].extend([input_files, in_out])
        else:
            if task not in self.input_feed.keys():
                self.input_feed[task] = [in_out]
            # if it exists append the output
            else:
                self.input_feed[task].append(in_out)

        return in_out

    def create_cmd(self, task, input_files, name=None):
        cmd = ''
        # if container task add container -jar to start
        if 'container' in self.task_args[task].keys():
            cmd = cmd + self.task_args[task]['container']
        # otherwise just add path to task
        cmd = cmd + self.task_args[task]['tool']
        # if running sub command add the sub command
        if 'sub_tool' in self.task_args[task].keys():
            cmd = cmd + ' ' + self.task_args[task]['sub_tool']
        # add the args
        cmd = cmd + ' ' + self.task_args[task]['args'].replace('\n', ' ')
        # If names true add names
        if 'named' in self.task_args[task].keys():
            cmd = cmd.replace('name_placeholder', name)
        # replace inputplaceholder with paired input files
        if 'input_multi' in self.task_args[task].keys():
            if self.task_args[task]['input_multi'] == 'paired':
                if 'secondary_in_placeholder' in self.task_args[task].keys():
                    cmd = cmd.replace('input_placeholder', input_files[0])
                    cmd = cmd.replace(
                        'secondary_in_placeholder', input_files[1])
                else:
                    cmd = cmd.replace('input_placeholder',
                                      ' '.join(input_files))
            elif self.task_args[task]['input_multi'] == 'all':
                if 'input_flag_repeat' in self.task_args[task].keys():
                    flag_string = ' {} '.format(
                        self.task_args[task]['input_flag_repeat'])
                else:
                    flag_string = ' '
                cmd = cmd.replace('input_placeholder',
                                  flag_string.join(input_files))
        else:
            cmd = cmd.replace('input_placeholder', input_files)
        # replace output_placeholder with first file
        in_out = self.in_out_feed(task, input_files)
        cmd = cmd.replace('output_placeholder', in_out)

        if 'secondary_output' in self.task_args[task].keys():
            cmd = cmd.replace('secondary_out_placeholder',
                              self.secondary_output(task, input_files))

        return cmd

    def create_pipeline(self):
        for task in self.task_list:
            # For multiple input
            if 'input_multi' in self.task_args[task].keys():
                # For paired
                if self.task_args[task]['input_multi'] == 'paired':
                    # For paired and named
                    if 'named' in self.task_args[task].keys():
                        for name, input_files in zip(self.input_names['input_names'], chunks(self.input_feed[self.task_args[task]['input_from']], 2)):
                            if task not in self.cmd_feed.keys():
                                self.cmd_feed[task] = [
                                    self.create_cmd(task, input_files, name)]
                            # if it exists append the output
                            else:
                                self.cmd_feed[task].append(
                                    self.create_cmd(task, input_files, name))
                    # Paired and not named
                    else:
                        for input_files in chunks(self.input_feed[self.task_args[task]['input_from']], 2):
                            if task not in self.cmd_feed.keys():
                                self.cmd_feed[task] = [
                                    self.create_cmd(task, input_files)]
                            # if it exists append the output
                            else:
                                self.cmd_feed[task].append(
                                    self.create_cmd(task, input_files))

                # Can't name if input is all
                elif self.task_args[task]['input_multi'] == 'all':
                    self.cmd_feed[task] = [
                        self.create_cmd(task, self.input_feed[self.task_args[task]['input_from']])]

            else:
                # Single named input
                if 'named' in self.task_args[task].keys():
                    for name, input_file in zip(self.input_names['input_names'], self.input_feed[self.task_args[task]['input_from']]):
                        if task not in self.cmd_feed.keys():
                            self.cmd_feed[task] = [
                                self.create_cmd(task, input_file, name)]
                        # if it exists append the output
                        else:
                            self.cmd_feed[task].append(
                                self.create_cmd(task, input_file, name))
                # Single Unnamed input
                else:
                    for input_file in self.input_feed[self.task_args[task]['input_from']]:
                        if task not in self.cmd_feed.keys():
                            self.cmd_feed[task] = [
                                self.create_cmd(task, input_file)]
                        # if it exists append the output
                        else:
                            self.cmd_feed[task].append(
                                self.create_cmd(task, input_file))

    def run_pipeline(self):
        for task in self.task_list:
            for cmd in self.cmd_feed[task]:
                if self.dryrun is not True:
                    mkdir(self.output_dir)
                    if 'pass' not in self.task_args[task].keys():
                        task_instance = RunPipe(
                            cmd, task, self.output_dir, self.project_name, self.verbose)
                        task_instance.run_task()
                    else:
                        pass
                else:
                    if 'pass' in self.task_args[task].keys():
                        sys.stdout.write('Passed:\n' + cmd + '\n')
                    else:
                        sys.stdout.write('\n' + cmd + '\n')
        self.remove_files()

    def remove_files(self):
        for task in self.task_list:
            if 'remove' in self.task_args[task].keys() and self.task_args[task]['remove'] == 'True':
                for marked_for_removal in self.input_feed[task]:
                    if self.dryrun is True:
                        sys.stdout.write(
                            'Will be removed: {}'.format(marked_for_removal))
                    else:
                        os.remove(marked_for_removal)

    def secondary_output(self, task, input_files):
        if 'secondary_dump_dir' in self.task_args[task].keys():
            secondary_dump_dir = self.task_args[task]['secondary_dump_dir']
        else:
            secondary_dump_dir = ''
        if self.dryrun is not True:
            mkdir(join(self.output_dir, secondary_dump_dir))
        if 'secondary_ext' in self.task_args[task].keys():
            secondary_ext = self.task_args[task]['secondary_ext']
        else:
            secondary_ext = ''
        if 'secondary_suffix' in self.task_args[task].keys():
            secondary_suffix = self.task_args[task]['secondary_suffix']
        else:
            secondary_suffix = ''
        if 'input_multi' in self.task_args[task].keys() and (self.task_args[task]['input_multi'] == 'paired' or self.task_args[task]['input_multi'] == 'all'):
            secondary_out = join(self.output_dir, secondary_dump_dir, splitext(
                basename(input_files[0]))[0] + secondary_suffix + '.' + secondary_ext)
        else:
            secondary_out = join(self.output_dir, secondary_dump_dir, splitext(
                basename(input_files))[0] + secondary_suffix + '.' + secondary_ext)
        return secondary_out


def mkdir(directory):
    if not exists(directory):
        os.makedirs(directory)


def chunks(l, n):
    '''Yield successive n-size chunks from l.'''
    for i in range(0, len(l), n):
        yield l[i:i + n]

from __future__ import print_function

import argparse
import itertools
import os
import re
import shutil
import subprocess
import sys
import time

from datetime import datetime
from .runner_utils import *

os.environ['LC_ALL'] = 'C'
os.umask(0o77)


def parseArgumentList():
  parser = argparse.ArgumentParser()
  parser.add_argument('--srv-path', required=True)
  parser.add_argument('--backup-path', required=True)
  parser.add_argument('--etc-path', required=True)
  parser.add_argument('--rsync-binary', default='rsync')
  parser.add_argument('--backup-wait-time', type=int, required=True)
  parser.add_argument('-n', action='store_true', dest='dry', default=False)

  return parser.parse_args()


def rsync(rsync_binary, source, destination, extra_args=None, dry=False):
  arg_list = [
    rsync_binary,
    '-rlptgov',
    '--stats',
    '--safe-links',
    '--ignore-missing-args',
    '--delete',
    '--delete-excluded'
  ]
  if isinstance(extra_args, list):
    arg_list.extend(extra_args)
  if isinstance(source, list):
    arg_list.extend(source)
  else:
    arg_list.append(source)
  arg_list.append(destination)

  if dry:
    print('DEBUG:', arg_list)
    return

  try:
    print(subprocess.check_output(arg_list))
  except subprocess.CalledProcessError as e:
    # All rsync errors are not to be considered as errors
    allowed_error_message_list = \
      '^(file has vanished: |rsync warning: some files vanished before they could be transferred)'
    if e.returncode != 24 or \
        re.search(allowed_error_message_regex, e.output, re.M) is None:
      raise


def synchroniseRunnerConfigurationDirectory(config, backup_path):
  if not os.path.exists(backup_path):
    os.makedirs(backup_path)

  file_list = ['config.json']
  for hidden_file in os.listdir('.'):
    if hidden_file[0] == '.':
      file_list.append(hidden_file)
  rsync(config.rsync_binary, file_list, backup_path, dry=config.dry)


def synchroniseRunnerWorkingDirectory(config, backup_path):
  file_list = []
  exclude_list = []

  if os.path.isdir('instance'):
    file_list.append('instance')
    exclude_list = getExcludePathList(os.getcwd())

  # XXX: proxy.db should be properly dumped to leverage its
  # atomic properties
  for file in ('project', 'public', 'proxy.db'):
    if os.path.exists(file):
      file_list.append(file)

  if file_list:
    rsync(
      config.rsync_binary, file_list, backup_path,
      ["--exclude={}".format(x) for x in exclude_list],
      dry=config.dry
    )


def backupFilesWereModifiedDuringExport(export_start_date):
  export_time = time.time() - export_start_date
  return bool(
    subprocess.check_output((
      'find', '-cmin',  str(export_time / 60.), '-type', 'f', '-path', '*/srv/backup/*'
    ))
  )


def runExport():
  export_start_date = int(time.time())
  print(datetime.fromtimestamp(export_start_date).isoformat())

  args = parseArgumentList()

  def _rsync(*params):
    return rsync(args.rsync_binary, *params, dry=args.dry)

  runner_working_path = os.path.join(args.srv_path, 'runner')
  backup_runner_path = os.path.join(args.backup_path, 'runner')

  # Synchronise runner's etc directory
  with CwdContextManager(args.etc_path):
    with open('.resilient-timestamp', 'w') as f:
      f.write(str(export_start_date))

    # "+ '/'" is mandatory otherwise rsyncing the etc directory
    # will create in the backup_etc_path only a file called etc
    backup_etc_path = os.path.join(args.backup_path, 'etc') + '/'
    synchroniseRunnerConfigurationDirectory(args, backup_etc_path)

  # Synchronise runner's working directory
  # and aggregate signature functions as we are here
  with CwdContextManager(runner_working_path):
    synchroniseRunnerWorkingDirectory(args, backup_runner_path)
    slappart_signature_method_dict = getSlappartSignatureMethodDict()

  # Calculate signature of synchronised files
  with CwdContextManager(args.backup_path):
    writeSignatureFile(slappart_signature_method_dict, runner_working_path)

  # BBB: clean software folder if it was synchronized
  # in an old instance
  backup_software_path = os.path.join(backup_runner_path, 'software')
  if os.path.isdir(backup_software_path):
    shutil.rmtree(backup_software_path)


  # Wait a little to increase the probability to detect an ongoing backup.
  time.sleep(10)

  # Check that export didn't happen during backup of instances
  with CwdContextManager(os.path.join(runner_working_path, 'instance')):
    if backupFilesWereModifiedDuringExport(export_start_date):
      print("ERROR: Some backups are not consistent, exporter should be re-run."
            " Let's sleep %s minutes, to let the backup end..." % args.backup_wait_time)
      time.sleep(args.backup_wait_time * 60)
      sys.exit(1)

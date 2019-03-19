import subprocess as sp
import argparse
import sys
import os

R1 = 'r1_files'
R2 = 'r2_files'
BASE = 'base'
EXP = 'experimental'
ANNOTATIONS = 'annotations'

def run_cmd(cmd, return_stderr=False):
    '''
    Runs a command through the shell
    '''
    p = sp.Popen(cmd, shell=True, stderr=sp.PIPE, stdout=sp.PIPE)
    stdout, stderr = p.communicate()
    if return_stderr:
        return (p.returncode, stderr.decode('utf-8'))
    return (p.returncode, stdout.decode('utf-8'))


def check_fastq_format(fastq_list):
    '''
    Runs the fastQValidator on each fastq file
    IF the file is invalid, the return code is 1 and
    the error goes to stdout.  If OK, then return code is zero.
    '''
    err_list = []
    base_cmd = 'fastQValidator --file %s'
    for f in fastq_list:
        cmd = base_cmd % f
        rc, stdout_string = run_cmd(cmd)
        if rc == 1:
            err_list.append(stdout_string)
    return err_list


def check_gzip_format(fastq_list):
    '''
    gzip -t <file> has return code zero if OK
    if not, returncode is 1 and error is printed to stderr
    '''
    err_list = []
    base_cmd = 'gzip -t %s'
    for f in fastq_list:
        cmd = base_cmd % f
        rc, stderr_string = run_cmd(cmd, return_stderr=True)
        if rc == 1:
            err_list.append(stderr_string)
    return err_list


def catch_very_long_reads(fastq_list, N=100, L=300):
    '''
    In case we get non-illumina reads, they will not exceed some threshold (e.g. 300bp)
    '''
    err_list = []
    for f in fastq_list:
        zcat_cmd = 'zcat %s | head -%d' % (f, 4*N)
        rc, stdout = run_cmd(zcat_cmd)
        lines = stdout.split('\n')
        
        # iterate through the sampled sequences.  
        # We don't want to dump a ton of long sequences, so if we encounter
        # ANY in our sample, save an error message and exit the loop.
        # Thus, at most one error per fastq.
        ok = True
        i = 1
        while ok and (i < len(lines)):
            if len(lines[i]) > L:
                err_list.append('Fastq file (%s) had a read of length %d, '
                    'which is too long for a typical Illumina read.  Failing file.' % (f, len(lines[i])))
                ok = False
            i += 4
    return err_list



def get_commandline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', required=True, dest=ANNOTATIONS)
    parser.add_argument('-r1', required=True, dest=R1, nargs='+')
    parser.add_argument('-r2', required=True, dest=R2, nargs='+')
    parser.add_argument('-x', required=True, dest=BASE, nargs='+')
    parser.add_argument('-y', required=True, dest=EXP, nargs='+')

    args = parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    arg_dict = get_commandline_args()

    # collect the error strings into a list, which we will eventually dump to stderr
    err_list = []

    # put all the fastq into a list:
    all_fastq = []
    all_fastq.extend(arg_dict[R1])
    all_fastq.extend(arg_dict[R2])

    # check that fastq in gzip:
    err_list.extend(check_gzip_format(fastq_list))

    # check the fastq format
    err_list.extend(check_fastq_format(all_fastq))

    # check that read lengths are consistent with Illumina:
    err_list.extend(catch_very_long_reads(all_fastq))

    if len(err_list) > 0:
        sys.stderr.write('\n'.join(err_list))
        sys.exit(1) # need this to trigger Cromwell to fail
        

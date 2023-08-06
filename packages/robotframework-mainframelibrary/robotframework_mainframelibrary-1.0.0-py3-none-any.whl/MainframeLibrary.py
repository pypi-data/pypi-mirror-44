'''
This is the library to work with Mainframe applications: submit jcls, verify spool, upload and retrieve datasets.

The connection to Mainframe establishes over secure ftp tls protocol by ftplib.

Author: Nadezhda Baranova

'''

import ftplib
from ftplib import FTP_TLS

import os
import codecs

rfftp = None
NO_DEBUG_OUTPUT = 0
MODERATE_DEBUG_OUTPUT = 1
MAX_DEBUG_OUTPUT = 2


def mainframe_connect(host, user='anonymous', password='anonymous@'):
    '''
    Creates ftp object, opens a connection to mainframe, login and secures de connection.
    Returns server output.
    Parameters:
        - host - server host or IP.
        - user - mainframe user name. If not given, 'anonymous' is used.
        - password - mainframe password. If not given, 'anonymous@' is used.
    '''
    global rfftp
    output_msg = ""

    if __check_ftp_tls_status(True):
        rfftp = FTP_TLS(host)
        output_msg = rfftp.set_debuglevel(MAX_DEBUG_OUTPUT)
        rfftp.auth()
        output_msg = rfftp.login(user, password)  # login before securing control channel
        print("Response login: " + output_msg)
        output_msg = rfftp.prot_p()  # switch to secure data connection
        print("Response prot_p: " + output_msg)
        return


def mainframe_submit_job_from_file(file_path):
    '''
    Submits jcl from file.
    Returns job id.
    Parameters:
        - file_path - path to file.
    '''
    global rfftp
    output_msg = ""

    if __check_ftp_tls_status():

        output_msg = rfftp.sendcmd('SITE FILETYPE=JES')
        print("Response sendcmd SITE FILETYPE=JES: " + output_msg)

        output_msg = rfftp.storlines('STOR TESTFILE', open(file_path, 'rb'))
        print("Response STOR TESTFILE: " + output_msg)

        job_status = output_msg.find('250-It is known to JES as')
        if job_status < 0:
            error_msg = "JOB Id not valid."
            rfftp = None
            raise FtpTlsLibraryError(error_msg)
        # return True
        else:
            offset = output_msg.find('JES as ')
            job_id = output_msg[offset + 7:offset + 15]
            return job_id


def mainframe_retrieve_job_spool_info_to_file(job_id, job_owner, file_path, option='Info'):
    '''
    Retrieves spool info to text file.
    Returns server output.
    Parameters:
        - job_id - job id returned by Mainframe.
        - job_owner - job owner.
        - file_path - file to store the spool.
        - option - Info, is the default will only bring the high level information, Verbose: will bring all the information.
    '''
    global rfftp
    output_msg = ""
    lines = []
    if __check_ftp_tls_status():

        output_msg = rfftp.sendcmd('SITE FILETYPE=JES')
        print("Response sendcmd SITE FILETYPE=JES: " + output_msg)
        output_msg = rfftp.sendcmd('SITE JESOWNER=' + job_owner)
        print("Response sendcmd SITE JESOWNER=' " + job_owner + output_msg)
        output_msg = rfftp.sendcmd('SITE JESJOBNAME=*')
        print("Response sendcmd SITE JESJOBNAME=*" + output_msg)

        #        txtFile = open(strFilePath + strJobCustomName + '_'+ strJOBId + '.txt', 'wt')
        a = codecs.open(file_path, 'w', 'utf8')
        if option == 'Info':
          output_msg = rfftp.retrlines('LIST ' + job_id, lines.append)
        else:
            option == 'Verbose'
            output_msg = rfftp.retrlines('RETR ' + job_id, lines.append)
        for line in lines:
            #           txtFile.write(line+"\n")
            a.write(str(line) + "\n")
        # txtFile = file(strFilePath + strJOBId + '.txt', 'wt')
        # output_msg = rfftp.retrlines('RETR ' + strJOBId, txtFile.write)
        print("Response RETR " + job_id + ": " + output_msg)
        return output_msg

def mainframe_retrieve_job_spool_info_as_lines(job_id, job_owner, option='Info'):
    '''
    Retrieves spool info as lines, does not require an output file.
    Returns spool info.
    Parameters:
        - job_id - spool job id.
        - job_owner - job owner.
        - option - Info, is the default will only bring the high level information, Verbose: will bring all the information.
    '''

    global rfftp
    lines = []
    if __check_ftp_tls_status():
#        rfftp.sendcmd('SITE FILETYPE=JES')
#        rfftp.sendcmd('SITE JESOWNER=' + strJobOwner)
#        rfftp.sendcmd('SITE JESJOBNAME=*')

        output_msg = rfftp.sendcmd('SITE FILETYPE=JES')
        print("Response sendcmd SITE FILETYPE=JES: " + output_msg)
        output_msg = rfftp.sendcmd('SITE JESOWNER=' + job_owner)
        print("Response sendcmd SITE JESOWNER=' " + job_owner + output_msg)
        output_msg = rfftp.sendcmd('SITE JESJOBNAME=*')
        print("Response sendcmd SITE JESJOBNAME=*" + output_msg)

        if option == 'Info':
            rfftp.retrlines('LIST ' + job_id, lines.append)
        else:
            option == 'Verbose'
            rfftp.retrlines('RETR ' + job_id, lines.append)

        return lines


def mainframe_retrieve_dataset(dataset, file_path):
    '''
    Retrieves dataset into text file.
    Returns server output.
    Parameters:
        - dataset - Mainframe dataset name.
        - file_path - file to store the dataset.
    '''
    global rfftp
    output_msg = ""
    lines = []
    if __check_ftp_tls_status():

            output_msg = rfftp.sendcmd('SITE FILETYPE=SEQ')
            print("Response sendcmd SITE FILETYPE=SEQ: " + output_msg)

            a = codecs.open(file_path, 'w', 'utf8')
            output_msg = rfftp.retrlines('RETR ' + dataset, lines.append)
            for line in lines:
                # txtFile.write(str(line.encode("utf-8"))+"\n")
                # txtFile.write(line+"\n")
                a.write(str(line) + "\n")
            print("Response RETR " + dataset + ": " + output_msg)
            return output_msg
  
def mainframe_upload_dataset(local_file_name, remote_file_name="None", remote_lrecl="None", remote_recfm="None"):
    '''
    Uploads file from local drive to Mainframe.
    Returns server output.
    Parameters:
    - local_file_path - local file.
    - remote_file_name (optional) - a name or path under which file should be saved.
    If remote_file_name argument is not given, local name will be used.
    '''
    global rfftp
    output_msg = ""
    lines = []

    if __check_ftp_tls_status():
        cmd = 'SITE FILETYPE=SEQ BLKSIZE=0 '
        if remote_lrecl != 'None':
            cmd += ' LRECL=' + remote_lrecl + ' '
        if remote_recfm != 'None':
            cmd += ' RECFM=' + remote_recfm + ' '
        output_msg = rfftp.sendcmd(cmd)
        local_file_path = os.path.normpath(local_file_name)
        if not os.path.isfile(local_file_path):
            raise FtpTlsLibraryError("Valid file path should be provided." + local_file_name)
        if remote_file_name == 'None':
            remote_file_path = local_file_name
            file_tuple = os.path.split(local_file_name)
            if len(file_tuple) == 2:
                remote_file_path = file_tuple[1]
        else:
            remote_file_path=remote_file_name
        try:
            output_msg = rfftp.storlines('STOR ' + remote_file_path, open(local_file_name, 'rb'))
        except ftplib.all_errors as e:
            raise FtpTlsLibraryError(str(e))

        return output_msg


def mainframe_dataset_size(dataset):
    '''
    Checks size of a file on mainframe. Returns size of a file in bytes (integer).
    Returns the size.
    Parameters:
    - dataset - file in Mainframe.
    IMPORTANT: Function works properly if only Mainframe allowed .size() function. Otherwise returns exception.
    '''
    global rfftp
    size_of_file = 0
    output_msg = ""
    if __check_ftp_tls_status():
        size_of_file = rfftp.size(dataset)
        print("Response: " + str(size_of_file))
        return size_of_file

def mainframe_delete_dataset(dataset):
    '''
    Deletes file on mainframe.
    Returns server output.
    Parameters:
    - dataset - file to be deleted
    '''
    global rfftp
    output_msg = ""
    if __check_ftp_tls_status():
        output_msg = rfftp.delete(dataset)
        print("Response: " + output_msg)
        return output_msg


def mainframe_change_working_directory(directory):
    '''
    Changes working directory.
    Returns server output.
    Parameters:
        - directory - a new working directory.
    '''
    global rfftp
    output_msg = ""
    if __check_ftp_tls_status():
        output_msg = rfftp.cwd(directory)
        print("Response: " + output_msg)
        return output_msg


def mainframe_list_directory(file_type, item=''):
    '''
    Returns list of contents of current directory or MVS spool according to filetype.
    Parameters:
    - file_type = dataset, spool.
    - item =
        for dataset, fully qualified name or dataset name.
        for spool, job id
    '''
    global rfftp
    output_msg = ""
    if __check_ftp_tls_status():

        if file_type == "dataset":
            print("Dir mode: MVS Data Set")
            output_msg = rfftp.sendcmd('SITE FILETYPE=SEQ')
        elif file_type == "spool":
            print("Dir mode: MVS Spool")
            output_msg = rfftp.sendcmd('SITE FILETYPE=JES')
        else:
            raise FtpTlsLibraryError("File Type not supported")

        if item == "":
            output_msg = rfftp.retrlines('LIST ')
            # dirList = rfftp.dir()
            print("Response LIST only: " + output_msg)
        else:
            output_msg = rfftp.retrlines('LIST ' + item)
            # dirList = rfftp.dir(dirItem, None)
            print("Response LIST + dirItem: " + output_msg)

        print(output_msg)
        return output_msg



def mainframe_create_directory(directory_name, recl="None", recfm="None"):
    '''
    Creates new directory on Mainframe.
    Returns new directory path.
    Parameters:
    - directory_name - name of a new directory.
    '''
    global rfftp
    output_msg = ""
    if __check_ftp_tls_status():
        cmd = 'SITE FILETYPE=PDS BLKSIZE=0 '
        if recl != 'None':
            cmd += ' LRECL=' + recl + ' '
        if recfm != 'None':
            cmd += ' RECFM=' + recfm + ' '
        output_msg = rfftp.sendcmd(cmd)
        output_msg = rfftp.mkd(directory_name)
        print("Response: " + output_msg)
        return output_msg



def mainframe_quit():
    '''
    Quit ftp tls connection.
    Returns None.
    Parameters: None
    '''
    global rfftp
    if __check_ftp_tls_status():
        rfftp.quit()
    rfftp = None


def mainframe_close():
    '''
    Closes ftp tls connection.
    Returns None.
    Parameters: None
    '''
    global rfftp
    if __check_ftp_tls_status():
        rfftp.close()
    rfftp = None


def __check_ftp_tls_status(inverted=False):
    global rfftp
    if inverted:
        if not isinstance(rfftp, FTP_TLS):
            return True
        else:
            raise FtpTlsLibraryError("Active FTP connection already exists.")
    else:
        if isinstance(rfftp, FTP_TLS):
            return True
        else:
            error_msg = "No active FTP TLS connection exists."
            error_msg += " One must be created before calling this method."
            raise FtpTlsLibraryError(error_msg)


class FtpTlsLibraryError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def __main():
    print ("Mainframe Library for Robotframework")

if __name__ == '__main__':
    __main()

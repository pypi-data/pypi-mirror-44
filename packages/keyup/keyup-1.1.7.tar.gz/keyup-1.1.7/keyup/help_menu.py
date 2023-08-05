"""

Help Menu
    Help menu object containing body of help content.
    For printing with formatting

"""

from pyaws import Colors
from keyup.colormap import ColorMap
from keyup.statics import PACKAGE, CONFIG_SCRIPT


# globals
cm = ColorMap()


PKG_ACCENT = Colors.ORANGE
PARAM_ACCENT = Colors.WHITE
bdwt = cm.bdwt


help_title = bdwt + PACKAGE + Colors.RESET + ' command help'

synopsis_cmd = (
    Colors.RESET + PKG_ACCENT + PACKAGE +
    PARAM_ACCENT + ' --profile ' + Colors.RESET + ' [PROFILE] ' +
    PARAM_ACCENT + '--operation ' + Colors.RESET + '[OPERATION]'
    )

url_doc = Colors.URL + 'http://keyup.readthedocs.io' + Colors.RESET
url_sc = Colors.URL + 'https://bitbucket.org/blakeca00/keyup' + Colors.RESET

menu_body = bdwt + """
  DESCRIPTION""" + Colors.RESET + """
            Automated IAM Access Key Rotation for Amazon Web Services

            Documentation  :  """ + url_doc + """
            Source Code    :  """ + url_sc + """
    """ + bdwt + """
  SYNOPSIS""" + Colors.RESET + """

              """ + synopsis_cmd + """

                             -p, --profile    <value>
                             -o, --operation  <value>
                            [-u, --user-name  <value> ]
                            [-a, --auto    ]
                            [-c, --configure  ]
                            [-R, --key-report ]
                            [-d, --debug   ]
                            [-h, --help    ]
                            [-V, --version ]
    """ + bdwt + """
  OPTIONS
        -p, --profile""" + Colors.RESET + """  <value>:  Profile  name of an IAM  (Identity Access
            Management) user from the local awscli configuration for which
            you want to rotate access keys.
    """ + bdwt + """
        -o, --operation""" + Colors.RESET + """  <value>: Operation conducted on the access key of
            the IAM user denoted in --profile value. Valid: {list, update}

                    - list  :  List keys and key metadata (DEFAULT)
                    - up    :  Create new keys, replace old keyset
    """ + bdwt + """
        -u, --user-name""" + Colors.RESET + """  <value>:  IAM username for which you will conduct
            key operations  using the permissions  of the profile username
            provided with the --profile option.
    """ + bdwt + """
        -a, --auto""" + Colors.RESET + """:  Suppress stdout output when """ + PACKAGE + """ is triggered via a
            scheduler such as unix cron or alternative automated means to
            rotate keys on a periodic schedule.
    """ + bdwt + """
        -c, --configure""" + Colors.RESET + """:  Configure custom values for runtime parameters.
            If local configuration file does not exist,  option writes new
            local configuration file to disk.  If a file exists, overwrite
            the existing configuration with updated values.

              Configure runtime options:  |  Display local config file:
                                          |
                $ """ + PKG_ACCENT + PACKAGE + PARAM_ACCENT + ' --configure' + Colors.RESET + """       |       $ """ + PKG_ACCENT + CONFIG_SCRIPT + PARAM_ACCENT + """
    """ + bdwt + """
        -R, --key-report""" + Colors.RESET + """:  Key expiration report for  all identities found
            in local awscli configuration files. Expired keysets are noted
            in red. Displays metadata for all keysets including key create
            date,  and the Identity Access Management (IAM) user  to which
            the awscli profile name maps in the AWS Account.
    """ + bdwt + """
        -d, --debug""" + Colors.RESET + """:  When True, only write newly generated credentials to
            temporary location on the  local filesystem instead of writing
            to local awscli config file(s).  Allows safe validation of the
            intgrity of the newly  created AWS authentication credentials.
    """ + bdwt + """
        -V, --version""" + Colors.RESET + """:  Print the """ + PACKAGE + """ package version.
    """ + bdwt + """
        -h, --help""" + Colors.RESET + """:  Show this help message and exit.
    """

# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import argparse


class CommandLine(object):
    """Class to handle the command line arguments

    Core Attributes
    ---------------
    webdir: str
        path to the directory where the data will be stored
    baseurl: str
        the url for the web directory
    samples: list
        list of strings giving paths to the results files
    email: str
        the email account that will be emailed when the job is complete
    dump: Bool
        Boolean to determine if all the data will be presented on a single
        webpage or not
    add_to_existing: Bool
        Boolean to determine if you would like to add to an existing html page
    existing_webdir: str
        path to the existing web directory
    inj_file: list
        list of strings showing paths to the injected files
    user: str
        the user who submitted the job
    labels: list
        list of labels that you would like to use
    verbose: Bool
        Boolean to determine if debugging information is printed
    save_to_hdf5: Bool
        Boolean to determine if the meta file is saved as an HDF5 file.

    GW Specific Attributes
    ----------------------
    approximant: list
        list of approximats used to generate the samples
    config: list
        list of paths to the configuration file associated with each results
        file
    sensitivity: Bool
        Boolean to determine if the sky sensitivities should be plotted
    psd: list
        list of psd files that were used in the analysis
    calibration: list
        list of calibration files that were used in the analysis
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(description=__doc__)
        self._setup_parser()
        self.opts = self.parser.parse_args()

    @property
    def webdir(self):
        return self.opts.webdir

    @property
    def baseurl(self):
        return self.opts.baseurl

    @property
    def samples(self):
        return self.opts.samples

    @property
    def email(self):
        return self.opts.email

    @property
    def dump(self):
        return self.opts.dump

    @property
    def add_to_existing(self):
        return self.opts.add_to_existing

    @property
    def existing_webdir(self):
        return self.opts.existing_webdir

    @property
    def inj_file(self):
        return self.opts.inj_file

    @property
    def user(self):
        return self.opts.user

    @property
    def labels(self):
        return self.opts.labels

    @property
    def verbose(self):
        return self.opts.verbose

    @property
    def save_to_hdf5(self):
        return self.opts.save_to_hdf5

    @property
    def approximant(self):
        return self.opts.approximant

    @property
    def config(self):
        return self.opts.config

    @property
    def sensitivity(self):
        return self.opts.sensitivity

    @property
    def gracedb(self):
        return self.opts.gracedb

    @property
    def psd(self):
        return self.opts.psd

    @property
    def calibration(self):
        return self.opts.calibration

    def _setup_parser(self):
        self.parser.add_argument("-w", "--webdir", dest="webdir",
                                 help="make page and plots in DIR",
                                 metavar="DIR", default=None)
        self.parser.add_argument("-b", "--baseurl", dest="baseurl",
                                 help="make the page at this url",
                                 metavar="DIR", default=None)
        self.parser.add_argument("-s", "--samples", dest="samples",
                                 help="Posterior samples hdf5 file", nargs='+',
                                 default=None)
        self.parser.add_argument("--email", action="store",
                                 help=("send an e-mail to the given address "
                                       "with a link to the finished page."),
                                 default=None)
        self.parser.add_argument("--dump", action="store_true",
                                 help=("dump all information onto a single "
                                       "html page"), default=False)
        self.parser.add_argument("--add_to_existing", action="store_true",
                                 help=("add new results to an existing html "
                                       "page"), default=False)
        self.parser.add_argument("-e", "--existing_webdir", dest="existing",
                                 help="web directory of existing output",
                                 default=None)
        self.parser.add_argument("-i", "--inj_file", dest="inj_file",
                                 help="path to injetcion file", nargs='+',
                                 default=None)
        self.parser.add_argument("--user", dest="user", help=argparse.SUPPRESS,
                                 default="albert.einstein")
        self.parser.add_argument("--labels", dest="labels",
                                 help="labels used to distinguish runs",
                                 nargs='+', default=None)
        self.parser.add_argument("-v", "--verbose", action="store_true",
                                 help=("print useful information for debugging "
                                       "purposes"))
        self.parser.add_argument("--save_to_hdf5", action="store_true",
                                 help="save the meta file in hdf5 format",
                                 default=False)
        self.parser.add_argument("-a", "--approximant", dest="approximant",
                                 help=("waveform approximant used to generate "
                                       "samples"), nargs='+', default=None)
        self.parser.add_argument("-c", "--config", dest="config",
                                 help=("configuration file associcated with "
                                       "each samples file."),
                                 nargs='+', default=None)
        self.parser.add_argument("--sensitivity", action="store_true",
                                 help="generate sky sensitivities for HL, HLV",
                                 default=False)
        self.parser.add_argument("--gracedb", dest="gracedb",
                                 help="gracedb of the event", default=None)
        self.parser.add_argument("--psd", dest="psd",
                                 help="psd files used", nargs='+', default=None)
        self.parser.add_argument("--calibration", dest="calibration",
                                 help="files for the calibration envelope",
                                 nargs="+", default=None)

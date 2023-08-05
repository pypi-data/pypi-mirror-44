#!/usr/bin/env python3

"""A utility for dealing with provisioning profiles"""

from enum import Enum

import copy
import os
import plistlib
import shutil
import subprocess
import sys
import tempfile


class ProvisioningType(Enum):
    """Enum representing the type of provisioning profile."""
    IOS_DEVELOPMENT = 1
    APP_STORE_DISTRIBUTION = 3
    AD_HOC_DISTRIBUTION = 5
    ENTERPRISE_DISTRIBUTION = 7


class ProvisioningProfile(object):
    """Represents a provisioning profile."""

    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
        self.file_name = os.path.basename(self.file_path)
        self.xml = None
        self._contents = None
        self._load_xml()
        self._load_contents_dict()
        self._parse_contents()

    def contents(self):
        """Return a copy of the content dict."""
        return copy.deepcopy(self._contents)

    @property
    def profile_type(self):
        if self.provisions_all_devices:
            return ProvisioningType.ENTERPRISE_DISTRIBUTION
        elif not self.entitlements.get("get-task-allow") and self.provisioned_devices:
            return ProvisioningType.AD_HOC_DISTRIBUTION
        elif not self.entitlements.get("get-task-allow") and not self.provisioned_devices:
            return ProvisioningType.APP_STORE_DISTRIBUTION
        elif self.entitlements.get("get-task-allow") and self.provisioned_devices:
            return ProvisioningType.IOS_DEVELOPMENT

    def _parse_contents(self):
        """Parse the contents of the profile."""
        self.app_id_name = self._contents.get("AppIDName")
        self.application_identifier_prefix = self._contents.get("ApplicationIdentifierPrefix")
        self.creation_date = self._contents.get("CreationDate")
        self.platform = self._contents.get("Platform")
        self.developer_certificates = self._contents.get("DeveloperCertificates")
        self.entitlements = self._contents.get("Entitlements")
        self.expiration_date = self._contents.get("ExpirationDate")
        self.name = self._contents.get("Name")
        self.team_identifier = self._contents.get("TeamIdentifier")
        self.team_name = self._contents.get("TeamName")
        self.time_to_live = self._contents.get("TimeToLive")
        self.uuid = self._contents.get("UUID")
        self.version = self._contents.get("Version")
        self.provisioned_devices = self._contents.get("ProvisionedDevices")
        self.provisions_all_devices = True if self._contents.get("ProvisionsAllDevices") else False

    def _load_xml(self):
        """Load the XML contents of a provisioning profile."""
        if not os.path.exists(self.file_path):
            raise Exception(f"File does not exist: {self.file_path}")

        security_cmd = f'security cms -D -i "{self.file_path}" 2> /dev/null'
        self.xml = subprocess.check_output(
            security_cmd,
            universal_newlines=True,
            shell=True
        ).strip()

    def _load_contents_dict(self):
        """Return the contents of a provisioning profile."""
        self._contents = plistlib.loads(self.xml.encode())


def profiles(profiles_dir = None):
    """Returns a list of all currently installed provisioning profiles."""
    if profiles_dir:
        dir_path = os.path.expanduser(profiles_dir)
    else:
        user_path = os.path.expanduser('~')
        dir_path = os.path.join(user_path, 
                                "Library", 
                                "MobileDevice", 
                                "Provisioning Profiles")
        
    profiles = []
    for profile in os.listdir(dir_path):
        full_path = os.path.join(dir_path, profile)
        _, ext = os.path.splitext(full_path)
        if ext == ".mobileprovision":
            provisioning_profile = ProvisioningProfile(full_path)
            profiles.append(provisioning_profile)

    return profiles


def diff(a_path, b_path, ignore_keys=None, tool_override=None):
    """Diff two provisioning profiles."""

    if tool_override is None:
        diff_tool = "opendiff"
    else:
        diff_tool = tool_override

    profile_a = ProvisioningProfile(a_path)
    profile_b = ProvisioningProfile(b_path)

    if ignore_keys is None:
        a_xml = profile_a.xml
        b_xml = profile_b.xml
    else:
        a_dict = profile_a.contents()
        b_dict = profile_b.contents()

        for key in ignore_keys:
            try:
                del a_dict[key]
            except:
                pass
            try:
                del b_dict[key]
            except:
                pass

        a_xml = plistlib.dumps(a_dict)
        b_xml = plistlib.dumps(b_dict)

    temp_dir = tempfile.mkdtemp()

    a_temp_path = os.path.join(temp_dir, profile_a.file_name)
    b_temp_path = os.path.join(temp_dir, profile_b.file_name)

    with open(a_temp_path, 'w') as temp_profile:
        temp_profile.write(a_xml)

    with open(b_temp_path, 'w') as temp_profile:
        temp_profile.write(b_xml)

    # We deliberately don't wrap the tool so that arguments work as well
    diff_command = '%s "%s" "%s"' % (diff_tool, a_temp_path, b_temp_path)

    try:
        diff_contents = subprocess.check_output(
            diff_command,
            universal_newlines=True,
            shell=True
        ).strip()
    except subprocess.CalledProcessError as ex:
        # Diff tools usually return a non-0 exit code if there are differences,
        # so we just swallow this error
        diff_contents = ex.output

    # Cleanup
    shutil.rmtree(temp_dir)

    return diff_contents


def value_for_key(profile_path, key):
    """Return the value for a given key"""

    profile = ProvisioningProfile(profile_path)

    try:
        value = profile.contents()[key]
        return value
    except KeyError:
        return None


def decode(profile_path, xml=True):
    """Decode a profile, returning as a dictionary if xml is set to False."""

    profile = ProvisioningProfile(profile_path)

    if xml:
        return profile.xml
    else:
        return profile.contents()


if __name__ == "__main__":
    print("This should only be used as a module.")
    sys.exit(1)

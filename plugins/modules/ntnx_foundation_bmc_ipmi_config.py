#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_bmc_ipmi_config
short_description: Nutanix module which configures IPMI IP address on BMC of nodes.
version_added: 1.1.0
description: 'Configures IPMI IP address on BMC of nodes.'
options:
  ipmi_user:
    description:
      - ipmi username of given nodes
    type: str
    required: true
  ipmi_netmask:
    description:
      - ipmi netmask of given nodes
    type: str
    required: true
  blocks:
    description:
        - set the list of blocks
    type: list
    elements: dict
    required: true
    suboptions:
        block_id:
          description:
            - block id
          type: str
          required: false
        nodes:
          description:
            - list of nodes
          type: list
          elements: dict
          required: true
          suboptions:
            ipmi_mac:
              description:
                - ipmi mac address
              type: str
              required: true
            ipmi_configure_now:
              description:
                - configure ipmi now or later
              type: bool
              default: true
            ipmi_ip:
              description:
                - ipmi ip address to be set
              type: str
              required: true
  ipmi_gateway:
    description:
      - ipmi gateway of given nodes
    type: str
    required: true
  ipmi_password:
    description:
      - ipmi password of given nodes
    type: str
    required: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_foundation_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
"""

RETURN = r"""

"""
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.foundation.base_module import FoundationBaseModule  # noqa: E402
from ..module_utils.v3.foundation.bmc_ipmi_config import BMC  # noqa: E402


def get_module_spec():
    node_spec = dict(
        ipmi_mac=dict(type="str", required=True),
        ipmi_ip=dict(type="str", required=True),
        ipmi_configure_now=dict(type="bool", required=False, default=True),
    )

    block_spec = dict(
        block_id=dict(type="str", required=False),
        nodes=dict(type="list", required=True, options=node_spec, elements="dict"),
    )

    module_args = dict(
        ipmi_user=dict(type="str", required=True),
        ipmi_netmask=dict(type="str", required=True),
        blocks=dict(type="list", required=True, options=block_spec, elements="dict"),
        ipmi_gateway=dict(type="str", required=True),
        ipmi_password=dict(type="str", required=True, no_log=True),
        timeout=dict(type="str", required=False),
    )

    return module_args


def configure_ipmi(module, result):
    bmc = BMC(module)
    spec, error = bmc.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating IPMI spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    timeout = module.params["timeout"]

    if timeout <= 60:
        timeout = 120

    resp = bmc.configure_ipmi(spec, timeout)

    result["changed"] = True
    result["response"] = resp


def run_module():
    module = FoundationBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }
    configure_ipmi(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

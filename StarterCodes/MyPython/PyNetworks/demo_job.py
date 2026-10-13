#!/usr/bin/env python3

"""
pyATS Job File - Network Automation Test Suite
"""

import os
from pyats.easypy import run

def main(runtime):
    """Main job function"""
    
    # Get testbed file
    testbed_file = runtime.args.testbed_file or 'testbed.yaml'
    
    # Run test scripts
    run(
        testscript='network_connectivity_test.py',
        runtime=runtime,
        testbed=testbed_file,
        task_id='ConnectivityTests'
    )
    
    run(
        testscript='interface_verification_test.py', 
        runtime=runtime,
        testbed=testbed_file,
        task_id='InterfaceTests'
    )
    
    run(
        testscript='protocol_verification_test.py',
        runtime=runtime,
        testbed=testbed_file,
        task_id='ProtocolTests'
    )

if __name__ == '__main__':
    import argparse
    from pyats.easypy import main as easypy_main
    
    parser = argparse.ArgumentParser(description='Network Test Job')
    parser.add_argument('--testbed-file', 
                       help='Testbed YAML file',
                       default='testbed.yaml')
    
    # Run the job
    easypy_main()

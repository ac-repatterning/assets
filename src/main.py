"""Module main.py"""
import datetime
import logging
import os
import sys

import boto3


def main():
    """
    Entry Point<br>
    -----------<br>

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)
    logger.info('Starting: %s', datetime.datetime.now().isoformat(timespec='microseconds'))

    codes = src.acquire.interface.Interface(
        service=service, s3_parameters=s3_parameters, arguments=arguments).exc()

    src.cartography.interface.Interface(
        s3_parameters=s3_parameters, connector=connector).exc(codes=codes)

    # Transfer
    src.transfer.interface.Interface(
      connector=connector, service=service, s3_parameters=s3_parameters, arguments=arguments).exc()

    # Delete Cache Points
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    # Paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import src.acquire.interface
    import src.cartography.interface
    import src.elements.service as sr
    import src.elements.s3_parameters as s3p
    import src.functions.cache
    import src.preface.interface
    import src.transfer.interface

    connector: boto3.session.Session
    s3_parameters: s3p
    service: sr.Service
    arguments: dict
    connector, s3_parameters, service, arguments = src.preface.interface.Interface().exc()

    main()

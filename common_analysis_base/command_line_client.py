import argparse
import importlib
import importlib.machinery
import logging
import pprint

PROGRAM_NAME = 'Common Analysis CLI test client'
PROGRAM_VERSION = '1.0'
PROGRAM_DESCRIPTION = 'Simple test client to run common analysis modules from the command line'


def _setup_argparser():
    parser = argparse.ArgumentParser(description='{} - {}'.format(PROGRAM_NAME, PROGRAM_DESCRIPTION))
    parser.add_argument('-V', '--version', action='version', version='{} {}'.format(PROGRAM_NAME, PROGRAM_VERSION))
    parser.add_argument('-l', '--log_file',
                        help='path to log file')
    parser.add_argument('-L', '--log_level',
                        help='define the log level [DEBUG,INFO,WARNING,ERROR]',
                        default='WARNING')
    parser.add_argument('-a', '--analysis-module',
                        help='name of the analysis module which should be loaded')
    parser.add_argument('-f', '--file',
                        help='path of the file that should be analyzed by the analysis module')
    parser.add_argument('-u', '--url',
                        help='URL that should be analyzed by the analysis module')
    parser.add_argument('-i', '--ip',
                        help='IPv4/IPv6 that should be analyzed by the analysis module')
    parser.add_argument('-d', '--domain',
                        help='Domain that should be analyzed by the analysis module')
    return parser.parse_args()


def _setup_logging(args):
    log_level = getattr(logging, args.log_level.upper(), None)
    log_file = getattr(args, 'log_file', None)
    log_format = logging.Formatter(fmt='[%(asctime)s][%(module)s][%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.INFO)
    console_log.setFormatter(log_format)
    logger.addHandler(console_log)
    if log_file:
        file_log = logging.FileHandler(args.log_file)
        file_log.setLevel(log_level)
        file_log.setFormatter(log_format)
        logger.addHandler(file_log)


def _load_analysis_class_from_module(args):
    logger = logging.getLogger('')
    analysis_module_name = getattr(args, 'analysis_module', None)
    if analysis_module_name is None:
        logger.error('No analysis module specified. Terminating.')
        exit(1)
    try:
        logger.info('Initializing analysis module: %s', analysis_module_name)
        module = importlib.import_module(analysis_module_name)
        return getattr(module, 'analysis_class')
    except ImportError as e:
        logger.error('Module %s can not be imported. Terminating.', analysis_module_name)
        raise e
    except AttributeError as e:
        logger.error('No analysis class found in module %s. Terminating.', analysis_module_name)
        raise e


def _analyze_file(analyzer, file_path):
    logger = logging.getLogger('')
    if analyzer.can_analyze_file():
        logger.info('Analyzing file: %s', file_path)
        return analyzer.analyze_file(file_path)
    else:
        logger.warn('File analysis requested, but analysis module can not analyze files. Skipping.')


def _analyze_url(analyzer, url):
    logger = logging.getLogger('')
    if analyzer.can_analyze_url():
        logger.info('Analyzing URL: %s', url)
        return analyzer.analyze_url(url)
    else:
        logger.warn('URL analysis requested, but analysis module can not analyze URLs. Skipping.')


def _analyze_ip(analyzer, ip):
    logger = logging.getLogger('')
    if analyzer.can_analyze_ip():
        logger.info('Analyzing IP: %s', ip)
        return analyzer.analyze_ip(ip)
    else:
        logger.warn('IP analysis requested, but analysis module can not analyze IPs. Skipping.')


def _analyze_domain(analyzer, domain):
    logger = logging.getLogger('')
    if analyzer.can_analyze_domain():
        logger.info('Analyzing domain: %s', domain)
        return analyzer.analyze_domain(domain)
    else:
        logger.warn('Domain analysis requested, but analysis module can not analyze domains. Skipping.')


def _pretty_print(object):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(object)


def _analyze(args, analysis_class):
    analyzer = analysis_class()
    file_path = getattr(args, 'file', None)
    url = getattr(args, 'url', None)
    ip = getattr(args, 'ip', None)
    domain = getattr(args, 'domain', None)
    if file_path:
        result = _analyze_file(analyzer, file_path)
        _pretty_print(result)
    if url:
        result = _analyze_url(analyzer, url)
        _pretty_print(result)
    if ip:
        result = _analyze_ip(analyzer, ip)
        _pretty_print(result)
    if domain:
        result = _analyze_domain(analyzer, domain)
        _pretty_print(result)


def _main():
    args = _setup_argparser()
    _setup_logging(args)
    analysis_class = _load_analysis_class_from_module(args)
    _analyze(args, analysis_class)
    exit(0)

if __name__ == '__main__':
    _main()

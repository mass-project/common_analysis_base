import datetime


class AnalysisPlugin:
    """
    All analysis plugins which are implemented according to our common code guidelines should be derived from this class.
    This way we can make sure that the implemented plugins follow the defined criteria and can be used in different applications.

    Note that this class does neither define nor implement any specific analysis method. Instead it provides a common interface to find out which
    analysis methods are supported by the derived analysis plugin class. Specifically, the user of any derived class may call the ``can_analyze_xyz`` methods
    to find out which types of analysis can be executed by the analysis plugin.

    :ivar plugin_version: The version number of the analysis plugin
    :ivar system_version: Optional version number of an external system which is used by the plugin, i.e. the version of an AV signature database.
    """
    def __init__(self, plugin_version, system_version=None):
        """
        Initialize the analysis plugin.

        The __init__ method of the superclass will set the ``plugin_version`` and optionally the ``system_version`` variables.

        :param plugin_version: plugin_version: The version number of the analysis plugin
        :param system_version: Optional version number of an external system which is used by the plugin, i.e. the version of an AV signature database.
        """
        self.plugin_version = plugin_version
        self.system_version = system_version

    def can_analyze_file(self):
        """
        Returns true if the analysis plugin supports the analysis of files.

        :return: True if file analysis is supported, False otherwise
        """
        return hasattr(self, "analyze_file") and callable(getattr(self, "analyze_file"))

    def can_analyze_url(self):
        """
        Returns true if the analysis plugin supports the analysis of URLs.

        :return: True if URL analysis is supported, False otherwise
        """
        return hasattr(self, "analyze_url") and callable(getattr(self, "analyze_url"))

    def can_analyze_ip(self):
        """
        Returns true if the analysis plugin supports the analysis of IP addresses.

        :return: True if IP address analysis is supported, False otherwise
        """
        return hasattr(self, "analyze_ip") and callable(getattr(self, "analyze_ip"))

    def can_analyze_domain(self):
        """
        Returns true if the analysis plugin supports the analysis of domain names.

        :return: True if domain name analysis is supported, False otherwise
        """
        return hasattr(self, "analyze_domain") and callable(getattr(self, "analyze_domain"))

    def prepare_analysis_report_dictionary(self):
        """
        Create and return a dictionary that can be used to return the analysis report.

        :return: Dictionary with analysis metadata
        """
        result = {
            'plugin_version': self.plugin_version,
            'analysis_date': datetime.datetime.now()
        }
        if self.system_version is not None:
            result['system_version'] = self.system_version
        return result


class FileAnalysisMixin:
    """
    Simple mixin which should be used by analysis plugins when implementing file analysis.

    """
    def analyze_file(self, file_path):
        """
        Placeholder function for file analysis. This function should be overwritten by the analysis plugin to execute the
        plugin-specific analysis procedure and return an analysis report. Will raise a ``NotImplementedError`` if used when not overwritten.

        :param file_path: Path to the file which should be analyzed. Can be an absolute path or relative to the current working directory.
        :type file_path: str
        :return: Dictionary with analysis report
        """
        raise NotImplementedError('This method is not implemented.')


class URLAnalysisMixin:
    """
    Simple mixin which should be used by analysis plugins when implementing URL analysis.

    """
    def analyze_url(self, url):
        """
        Placeholder function for URL analysis. This function should be overwritten by the analysis plugin to execute the
        plugin-specific analysis procedure and return an analysis report. Will raise a ``NotImplementedError`` if used when not overwritten.

        :param url: URL that should be analyzed
        :type url: str
        :return: Dictionary with analysis report
        """
        raise NotImplementedError('This method is not implemented.')


class IPAnalysisMixin:
    """
    Simple mixin which should be used by analysis plugins when implementing IP address analysis.

    """
    def analyze_ip(self, ip):
        """
        Placeholder function for IP address analysis. This function should be overwritten by the analysis plugin to execute the
        plugin-specific analysis procedure and return an analysis report. Will raise a ``NotImplementedError`` if used when not overwritten.

        :param ip: IPv4 address or IPv6 address that should be analyzed
        :type ip: IPv4Address or IPv6Address
        :return: Dictionary with analysis report
        """
        raise NotImplementedError('This method is not implemented.')


class StringAnalysisMixin:
    """
    Simple mixin which should be used by analysis plugins when implementing string analysis.

    """
    def analyze_string(self, string):
        """
        Placeholder function for string analysis. This function should be overwritten by the analysis plugin to execute the
        plugin-specific analysis procedure and return an analysis report. Will raise a ``NotImplementedError`` if used when not overwritten.

        :param string: string that should be analyzed
        :type string: string
        :return: Dictionary with analysis report
        """
        raise NotImplementedError('This method is not implemented.')



class DomainAnalysisMixin:
    """
    Simple mixin which should be used by analysis plugins when implementing domain name analysis.

    """
    def analyze_domain(self, domain):
        """
        Placeholder function for domain name analysis. This function should be overwritten by the analysis plugin to execute the
        plugin-specific analysis procedure and return an analysis report. Will raise a ``NotImplementedError`` if used when not overwritten.

        :param domain: Domain name which should be analyzed.
        :type domain: str
        :return: Dictionary with analysis report
        """
        raise NotImplementedError('This method is not implemented.')


class AnalysisPluginFile(AnalysisPlugin, FileAnalysisMixin):
    """
    Convenience class that can be used as the superclass for file analysis plugins. Derived from :py:class:`.AnalysisPlugin` and :py:class:`.FileAnalysisMixin`
    """
    pass


class AnalysisPluginURL(AnalysisPlugin, URLAnalysisMixin):
    """
    Convenience class that can be used as the superclass for URL analysis plugins. Derived from :py:class:`.AnalysisPlugin` and :py:class:`.URLAnalysisMixin`
    """
    pass


class AnalysisPluginIP(AnalysisPlugin, IPAnalysisMixin):
    """
    Convenience class that can be used as the superclass for IP address analysis plugins. Derived from :py:class:`.AnalysisPlugin` and :py:class:`.IPAnalysisMixin`
    """
    pass


class AnalysisPluginDomain(AnalysisPlugin, DomainAnalysisMixin):
    """
    Convenience class that can be used as the superclass for domain name analysis plugins. Derived from :py:class:`.AnalysisPlugin` and :py:class:`.DomainAnalysisMixin`
    """
    pass


class AnalysisPluginString(AnalysisPlugin, StringAnalysisMixin):
    """
    Convenience class that can be used as the superclass for string analysis plugins. Derived from :py:class:`.AnalysisPlugin` and :py:class:`.StringAnalysisMixin`
    """
    pass

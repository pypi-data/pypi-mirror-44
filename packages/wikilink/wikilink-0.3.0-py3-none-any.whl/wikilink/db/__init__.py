"""
	wikilink
	~~~~~~~~

	wikilink is a multiprocessing web-scraping application to scrape wiki pages and 
	find minimum number of links between two given wiki pages.

	:copyright: (c) 2016 - 2019 by Tran Ly VU. All Rights Reserved.
	:license: Apache License 2.0.
"""

from .connection import Connection
from .page import Page
from .link import Link

__all__ = ["Connection", "Page", "Link"]
__author__ = "Tran Ly Vu (vutransingapore@gmail.com)"
__copyright__ = "Copyright (c) 2016 - 2019 Tran Ly Vu. All Rights Reserved."
__credits__ = ["Tranlyvu"]
__license__ = "Apache License 2.0"
__maintainer__ = "Tran Ly Vu"
__email__ = "vutransingapore@gmail.com"
__status__ = "Beta"


"""
Client for the ISBNdb APi
"""

import re
import urllib2 as urllib

BASE_URL = "http://isbndb.com/api/"
BOOK_URL = "".join([BASE_URL, "books.xml"])
SUBJECTS_URL = "".join([BASE_URL, "subjects.xml"])
CATEGORIES_URL = "".join([BASE_URL, "categories.xml"])
AUTHORS_URL = "".join([BASE_URL, "authors.xml"])
PUBLISHERS_URL = "".join([BASE_URL, "publishers.xml"])

COMMON_RESULTS_REGEX = "keystats|args"

BOOKS_RESULTS_REGEX = "details|texts|prices|pricehistory|subjects|marc|authors"
BOOKS_INDEX1_REGEX = "isbn|title|combined|full|book_id|person_id|publisher_id|subject_id|dewey_decimal|lcc_number"

BOOKS_RESULTS_REGEX_OBJECT = re.compile("|".join([COMMON_RESULTS_REGEX,
                                                 BOOKS_RESULTS_REGEX]))
BOOKS_INDEX1_REGEX_OBJECT = re.compile(BOOKS_INDEX1_REGEX)

SUBJECTS_RESULTS_REGEX = "categories|structure"
SUBJECTS_INDEX1_REGEX = "name|category_id|subject_id"

SUBJECTS_RESULTS_REGEX_OBJECT = re.compile("|".join([COMMON_RESULTS_REGEX,
                                                 SUBJECTS_RESULTS_REGEX]))
SUBJECTS_INDEX1_REGEX_OBJECT = re.compile(SUBJECTS_INDEX1_REGEX)

CATEGORIES_RESULTS_REGEX = "details|subcategories"
CATEGORIES_INDEX1_REGEX = "name|category_id|parent_id"

CATEGORIES_RESULTS_REGEX_OBJECT = re.compile("|".join([COMMON_RESULTS_REGEX,
                                                 CATEGORIES_RESULTS_REGEX]))
CATEGORIES_INDEX1_REGEX_OBJECT = re.compile(CATEGORIES_INDEX1_REGEX)

AUTHORS_RESULTS_REGEX = "details|categories|subjects"
AUTHORS_INDEX1_REGEX = "name|person_id"

AUTHORS_RESULTS_REGEX_OBJECT = re.compile("|".join([COMMON_RESULTS_REGEX,
                                                 AUTHORS_RESULTS_REGEX]))
AUTHORS_INDEX1_REGEX_OBJECT = re.compile(AUTHORS_INDEX1_REGEX)

PUBLISHERS_RESULTS_REGEX = "details|categories"
PUBLISHERS_INDEX1_REGEX = "name|publisher_id"

PUBLISHERS_RESULTS_REGEX_OBJECT = re.compile("|".join([COMMON_RESULTS_REGEX,
                                                 PUBLISHERS_RESULTS_REGEX]))
PUBLISHERS_INDEX1_REGEX_OBJECT = re.compile(PUBLISHERS_INDEX1_REGEX)


class ISBNdbClient(object):

    """
    Class for the ISBNdbAPI
    """

    def __init__(self, access_key):

        """
        Constructor method for the ISBNdbClient
        """

        self._access_key = None
        self.access_key_variable = None
        self._set_access_key(access_key)

        self.results = None
        self.index1 = None
        self.value1 = None
        self.url = None
        self.page = None

    def _set_access_key(self, value):

        """
        Checks if value is a string and sets the _acces_key attribute to it if
        that is the case. Also it sets the access_key_variable attribute.

        @param value: access_key
        """

        if isinstance(value, str):
            self._access_key = value
            self.access_key_variable = "".join(["?", "access_key", "=", value])
        else:
            raise TypeError("access_key must be a string")

    def _get_access_key(self):

        """
        Return the _accss_key attribute.
        """

        return self._access_key

    def _del_access_key(self):

        """
        Deletes the _acces_key and the access_key_varialbe attribute.
        """

        del self._access_key
        del self.access_key_variable

    access_key = property(_get_access_key, _set_access_key, _del_access_key)

    def _request(self, index1, value1, results_regex_object,
                 index1_regex_object, base_url, results=None, page=None):

        """
        Creates the url and returns it results.

        @param index1 the index1 of the request, needs to be a string
        @param value1 the value1 of the request, needs to be a string
        @param results_regex_object the regex to match results, needs to be a
        regex object
        @param index1_regex_object the regex to match index1, needs to be a
        regex object
        @param base_url the base url, needs to be a string
        @param results if None, don't include results, else include it. Needs
        to be None or a string.
        @param page the page_number must be None or a int
        """

        if results is not None:
            try:
                if results_regex_object.match(results):
                    self.results = results
                else:
                    raise ValueError(" ".join(["results must match",
                                     results_regex_object.pattern]))
            except AttributeError:
                raise TypeError("results_regex_object must be regex object")
        else:
            self.results = False

        if isinstance(index1, str):
            try:
                if index1_regex_object.match(index1):
                    self.index1 = index1
                else:
                    raise ValueError(" ".join(["index1 must match",
                                     index1_regex_object.pattern]))
            except AttributeError:
                raise TypeError("index1_regex_object must be a regex object")
        else:
            raise TypeError("index1 must be a string")

        if page is not None:
            if isinstance(page, int):
                self.page = page
            else:
                raise TypeError("page must be a int")
        else:
            self.page = False

        if isinstance(value1, str):
            self.value1 = value1
        else:
            raise TypeError("value1 must be a string")

        if self.results is not False:
            results_variable = "".join(["results", "=", self.results])

        index1_variable = "".join(["index1", "=", self.index1])

        value1_variable = "".join(["value1", "=", self.value1])

        if self.page is not False:
            page_variable = "".join(["page_number", "=", self.page])

        if self.results is not False:
            variables = "&".join([results_variable, index1_variable,
                                  value1_variable])
        else:
            variables = "&".join([index1_variable, value1_variable])

        if self.page is not False:
            variables = "&".join([variables, page_variable])

        variables = "&".join([self.access_key_variable, variables])

        self.url = "".join([base_url, variables])

        return "".join(urllib.urlopen(self.url).readlines()).replace("\n", "")

    def request_book(self, index1, value1, results=None, page=None):

        """
        Requests book collections

        @param index1 the index1 of the request, needs to be a string and
        match isbn|title|combined|full|book_id|person_id|publisher_id|subject_id|dewey_decimal|lcc_number
        @param value1 the value 1 of the request, needs to be a string
        @param results if None, don't include results, else include it. Needs
        to be None or a string, that matches keystats|args|details|texts|prices|pricehistory|subjects|marc|authors.
        @param page the page_number must be None or a int
        """

        return self._request(index1=index1, value1=value1,
                             results_regex_object=BOOKS_RESULTS_REGEX_OBJECT,
                             index1_regex_object=BOOKS_INDEX1_REGEX_OBJECT,
                             base_url=BOOK_URL, results=results, page=page)

    def request_subjects(self, index1, value1, results=None, page=None):

        """
        Request subjects collections

        @param index1 the index1 of the request, needs to be a string and
        match name|category_id|subject_id
        @param value1 the value1 of the request, needs to be a string
        @param results if None, don't include results, else include it. Needs
        to be None or a string, that matches keystats|args|categories|structure
        @param page the page_number must be None or a int
        """

        return self._request(index1=index1, value1=value1,
                             results_regex_object=SUBJECTS_RESULTS_REGEX_OBJECT,
                             index1_regex_object=SUBJECTS_INDEX1_REGEX_OBJECT,
                             base_url=SUBJECTS_URL, results=results, page=page)

    def request_categories(self, index1, value1, results=None, page=None):

        """
        Request categories collections

        @param index1 the index1 of the request, needs to be a string and match
        name|category_id|parent_id
        @param value the value1 of the request, needs to be a string
        @param results if None, don't include results, else include it. Needs
        to be None or string, that matches keystats|args|details|subcategories
        @param page the page_number must be None or a int
        """

        return self._request(index1=index1, value1=value1,
                             results_regex_object=CATEGORIES_RESULTS_REGEX_OBJECT,
                             index1_regex_object=CATEGORIES_INDEX1_REGEX_OBJECT,
                             base_url=CATEGORIES_URL, results=results, page=page)

    def request_authors(self, index1, value1, results=None, page=None):
        """
        Request authors collections

        @param index1 the index1 of the request, needs to be a string and match
        name|person_id
        @param value1 the value1 of the request, needs to be a string
        @param results if None, don't include results, else include it. Needs
        to be None or string, that matches keystats|args|details|categories|subjects
        @param page the page_number must be None or a int
        """

        return self._request(index1=index1, value1=value1,
                             results_regex_object=AUTHORS_RESULTS_REGEX_OBJECT,
                             index1_regex_object=AUTHORS_INDEX1_REGEX_OBJECT,
                             base_url=AUTHORS_URL, results=results, page=page)

    def request_publishers(self, index1, value1, results=None, page=None):

        """
        Request publishers collections

        @param index1 the index1 of the request, needs to be a string and match
        name|publisher_id
        @param value1 the value1 of the request, needs to be a string
        @param results if None, don't include results, else include it. Needs
        to be None or string, that matches keystats|args|details|categories
        @param page the page_number must be None or a int
        """

        return self._request(index1=index1, value1=value1,
                             results_regex_object=PUBLISHERS_RESULTS_REGEX_OBJECT,
                             index1_regex_object=PUBLISHERS_INDEX1_REGEX_OBJECT,
                             base_url=PUBLISHERS_URL, results=results, page=page)

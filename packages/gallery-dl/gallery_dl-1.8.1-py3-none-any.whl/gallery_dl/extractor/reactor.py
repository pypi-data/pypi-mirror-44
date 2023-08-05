# -*- coding: utf-8 -*-

# Copyright 2019 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Generic extractors for *reactor sites"""

from .common import Extractor, Message, SharedConfigMixin
from .. import text
import urllib.parse
import random
import time
import json


BASE_PATTERN = r"(?:https?://)?([^/.]+\.reactor\.cc)"


class ReactorExtractor(SharedConfigMixin, Extractor):
    """Base class for *reactor.cc extractors"""
    basecategory = "reactor"
    filename_fmt = "{post_id}_{num:>02}{title[:100]:?_//}.{extension}"
    archive_fmt = "{post_id}_{num}"

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.root = "http://" + match.group(1)
        self.session.headers["Referer"] = self.root

        self.wait_min = self.config("wait-min", 3)
        self.wait_max = self.config("wait-max", 6)
        if self.wait_max < self.wait_min:
            self.wait_max = self.wait_min

        if not self.category:
            # set category based on domain name
            netloc = urllib.parse.urlsplit(self.root).netloc
            self.category = netloc.rpartition(".")[0]

    def items(self):
        data = self.metadata()
        yield Message.Version, 1
        yield Message.Directory, data
        for post in self.posts():
            for image in self._parse_post(post):
                url = image["file_url"]
                image.update(data)
                yield Message.Url, url, text.nameext_from_url(url, image)

    def metadata(self):
        """Collect metadata for extractor-job"""
        return {}

    def posts(self):
        """Return all relevant post-objects"""
        return self._pagination(self.url)

    def _pagination(self, url):
        while True:
            time.sleep(random.uniform(self.wait_min, self.wait_max))

            response = self.request(url)
            if response.history:
                # sometimes there is a redirect from
                # the last page of a listing (.../tag/<tag>/1)
                # to the first page (.../tag/<tag>)
                # which could cause an endless loop
                cnt_old = response.history[0].url.count("/")
                cnt_new = response.url.count("/")
                if cnt_old == 5 and cnt_new == 4:
                    return
            page = response.text

            yield from text.extract_iter(
                page, '<div class="uhead">', '<div class="ufoot">')

            try:
                pos = page.index("class='next'")
                pos = page.rindex("class='current'", 0, pos)
                url = self.root + text.extract(page, "href='", "'", pos)[0]
            except (ValueError, TypeError):
                return

    def _parse_post(self, post):
        post, _, script = post.partition('<script type="application/ld+json">')
        images = text.extract_iter(post, '<div class="image">', '</div>')
        script = script[:script.index("</")].strip()

        try:
            data = json.loads(script)
        except ValueError:
            try:
                # remove control characters and escape backslashes
                mapping = dict.fromkeys(range(32))
                script = script.translate(mapping).replace("\\", "\\\\")
                data = json.loads(script)
            except ValueError as exc:
                self.log.warning("Unable to parse JSON data: %s", exc)
                return

        num = 0
        date = data["datePublished"]
        user = data["author"]["name"]
        description = text.unescape(data["description"])
        title, _, tags = text.unescape(data["headline"]).partition(" / ")
        post_id = text.parse_int(
            data["mainEntityOfPage"]["@id"].rpartition("/")[2])

        if not tags:
            title, tags = tags, title

        for image in images:
            url = text.extract(image, ' src="', '"')[0]
            if not url:
                continue
            width = text.extract(image, ' width="', '"')[0]
            height = text.extract(image, ' height="', '"')[0]
            image_id = url.rpartition("-")[2].partition(".")[0]
            num += 1

            if image.startswith("<iframe "):  # embed
                url = "ytdl:" + text.unescape(url)

            yield {
                "file_url": url,
                "post_id": post_id,
                "image_id": text.parse_int(image_id),
                "width": text.parse_int(width),
                "height": text.parse_int(height),
                "title": title,
                "description": description,
                "tags": tags,
                "date": date,
                "user": user,
                "num": num,
            }


class ReactorTagExtractor(ReactorExtractor):
    """Extractor for tag searches on *reactor.cc sites"""
    subcategory = "tag"
    directory_fmt = ("{category}", "{search_tags}")
    archive_fmt = "{search_tags}_{post_id}_{num}"
    pattern = BASE_PATTERN + r"/tag/([^/?&#]+)"
    test = ("http://anime.reactor.cc/tag/Anime+Art",)

    def __init__(self, match):
        ReactorExtractor.__init__(self, match)
        self.tag = match.group(2)

    def metadata(self):
        return {"search_tags": text.unescape(self.tag).replace("+", " ")}


class ReactorSearchExtractor(ReactorTagExtractor):
    """Extractor for search results on *reactor.cc sites"""
    subcategory = "search"
    directory_fmt = ("{category}", "search", "{search_tags}")
    archive_fmt = "s_{search_tags}_{post_id}_{num}"
    pattern = BASE_PATTERN + r"/search(?:/|\?q=)([^/?&#]+)"
    test = ("http://anime.reactor.cc/search?q=Art",)


class ReactorUserExtractor(ReactorExtractor):
    """Extractor for all posts of a user on *reactor.cc sites"""
    subcategory = "user"
    directory_fmt = ("{category}", "user", "{user}")
    pattern = BASE_PATTERN + r"/user/([^/?&#]+)"
    test = ("http://anime.reactor.cc/user/Shuster",)

    def __init__(self, match):
        ReactorExtractor.__init__(self, match)
        self.user = match.group(2)

    def metadata(self):
        return {"user": text.unescape(self.user).replace("+", " ")}


class ReactorPostExtractor(ReactorExtractor):
    """Extractor for single posts on *reactor.cc sites"""
    subcategory = "post"
    pattern = BASE_PATTERN + r"/post/(\d+)"
    test = ("http://anime.reactor.cc/post/3576250",)

    def __init__(self, match):
        ReactorExtractor.__init__(self, match)
        self.post_id = match.group(2)

    def items(self):
        yield Message.Version, 1
        post = self.request(self.url).text
        pos = post.find('class="uhead">')
        for image in self._parse_post(post[pos:]):
            if image["num"] == 1:
                yield Message.Directory, image
            url = image["file_url"]
            yield Message.Url, url, text.nameext_from_url(url, image)


# --------------------------------------------------------------------
# JoyReactor

JR_BASE_PATTERN = r"(?:https?://)?(?:www\.)?(joyreactor\.c(?:c|om))"


class JoyreactorTagExtractor(ReactorTagExtractor):
    """Extractor for tag searches on joyreactor.cc"""
    category = "joyreactor"
    pattern = JR_BASE_PATTERN + r"/tag/([^/?&#]+)"
    test = (
        ("http://joyreactor.cc/tag/Advent+Cirno", {
            "count": ">= 17",
        }),
        ("http://joyreactor.com/tag/Cirno", {
            "url": "a81382a3146da50b647c475f87427a6ca1d737df",
        }),
    )


class JoyreactorSearchExtractor(ReactorSearchExtractor):
    """Extractor for search results on joyreactor.cc"""
    category = "joyreactor"
    pattern = JR_BASE_PATTERN + r"/search(?:/|\?q=)([^/?&#]+)"
    test = (
        ("http://joyreactor.cc/search/Cirno+Gifs", {
            "range": "1-25",
            "count": ">= 20",
        }),
        ("http://joyreactor.com/search?q=Cirno+Gifs", {
            "count": 0,  # no search results on joyreactor.com
        }),
    )


class JoyreactorUserExtractor(ReactorUserExtractor):
    """Extractor for all posts of a user on joyreactor.cc"""
    category = "joyreactor"
    pattern = JR_BASE_PATTERN + r"/user/([^/?&#]+)"
    test = (
        ("http://joyreactor.cc/user/hemantic"),
        ("http://joyreactor.com/user/Tacoman123", {
            "url": "0444158f17c22f08515ad4e7abf69ad2f3a63b35",
        }),
    )


class JoyreactorPostExtractor(ReactorPostExtractor):
    """Extractor for single posts on joyreactor.cc"""
    category = "joyreactor"
    pattern = JR_BASE_PATTERN + r"/post/(\d+)"
    test = (
        ("http://joyreactor.com/post/3721876", {  # single image
            "url": "904779f6571436f3d5adbce30c2c272f6401e14a",
            "keyword": "e8deb51e66325341fe33f6e99938b8548093d34b",
        }),
        ("http://joyreactor.com/post/3713804", {  # 4 images
            "url": "99c614416b959f22001f7da3f68df03b1551abdf",
            "keyword": "c5a6893e2425d31393139e355370e208754eb8fa",
        }),
        ("http://joyreactor.com/post/3726210", {  # gif / video
            "url": "33a48e1eca6cb2d298fbbb6536b3283799d6515b",
            "keyword": "11cfce3f2ea336979ca6cc5da604fbe02aeda345",
        }),
        ("http://joyreactor.com/post/3668724", {  # youtube embed
            "url": "be2589e2e8f3ffcaf41b34bc28bfad850ccea34a",
            "keyword": "889206164b4a180aed6bf6186d2456cf31afbed8",
        }),
        ("http://joyreactor.cc/post/1299", {  # "malformed" JSON
            "url": "d45337fec926159afe11c59e32d259d793dd00b3",
        }),
    )


# --------------------------------------------------------------------
# PornReactor

PR_BASE_PATTERN = r"(?:https?://)?(?:www\.)?(pornreactor\.cc|fapreactor.com)"


class PornreactorTagExtractor(ReactorTagExtractor):
    """Extractor for tag searches on pornreactor.cc"""
    category = "pornreactor"
    pattern = PR_BASE_PATTERN + r"/tag/([^/?&#]+)"
    test = (
        ("http://pornreactor.cc/tag/RiceGnat", {
            "range": "1-25",
            "count": ">= 25",
        }),
        ("http://fapreactor.com/tag/RiceGnat"),
    )


class PornreactorSearchExtractor(ReactorSearchExtractor):
    """Extractor for search results on pornreactor.cc"""
    category = "pornreactor"
    pattern = PR_BASE_PATTERN + r"/search(?:/|\?q=)([^/?&#]+)"
    test = (
        ("http://pornreactor.cc/search?q=ecchi+hentai", {
            "range": "1-25",
            "count": ">= 25",
        }),
        ("http://fapreactor.com/search/ecchi+hentai"),
    )


class PornreactorUserExtractor(ReactorUserExtractor):
    """Extractor for all posts of a user on pornreactor.cc"""
    category = "pornreactor"
    pattern = PR_BASE_PATTERN + r"/user/([^/?&#]+)"
    test = (
        ("http://pornreactor.cc/user/Disillusion", {
            "range": "1-25",
            "count": ">= 25",
        }),
        ("http://fapreactor.com/user/Disillusion"),
    )


class PornreactorPostExtractor(ReactorPostExtractor):
    """Extractor for single posts on pornreactor.cc"""
    category = "pornreactor"
    subcategory = "post"
    pattern = PR_BASE_PATTERN + r"/post/(\d+)"
    test = (
        ("http://pornreactor.cc/post/863166", {
            "url": "9e5f7b374605cbbd413f4f4babb9d1af6f95b843",
            "content": "3e2a09f8b5e5ed7722f51c5f423ff4c9260fb23e",
        }),
        ("http://fapreactor.com/post/863166", {
            "url": "83ff7c87741c05bcf1de6825e2b4739afeb87ed5",
        }),
    )

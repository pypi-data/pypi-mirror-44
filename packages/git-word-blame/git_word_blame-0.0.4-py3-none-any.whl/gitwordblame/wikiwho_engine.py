import sys
from pathlib import Path
import hashlib

from lys import L, render, raw
import git
from mwxml import Dump
from mwtypes.files import reader
from WikiWho.wikiwho import Wikiwho
from WikiWho.examples.process_xml_dump import process_xml_dump
from WikiWho.utils import iter_rev_tokens
from mwpersistence import Token


__all__ = ('get_tokens_authorship',)


HEADER = """<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="fr">
  <siteinfo>
    <sitename>Wikipédia</sitename>
    <dbname>frwiki</dbname>
    <base>https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal</base>
    <generator>MediaWiki 1.33.0-wmf.23</generator>
    <case>first-letter</case>
    <namespaces>
      <namespace key="0" case="first-letter"/>
    </namespaces>
  </siteinfo>"""

FOOTER = """</mediawiki>"""


def convert_to_mwxml(git_commits):
    ## converts to mediawiki xml

    revisions = []
    for i, revision in enumerate(git_commits):
        _, filecontents = revision
        revision = L.revision / (
            L.id / str(i),
            L.timestamp / '2008-01-26T13:36:54Z',
            L.contributor / (
                L.username / "--",
                L.id / str(0),
            ),
            L.model / 'wikitext',
            L.format / 'text/x-wiki',
            # lys doesn't support namespaced attributes for now
            raw('<text xml:space="preserve" bytes="1181">'),
            raw(render(filecontents)),
            raw('</text>'),
        )

        revisions.append(revision)

    xml_tree = (
        raw(HEADER),
        L.page / (
            L.title / '---',
            L.ns / '0',
            L.id / '1',
            revisions,
        ),
        raw(FOOTER),
    )

    return render(xml_tree)


def iter_rev_tokens_and_text(last_rev, raw_text):
    curr_pos = 0
    ltext = raw_text.lower()
    for token in iter_rev_tokens(last_rev):
        next_pos = ltext.index(token.value, curr_pos)
        if next_pos > curr_pos:
            # attribute whitespace around token to token
            yield token, raw_text[curr_pos:next_pos]
        yield token, raw_text[next_pos:next_pos + len(token.value)]
        curr_pos = next_pos + len(token.value)


def get_tokens_authorship(git_commits):
    xml = convert_to_mwxml(git_commits)
    tmp_file = "/tmp/git_export_to_mwxml.xml"
    with open(tmp_file, 'w') as f:
        f.write(xml)
    wikiwho_obj = process_xml_dump(tmp_file)
    _, raw_text = git_commits[-1]
    last_rev = wikiwho_obj.revisions[wikiwho_obj.ordered_revisions[-1]]
    for token, text in iter_rev_tokens_and_text(last_rev, raw_text):
        # TODO: revisions after original
        yield Token(text, revisions=[token.origin_rev_id])

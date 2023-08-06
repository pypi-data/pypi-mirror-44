import os
import re
import jinja2
import delegator
import datetime

class Messages:
    pass


class Context:

    PATTERN = r'(feat|fix|docs|style|refactor|perf|test|chore)\(?(.*[^\)])?\)?: (.*)$'
    PATTERN = r'(?P<prefix>feat|fix|docs|style|refactor|perf|test|chore)\(?(?P<scope>.*[^\)])?\)?: (?P<subject>.*)$'
    TEMPLATE_NAME = 'auto_changelog'

    def __init__(self):
        self._message = ''
        self._parsed = tuple()

    def __get__(self, instance, owner):
        return self

    def __set__(self, instance, message):
        self._message = message

    def parse(self):
        if not self._parsed:
            self._parsed = re.match(self.PATTERN, self._message)

    @property
    def parsed(self):
        self.parse()
        return self._parsed.groupdict()

    def is_valid(self):
        self.parse()
        return bool(self._parsed)


class Tag:

    def __init__(self, message):
        self._message = message
        self.timestamp
        self.tag

    def parse(self):
        timestamp, tag = self.message.split(',')
        self.timestamp = datetime.datetime.fromtimestamp(timestamp)
        self.tag = tag


class Git:

    tags_command = "git tag --format='%(creatordate:raw),%(refname:strip=2)'"  # iso8601-strict
    commits_command = 'git log --pretty=format:"%aI,%s" {last_tag}'
    # git log --pretty=format:"%aI,%s" ...v0.8.0

    def __get__(self, obj):
        self.context = obj.context
        self._tags = []

    def tags(self):
        c = delegator.run(self.tags_command)
        tags = c.out.strip().split('\n')
        self._tags = [Tag(message) for message in tags]

    def commits(self):
        pass

    def messages(self):
        pass


class MdRenderer:
    pass


class BaseChangelog:
    context = Context()
    version_control = Git()


    def renamedder(self, tpl_path, context):
        path, filename = os.path.split(tpl_path)
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or './')
        ).get_template(filename).render(context)

    def write(self, result):
        pass

    def create(self, partial=False):
        context = self.version_control.messages
        result = self.render(self.template_name, context)
        self.write(result)
        # get valid commits messages
        # load template
        # write to file
        pass

from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host("", "project.urls", name="none"),
    host("connect", "connect.urls", name="connect"),
)
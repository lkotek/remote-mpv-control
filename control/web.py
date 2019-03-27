#!/usr/bin/env python3

from bottle import route, run, template, view, static_file, redirect, SimpleTemplate
import sys

run(host=sys.argv[1], port=sys.argv[2])
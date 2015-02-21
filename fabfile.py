#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fabric build script for deploying this bad boy into webfaction.

It's not pretty but it works.

"""

import os
import json

#from django.utils.html import strip_spaces_between_tags
#from fabric.api import *  # oh my god... it's full of stars
from fabric.api import cd, local, get, run, put, env

import secrets

LIBS = (
    "jquery-2.1.3.min.js",
    "lodash.min.js",
    "backbone.js",
    "backbone-tastypie.min.js",
    "jquery.lazyload.min.js",
    "jquery.cookie.min.js",
    "jquery-ui-1.10.3.custom.min.js",
    "mustache.min.js",
    "keyboard.js")


def _config():
    env.user = "inopia"
    env.home = "/home/%s/" % env.user
    #pubkey authentication
    #env.key_filename = "/home/%s/.ssh/id_staging_rsa" % env.user
    env.mysql_user = "inopia_mlfw"
    env.mysql_pass = secrets.MYSQLPASS
    env.hosts = ["mlfw.info"]
    env.appdir = env.home + "webapps/mylittlefacewhen/"
    env.mediadir = env.home + "webapps/mlfw_media/"
    env.staticdir = env.appdir + "mylittlefacewhen/static/"
    env.staticdeploydir = env.home + "webapps/mlfw_static/"

    env.minifier = "yui-compressor -o"

    env.install_db = False
    env.install_app = False
    env.install_media = False
    env.install_static = False

    env.files = []


def production():
    _config()


def db():
    env.files.append("dump.sql.tar.gz")
    env.install_db = True


def media():
    env.files.append("media.tar.gz")
    env.install_media = True


def static():
    env.files.append("static.tar.gz")
    env.install_static = True


def app():
    env.files.append("application.tar.gz")
    env.install_app = True


def update_cache():
    with cd(env.appdir + "mylittlefacewhen/"):
        run("""python2.7 manage.py updatecache""")


def deploy():
    _prepare_deploy()
    _put()
    _install()


def fetch_db():
    run("""mysqldump --databases inopia_mlfw -u%s -p"%s" \
        --ignore-table=inopia_mlfw.viewer_accesslog > ~/dump.sql"""
        % (env.mysql_user, env.mysql_pass))
    run("""tar czfP ~/dump.sql.tar.gz ~/dump.sql""")
    try:

        local("""rm ~/dump.sql ~/dump.sql.tar.gz""")
    except:
        pass
    get("~/dump.sql.tar.gz", "~/")
    local("""tar xzfP ~/dump.sql.tar.gz""")
    local("""mysql -u%s -p"%s" inopia_mlfw < ~/dump.sql"""
          % (env.mysql_user, env.mysql_pass))


def fetch_media(days=None):
    if not days:
        run("""tar czfP ~/fetch_media.tar.gz ~/webapps/mlfw_media/""")
    else:
        run("""tar czfPN '%d days ago' \
                ~/fetch_media.tar.gz ~/webapps/mlfw_media/""" % int(days))

    try:
        local("""rm ~/webapps/mlfw_media/ ~/fetch_media.tar.gz -rf""")
    except:
        pass

    get("""~/fetch_media.tar.gz""", """~/""")
    local("""tar xzfP ~/fetch_media.tar.gz""")


def _prepare_deploy():
    """
    Collects all files needed for service and puts them to /tmp/.
    """
    if not os.path.exists("/tmp/mlfw_deploy/"):
        os.mkdir("/tmp/mlfw_deploy/")
    os.chdir("/tmp/mlfw_deploy/")

    # Database
    if env.install_db:
        mysqlp = (env.mysql_user, env.mysql_user, env.mysql_pass)
        cmd = """mysqldump --databases %s -u%s -p"%s" \
            --ignore-table=inopia_mlfw.viewer_accesslog > dump.sql""" % mysqlp
        local(cmd)

        cmd = "tar czf dump.sql.tar.gz dump.sql"
        local(cmd)

    # media
    if env.install_media:
        os.chdir(env.home)
        relative_dir = env.mediadir.lstrip(env.home)
        #cmd = """tar czf media.tar.gz %s""" % relative_dir
        #local(cmd)
        #local("mv media.tar.gz /tmp/mlfw_deploy/")

    # static
    if env.install_static:
        os.chdir(env.home)
        css = ""
        #css = "var collated_stylesheets = '"

        cssdir = env.staticdir + "css/"
        for filu in os.listdir(cssdir):
            if filu.endswith(".css") and filu != "responsive.css":
                local(env.minifier + " " + cssdir + filu + " " + cssdir + filu)
        #        with open(cssdir + filu) as cssfilu:
        #            css += cssfilu.read()

        #css += "';"

        lib = ""
        libdir = env.staticdir + "lib/"
        for filu in LIBS:
            with open(libdir + filu) as libfile:
                lib += libfile.read()

        jsdir = env.staticdir + "js/"
        views = ""
        app = ""
        main = ""

        for filu in ("models.js", "utils.js", "main.js"):
            with open(jsdir + filu) as jsfile:
                if filu == "main.js":
                    main += jsfile.read() + "\n"
                else:
                    app += jsfile.read() + "\n"

        for filu in os.listdir(jsdir + "views/"):
            if filu.endswith(".js"):
                with open(jsdir + "views/" + filu) as jsfile:
                    views += jsfile.read() + "\n"

        templatedir = env.staticdir + "mustache/"
        templates = {}
        for template in os.listdir(templatedir):
            if template.endswith(".mustache"):
                with open(templatedir + template, "r") as filu:
                    name = template.partition(".")[0]
                    data = filu.read()
#                    data = strip_spaces_between_tags(filu.read())
                    templates[name] = data

        with open(env.staticdir + "app.js", "w") as out:
            out.write(css + lib + views + app + "tpl.templates = " +
                      json.dumps(templates) + ";\n" + main)
#TODO fix
        local(env.minifier + " " + env.staticdir + "app.js " +
              env.staticdir + "app.js")

        loc = env.staticdeploydir
        local("rm %s* -rf" % loc)
        local("cp %s* %s -r" % (env.staticdir, loc))
        relative_dir = loc.lstrip(env.home)
        cmd = """tar czf static.tar.gz --exclude='*.coffee' \
                --exclude='*.sass' %s""" % relative_dir
        local(cmd)
        local("mv static.tar.gz /tmp/mlfw_deploy/")

    # application
    if env.install_app:
        os.chdir(env.home)
        relative_dir = env.appdir.lstrip(env.home)
        cmd = """tar czf application.tar.gz %s"""

        cmd = cmd % relative_dir
        local(cmd)

        local("mv application.tar.gz /tmp/mlfw_deploy")


def _put():
    """
    Upload stuff to server.
    """
    for filu in env.files:
        if filu.startswith("media"):
            continue
        put("/tmp/mlfw_deploy/%s" % filu, "/home/inopia/")


def _install():
    with cd("/home/inopia/"):

        appdir = env.appdir
        mediadir = env.mediadir
        staticdir = env.staticdeploydir

        run(appdir + "apache2/bin/stop")

        if env.install_app:
            run("rm %smylittlefacewhen/* -rf" % appdir)
        if env.install_media:
            run("rm %s* -rf" % mediadir)
        if env.install_static:
            run("rm %s* -rf" % staticdir)

        for filu in env.files:
            run("tar xzf %s" % filu)

        if env.install_db:
            cmd = """mysql -u%s -p"%s" %s < dump.sql""" % \
                (env.mysql_user, env.mysql_pass, env.mysql_user)
            run(cmd)

        with cd(appdir + "mylittlefacewhen/"):
#            run("python2.7 manage.py migrate viewer")
            with cd("mylittlefacewhen"):
                run("find settings.py -type f -exec sed -i \
                    's/DEBUG = True/DEBUG = False/g' {} ';'")
            with cd("templates"):
                run("find ./ -type f -exec sed -i 's/<!--remove//g' {} ';'")
                run("find ./ -type f -exec sed -i 's/remove-->//g' {} ';'")

        if env.install_static:
            update_cache()

        run(appdir + "apache2/bin/start")

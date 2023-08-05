#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.dbs.basedb import BaseDB
from datafaker.drivers import load_sqlalchemy
from datafaker.utils import save2db


class HiveDB(BaseDB):

    def construct_self_rows(self):
        session = load_sqlalchemy(self.args.connect)
        sql = 'desc %s' % self.args.table
        rows = session.execute(sql)
        return rows

    def save_data(self, lines):
        save2db(lines, self.schema, self.args.table, self.args.connect)
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from datafaker.cli import main

if __name__ == "__main__":

    #
    # cmd = 'datafaker mysql mysql+mysqldb://root:root@localhost:3600/test stu 10'
    # # # cmd = 'datafaker kafka localhost:9092 hello 1 --meta /Users/lovelife/git/github/python/datafaker/datafaker/data/student.text --outprint'
    # # # cmd = 'datafaker file out.txt hello 10 --meta /Users/lovelife/git/github/python/datafaker/datafaker/data/student.text --outprint --outfile output.txt'
    # # # cmd = 'datafaker file out.txt hello 10 --meta /Users/lovelife/git/github/python/datafaker/datafaker/data/student.text --outfile output.txt'
    # # cmd = 'datafaker file . hello.txt 10 --meta data/student.text --outprint --outspliter ## --withheader --format json'
    # # cmd = 'datafaker file . hello.txt 10 --meta data/student.text --format json'
    # # cmd = 'datafaker file . hello.txt 10 --meta data/hive_meta.txt --format text --outprint'
    # cmd = 'datafaker hive hive://yarn@hdfs03-dev.yingzi.com:10000/yz_targetmetric_nuc dws_f_nuc_female_feeding_test 1000 --meta data/hive_meta.txt'
    # # # cmd = 'datafaker hbase localhost:9090 pigtest 2 --meta data/hbase.txt'
    # sys.argv = cmd.strip().split(' ')

    sys.exit(main())


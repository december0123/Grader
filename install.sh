#!/bin/bash

set -x

mkdir ~/.grader
cp -rf Default_config/* ~/.grader/. && chmod 600 ~/.grader/mail_config

#
# See https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

set -x

VENV=.venv
DEPS=python-dependencies.txt
ACTIVATE=".venv/bin/activate"

PYTHON=python
if test -f /usr/bin/python3
then
	PYTHON=python3
fi
echo "USING $PYTHON as python command"

function setupPip() {
	echo "SETTING UP pip"
	$PYTHON -m pip install --upgrade pip
}

function installDeps() {
	echo "INSTALLING DEPENDENCIES"
	$PYTHON -m pip install -r $DEPS
}

function create_venv() {
	echo "CREATING VIRTUAL ENVIRONMENT"
	$PYTHON -m venv .venv
}

function show_command() {
	if test -f .venv/bin/activate
	then
		echo "Now (in bash) run"
		echo source $ACTIVATE
	fi
}

if ! test -f ./bin/activate
then
	create_venv
fi

source $ACTIVATE
setupPip
installDeps
show_command




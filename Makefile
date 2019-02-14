# Note: This is meant for psysh_kernel developer use only
.PHONY: all clean test release

export NAME=`python3 setup.py --name 2>/dev/null`
export VERSION=`python3 setup.py --version 2>/dev/null`

all: clean
	python3 setup.py install

clean:
	rm -rf build
	rm -rf dist

test: clean
	python3 -m pip install jupyter_kernel_test nbconvert
	composer global require psy/psysh:@stable
	python3 -V 2>&1 | grep "Python3 3" && python3 test_psysh_kernel.py || echo "Skipping unit test"
	jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=psysh --ExecutePreprocessor.timeout=60 --stdout psysh_kernel.ipynb > /dev/null;
	make clean

release: test clean
	pip3 install wheel
	python3 setup.py register
	python3 setup.py bdist_wheel --universal
	python3 setup.py sdist
	git commit -a -m "Release $(VERSION)"; true
	git tag v$(VERSION)
	git push origin --all
	git push origin --tags
	twine upload dist/*
	printf '\nUpgrade psysh_kernel-feedstock with release and sha256 sum:'
	shasum -a 256 dist/*.tar.gz

# Note: This is meant for psysh_kernel developer use only
.PHONY: all clean test release

export NAME=`python setup.py --name 2>/dev/null`
export VERSION=`python setup.py --version 2>/dev/null`

all: clean
	python setup.py install

clean:
	rm -rf build
	rm -rf dist

test: clean
	python -m pip install jupyter_kernel_test nbconvert
	composer global require psy/psysh:@stable
	python -V 2>&1 | grep "Python 3" && python test_psysh_kernel.py || echo "Skipping unit test"
	jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=psysh --ExecutePreprocessor.timeout=60 --stdout psysh_kernel.ipynb > /dev/null;
	make clean

release: test clean
	pip install wheel
	python setup.py register
	python setup.py bdist_wheel --universal
	python setup.py sdist
	git commit -a -m "Release $(VERSION)"; true
	git tag v$(VERSION)
	git push origin --all
	git push origin --tags
	twine upload dist/*
	printf '\nUpgrade psysh_kernel-feedstock with release and sha256 sum:'
	shasum -a 256 dist/*.tar.gz

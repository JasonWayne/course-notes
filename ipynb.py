import os
import sys
import getopt


def generate_image_list(qiniu_base, image_counts):
	for i in xrange(1, image_counts + 1):
		yield (i, qiniu_base % i)


def create_markdown_cells(image_list):
	markdown_cell_template = """
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "##### %d"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![%d](%s)"
   ]
  },
	"""
	ret = ""
	for image_tuple in image_list:
		seq_no = image_tuple[0]
		url = image_tuple[1]
		ret += markdown_cell_template % (seq_no, seq_no, url)
	return ret


def gen_ipynb_str(cells_str):
	notebook_stub = """
{
 "cells": [
  %s
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}

	"""
	return notebook_stub % cells_str


def output(path, s):
	with open(path, 'w') as f:
		f.write(s)


def gen_info(course, lec_number):
	courses = set(["mlfoundations", "zbml", "dlfornlp", "cs231n"])
	if course not in courses:
		print "Not a valid course name"
		exit(1)

	link = "http://7xqhfk.com1.z0.glb.clouddn.com/%s/lec%02d/%%04d.jpg" % (course, lec_number)
	path = "%s/lec%02d.ipynb" % (course, lec_number)
	return link, path

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Three args: course name, lec number, pdf pages"
		exit(1)

	course, lec_number, image_counts = sys.argv[1:]

	link, path = gen_info(course, int(lec_number))
	qiniu_images = generate_image_list(link, int(image_counts))
	cells = create_markdown_cells(qiniu_images)
	whole_str = gen_ipynb_str(cells)
	if not os.path.isfile(path):
		output(path, whole_str)
	else:
		print "File exists! Not writing file! Check the output path first!"

import os


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



if __name__ == "__main__":
	qiniu_base_link = "http://7xqhfk.com1.z0.glb.clouddn.com/zbml/lec05/%04d.jpg"
	image_counts = 56
	# path = "dlfornlp/lec08.ipynb"
	path = "zbml/lec05-lr.ipynb"
	qiniu_images = generate_image_list(qiniu_base_link, image_counts)
	cells = create_markdown_cells(qiniu_images)
	whole_str = gen_ipynb_str(cells)
	if not os.path.isfile(path):
		output(path, whole_str)
	else:
		print "File exists! Not writing file! Check the output path first!"


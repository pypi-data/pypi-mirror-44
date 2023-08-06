# sixadsml

Package that is used by the SixAds data science department. To know more about sixads,
visit https://sixads.net/.

The github link for this package is https://bitbucket.org/eligijus112/sixadsml/src/master/

Installation

In anaconda prompt type (windows users):

```console
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install SixAdsDS
```

# sixadsml.clean_text

Functions for text preprocesing/summarizing.
A common way to use these functions is to combine them into a pipeline which the input is a list containing strings.

## lemmatize_word
```python
lemmatize_word(string_list, engine=<WordNetLemmatizer>)
```

Lemmatize words using one of the WordNet engines

Parameters
----------
string_list : list
    List which stores strings
engine : WordNetLemmatizer() (default)
    An object from the nltk.stem.wodnet library

Returns
-------
list
    List with the same length as *string_list* where each word in each
    string is lemmatized


## to_str
```python
to_str(string_list)
```

Lemmatize words using one of the WordNet engines

Parameters
----------
string_list : list
    List which stores strings

Returns
-------
list
    List with the same length as *string_list* where every list element
    is converted to a str type object


## rm_short_words
```python
rm_short_words(string_list, lower_bound=1, upper_bound=2)
```

Removes characters that are in the range of *lower_bound* and *upper_bound*

Parameters
----------
string_list : list
    List which stores strings

lower_bound: int
    Integer indicating the lower bound of a character length

upper_bound: int
    Integer indicating the upper bound of a character length

Returns
-------
list
    List with the same length as *string_list* where every character that is
    split by whitespace is removed if it has a length in the range
    [lower_bound, upper_bound]

Examples
--------
>>> string_list = ['python is awesome', 'R is good as well']
>>> rm_short_words(string_list)
>>> rm_short_words(string_list, 4, 5)


## to_single
```python
to_single(string_list)
```

Converts every word in string_list to it's singular form.

Parameters
----------
 string_list : list
    List which stores strings

Returns
-------
 list
    List with the same length as *string_list* where every word is converted
    to singular form

## to_lower
```python
to_lower(string_list)
```

Makes every word in the string_list lowercase

Parameters
----------
 string_list : list
    List which stores strings

Returns
-------
 list
    List with the same length as *string_list* where every word is converted
    to lowercase

## rm_stop_words
```python
rm_stop_words(string_list)
```

Removes stop words using the nltk stopwords module.

Parameters
----------
 string_list : list
    List which stores strings

Returns
-------
 list
    List with the same length as *string_list* where every string is without
    stopwords

## rm_punctuations
```python
rm_punctuations(string_list)
```

Removes punctuations and other special characters from a string list

Parameters
----------
 string_list : list
    List which stores strings

Returns
-------
 list
    List with the same length as *string_list* where every string is without
    punctuations and other special characters

## rm_digits
```python
rm_digits(string_list)
```

Removes digits from a string list

Parameters
----------
 string_list : list
    List which stores strings

Returns
-------
 list
    List with the same length as *string_list* where every string is without
    digits

## stem_words
```python
stem_words(string_list, stemmer=<nltk.stem.snowball.SnowballStemmer object at 0x00000233385321D0>)
```

A function to stemm the words in a given string vector

Parameters
----------
 string_list : list
    List which stores strings

 stemmer : word stemmer from nltk.stem library;
     nltk.stem.SnowballStemmer('english') default

Returns
-------
 list
    List with the same length as *string_list* where every character is stemmed

## clean_ws
```python
clean_ws(string_list)
```

Cleans one or more whitespaces

Parameters
----------
 string_list : list
    List which stores strings

Returns
-------
 list
    List with the same length as *string_list* where every string has only
    one or less whitespace


## build_vocab
```python
build_vocab(string_list, verbose=True)
```

A function that creates a term frequency vocabulary from the text

Parameters
----------
 string_list : list
    List which stores strings
 verbose : boolean; default=True
     Whether to show the timing of the for loop

Returns
-------
vocabulary
    vocabulary that each key is a unique term in the string_list and
    the key value is the number of times a certain term appeared in the
    string

Example
-------
>>> string_list = string_list = ['python is awesome', 'R is awesome as well']
>>> build_vocab(string_list)


# sixadsml.images

Functions to preproces images from the web or a local machine

## img_read_url
```python
img_read_url(url, h=256, w=256, to_grey=False, timeout=2)
```

Returns an image via an url

Parameters
----------
url : string
    url (in a string format)
h: int
    Desired height of the returned image (px)
w: int
    Desired width of the returned image (px)
to_grey: bool
    should the image be returned in greyscale?
timeout: int
    maximum wait time before dropping the request

Returns
-------
numpy.ndarray
    a numpy array width dimensions (h, w, 3) or (h, w, 1) if to_grey=True

## img_read_url_PIL
```python
img_read_url_PIL(url, h=256, w=256, timeout=2)
```

Returns an image via an url (using PIL framework)

Parameters
----------
url : string
    url (in a string format)
h: int
    Desired height of the returned image (px)
w: int
    Desired width of the returned image (px)
timeout: int
    maximum wait time before dropping the request

Returns
-------
PIL.Image.Image
    a PIL image

## img_read
```python
img_read(path, h=256, w=256, to_grey=False)
```

Reads an image from the local machine

Parameters
----------
path : string
    path to image on a local machine
h: int
    Desired height of the returned image (px)
w: int
    Desired width of the returned image (px)
to_grey: bool
    Should the image be returned in greyscale?

Returns
-------
numpy.ndarray
    a numpy array width dimensions (h, w, 3) or (h, w, 1) if to_grey=True

## return_image_hist
```python
return_image_hist(image, no_bins_per_channel=10, normalize=False)
```

Function to get the histogram of the colours in a photo

Parameters
----------
image : numpy ndarray
    A numpy array with the shape (x, y, 3)
no_bins_per_channel: int
    How many bins should a histgoram have for each channel of colors
normalize : bool
    Should the coordinates add up to 1?

Returns
-------
A list of size 3 * no_bins_per_channel representing the distribution
of colors in the image


# sixadsml.utility

Utility functions

## make_connection
```python
make_connection(specs)
```

Creates a connection based on the information in the *specs*. Ussually,
the *specs* dictionary is the output of the *read_yaml* function

Parameters
----------
specs : dictionary
    A dictionary that stores the user, password, host and db keys

Returns
-------
An sql_alchemy connection object

## exec_file
```python
exec_file(file, add_params=None)
```

Executes a file with the .py extension

Parameters
----------
file: string
    path to the python file
add_params:
    additional parameters that are used in the file that is beeing executed

Returns
-------
Whatever output the executable file outputs

## read_yaml
```python
read_yaml(file)
```

Reads a .yml or .yaml file

Parameters
----------
path: string
    path to the .yml or .yaml files

Returns
-------
Dictionary with the .yml or .yaml file contents

## chunks_of_n
```python
chunks_of_n(l, n)
```

Splits a list into n equal sizes

Parameters
----------
l: list

n: int

Returns
    A list of size *n* with the items of *l* splited equaly

## unique
```python
unique(l)
```

A handy function to return unique elements of a list or a numpy array

Parameters
----------
l : list or array

Returns
-------
A list or array containing unique elements of l

# sixadsml.sql_utility

Functions to deal with downloading and writting data to the database

## Get_sql
```python
Get_sql(self, /, *args, **kwargs)
```

Class that deals with downloading data

## Write_sql
```python
Write_sql(self, /, *args, **kwargs)
```

Class that deals with writting data

# sixadsml.embeddings

Class for dealing with word embeddings

## load_from_text
```python
load_from_text(path)
```

Reads the word embeddings from a txt documents and saves it as a dictionary

Parameters
----------
path: string
    path to a txt document containing the word embeddings

Returns
    A dictionary where the key values are individual words and the
    values are the vectors

## tokenize_text
```python
tokenize_text(string_list, max_features, max_len)
```

Creates a tokenizer from a given text list

Parameters
----------
string_list: list
    List containing strings
max_features: int
    The maximum number of unique words that the tokenizer saves in memory
max_len: int
    The length of the vector into which all elements of *string_list* will
    be converted to.

Returns
    A tuple of the tokenized text and the fitted tokenizer for future use.
    The first element of the tuple is an array of shape (len(*string_list*), max_len)

## create_embedding_matrix
```python
create_embedding_matrix(embeddings, tokenizer, max_features, embed_size=300)
```

Function to create the embedding matrix to use in neural networks. This goes
directly to the embedding layer.

Parameters
----------
embeddings: dictionary
    output of load_from_text() function
tokenizer: keras.Tokenizer object
    output of tokenize_text() function
max_features: int
    how many unique tokens to use
embed_size: int
    how many coordinates does the embedding have; default=300

Returns
    A numpy.ndarray of shape (max_features, embed_size)


# merge\_files

A generic, extensible file merger and converter.

## Simple usage

To merge a JSON file into a YAML file, you'd do the following:

    merge-files input.json output.yaml

This would detect the first file as JSON, the second as a YAML and insert the
JSON file into the YAML.

If you wanted to create this as a new file, you could do:

    merge-files input.json input.yaml output.yaml

This would merge the JSON file into the YAML file and merge the result into the
output.yml. This probably isn't what you want, so a warning will be emitted if
the output file does not exist. If you wanted to create a new file, you could
pass the `--create` flag to force overwriting the output, like so:

    merge-files input.json input.yaml --create output.yaml

### The merge pipeline

The merge process is a series of convert and join steps applied one after
another. Each step represents a mergeable thing that is given a list of
options that look like this:

    merge-files --options [--options ...] file1 [--options ...] file2 [...]

Each loader is asked whether they can handle the file given the options passed
in. If they can, they are added to the candidate list for that step. This is
repeated for each step until the final step is reached. At this point, none of
the loaders are aware of the actual data inside the files, only the options
passed in.

Next, each candidate loader is asked if it can merge into the candidate in the
next step. Any incompatible candidates are removed. This is repeated for each
step. If there are any steps where a merge can't be performed, then the merge
fails.

Once the candidates are determined for each step, they are sorted by their
highest compatibility score. Each loader is given the data itself to look at,
and an actual compatibility score is determined.

## Under the hood

In the example of a JSON file, as a `file` it is a sequence of binary digits.
These can be imagined as either an array of 0s and 1s; some `data` or they can
be grouped as a `list` of numbers made of some length of bits. As it's a text
format, it is best grouped into `bytes` of 8 bits and this decoded into an array
of `char`s; a `string`. This string can be broken into a `list` of `string`s,
depending on the line endings used in the string. But a better way to think of
it is as a tree of keys and values of different types; a `json_tree` object.

`merge-files` supports different types of mergeable objects through a series
of `mergeable_format` loaders. Each loader is registered by the

itself, and uses external libraries to read and write the data.

Currently supported files:

* `.env` files
* binary files (concatenates)
* text files (most encodings, concatenates)

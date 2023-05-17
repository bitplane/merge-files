# merge\_files

A generic, extensible file merge and conversion tool.

## Simple usage

To merge changes in an `.env` file into an existing one in a `make` step,
you might do this:

    merge-files setup/default.env .env

This uses sensible defaults and won't overwrite existing values, but
will add new ones into the file.

To merge a json file into a yaml file, maybe this:

    merge-files output.json docker-compose.yaml

By default, only the final step of the merge pipeline is written to. This is
still pretty dangerous and the tool ia quite young, so buyer beware - make
backups, add an extra step on the end, and expect it to change in future.

### The merge pipeline

The pipeline is a series of load and merge steps applied one after another in
a chain. Each step has some `options` followed by a `target`. The combination
of these guides the selection of `merge_method`s that convert and brutalize
your data along its way. The first options are global, and once a non-global
option is spotted, the rest apply to the next target. The next option that
doesn't start with a hyphen (or does but was preceded by `--`) is the next
target.

See `merge-files --help [topic]` to explore the available options and file
formats.

## Under the hood

`format`s are auto-discovered and collected by the `merger`. Each declares
its `options` and one or more `merge_method`s that can receive a given
`format`.

The `merger` filters these by the given options for the stage, and orders
them by compatibility. In the case of 100% compatibility, chains between
formats are treated as a single link.

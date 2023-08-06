# TIDE 🌊 🏖️

From text editor to IDE. Use a yaml config and some script functions to give your text editor...

# super powers 🦸

## So, what is this thing and how is it useful?

Well, it's really just a way to specify a bunch of stuff that a process can do in a repeatable, predictable way. This lends itself to being a cross-platform, cross-editor solution to many common editor plugin features.

So, instead of having a different plugin implementation for each editor, tide allows you to define the configuration and functionality of your plugin once and target different editors with the same configuration.

## I'm listening and can see a few uses for this... so how do I use it?

Well, I'm glad you asked. As it is cross-editor and cross-platform, there isn't much that can be used to bootstrap tide; except a specific environment variable or a specific file. Tide only needs to know the location of your configuration and can work out the rest once instansiated from your editor (or whatever else you are using it for).

- If no environment variable is specified, the path to the config will be in tide path `./tide/defaults/config_location.yaml`. This is the default config location and specifies the path from which to look for your yaml config file. You can replace the value in this file if you like.
- If the environment variable `TIDE_CONFIG_LOCATION` is set, this will override the value specified in the `config_location.yaml` file. This is the most flexible way of working with tide as you can swap in different configurations from the command line a lot easier than changing the yaml file. For example, setting: `export TIDE_CONFIG_LOCATION=/Users/willvk/Source/wilvk/vgdb/plugins/test_go` would specify the config in this location before starting Vim so that once it is started in Vim as part of the config in that location, it would run commands specific to that configuration set.

## That's great, but please stop being so sassy, and could you give me a rundown of how I can implement this please?

.. hmm.. no, or not yet at least.. 

# whatevs.. 💁

TODO: wiki/tutorial

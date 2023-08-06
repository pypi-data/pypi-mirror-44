# About

This is an extension for the official **awsebcli** where the ssh connections are redirected to the internal IP instead of the external one.

# Installation

To install the latest version:

```
pip  install ebdalia
```

# Usage

```
ebdalia ssh <elastic beanstalk environment>
```

## Example

```
ebdalia ssh campaignplatform-production-web
```

In case you want to use a specific profile from your `~/.aws/config` file, you can add it to the arguments:

```
ebdalia ssh --profile <profile from ~/.aws/config> <elastic beanstalk environment>
```

## Example

```
ebdalia ssh --profile campaignplatform-production campaignplatform-production-web
```

# Redirection to the official awsebcli

This script can be used as a replacement for the official cli, all commands different from `ssh` will be redirect to the official `eb` command.

## Example

```
ebdalia list --profile campaignplatform-production
ebdalia health --profile campaignplatform-production campaignplatform-production-web
ebdalia status --profile campaignplatform-production campaignplatform-production-web
```

---

# Build

In case something is updated in the code, the package must be recreated:

```
./build.sh
```

And uploaded to Pypi:

```
twine upload dist/*  ## (password in passpack, search for 'Pypi')
```

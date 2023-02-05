# actionstore-aws

Kubiya action store to manipulate with AWS resources

## Installation

```
faas-cli deploy -f aws.yaml
```

# Local development

1. Pull the Kubiya base template:
```bash
faas-cli template pull https://github.com/kubiyabot/runner-template-python3
```
2. Change relevant code base
3. Publish & Deploy:
```
faas-cli publish -f aws.yaml
faas-cli deploy -f aws.yaml
```
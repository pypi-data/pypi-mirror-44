# VGS Client
[![CircleCI](https://circleci.com/gh/verygoodsecurity/vgs-cli/tree/master.svg?style=svg&circle-token=dff66120c964e4fbf51dcf059b03746910d0449d)](https://circleci.com/gh/verygoodsecurity/vgs-cli/tree/master)

A command line tool that configures routes in VGS vaults
# Requirements
- Python 3
# Installation
To install the latest version enter:
```
pip install vgs-cli
```

# Help
To call help instruction run `vgs --help` or `vgs -h`

# Authentication
All commands provided by vgs-cli require MFA verification. 

To authenticate run `vgs authenticate` command. After that enter dashboard credentials and authenticate in your browser. Then return back to the terminal and continue usage of VGS CLI.

If you come across an error **You need to run `vgs authenticate` because your session has been expired**, please re-authenticate.
You may be asked to allow storing data in your OS password management system (Mac OS X Keychain, Linux Secret Service, Windows Credential Vault).

In order to remove authenticated session type:
```
vgs logout
```

# Commands
## Parameters
| Name                                    | Description                                                                                          | Mandatory                                | Default value                        |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------- | -------------------------------------- |
| `tenant`                                | Tenant identifier of a vault                                                                         | Yes                                    |                                        |
| `environment`                           | VGS environment. Possible values are `sandbox` and `live`. Default is `sandbox`.                     | No                                     | sandbox                                |
## dump-all
This command dumps routes in a readable YAML format to stdout. We recommend redirecting output to a file for convenience.
```
vgs --tenant=tnteipi8liw --environment=sandbox route --dump-all
```
### Recommended way of using the command
```
vgs --tenant=tnteipi8liw --environment=sandbox route --dump-all > tnteipi8liw.yml
```
### Sample output looks like
```yaml
data:
- attributes:
    created_at: '2018-07-17T16:50:37'
    destination_override_endpoint: https://httpbin.verygoodsecurity.io
    entries:
    - classifiers: {}
      config:
        condition: AND
        expression: null
        rules:
        - condition: null
          expression:
            field: PathInfo
            operator: equals
            type: string
            values: [/post]
          rules: null
        - condition: null
          expression:
            field: ContentType
            operator: equals
            type: string
            values: [application/json]
          rules: []
      id: a46b73e5-df5a-4780-bc01-9e19b1aa04bc
      id_selector: null
      operation: REDACT
      operations: null
      phase: REQUEST
      public_token_generator: UUID
      targets: [body]
      token_manager: PERSISTENT
      transformer: JSON_PATH
      transformer_config: [$.secret]
    host_endpoint: (.*)\.verygoodproxy\.com
    id: 6153b3fc-f869-4fdd-824f-5ed6b1e393c5
    port: 443
    protocol: http
    source_endpoint: '*'
    updated_at: '2018-07-17T16:50:50'
  id: 6153b3fc-f869-4fdd-824f-5ed6b1e393c5
  type: rule_chain
- attributes:
    created_at: '2018-07-17T16:53:01'
    destination_override_endpoint: '*'
    entries: []
    host_endpoint: (.*)
    id: d6c86a9f-c85c-4ced-9998-16b050541f84
    port: 443
    protocol: http
    source_endpoint: '*'
    updated_at: '2018-07-17T16:53:01'
  id: d6c86a9f-c85c-4ced-9998-16b050541f84
  type: rule_chain
version: 1
```
## sync-all
This command synchronizes updates to routes back upstream. It takes a YAML document with routes via stdin.
### Important
For this command to work the following conditions should hold
- YAML document should be a result of a previous output from `dump-all`.
- You can only make changes to the entities in the original YAML document, and you must keep ids as is.
```
vgs --tenant=tnteipi8liw --environment=sandbox route --sync-all < tnteipi8liw.yml
```
## create-all
This command creates new routes in a vault. An input YAML document should take the same form as an output of the `dump-all` command.
A typical use case for this command is a migration of routes from a sandbox environment to live
```
vgs --tenant=tnt3lmevlos --environment=live route --create-all < tnteipi8liw.yml
```
## version
Prints current CLI version.
```
vgs version
```
# Typical scenarios
## Migrate routes from a sandbox environment to live
- Sandbox tenant: `tnt_sandbox`
- Live tenant: `tnt_live`

1. Dump routes from a sandbox vault locally

    ```
    vgs --tenant=tnt_sandbox --environment=sandbox route --dump-all > tnt_sandbox.yml
    ```
2. Re-create routes in a live vault

    ```
    vgs --tenant=tnt_live --environment=live route --create-all < tnt_sandbox.yml
    ```
3. Dump new routes from a live environment locally. We recommend to keep them in a separate file

    ```
    vgs --tenant=tnt_live --environment=live route --dump-all > tnt_live.yml
    ```
4. Update migrated routes in `tnt_live.yml`, if needed. Typically you may need to make changes to some upstream configurations that you were using when testing.
5. Sync changes back to tnt_live

    ```
    vgs --tenant=tnt_live --environment=live route --sync-all < tnt_live.yml
    ```
6. Modify upstream hosts for migrated routes to match your live API's. A typical example is switching development environment to production one on live routes after migration.

# Useful links
[Troubleshooting](https://www.verygoodsecurity.com/docs/api/1/cli#troubleshooting)
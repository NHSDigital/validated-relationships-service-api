# Contribution Guidelines

> [!WARNING]
> Some of the documentation and links in this file are specific to the maintainers of this repository and are only available to NHS England staff.

- [Contribution Guidelines](#contribution-guidelines)
    - [Raising an Issue](#raising-an-issue)
    - [Contributing code](#contributing-code)
        - [Merge responsibility](#merge-responsibility)
        - [Branch naming](#branch-naming)
            - [Developers within the NHS](#developers-within-the-nhs)
            - [Developers outside of the NHS](#developers-outside-of-the-nhs)
        - [Commit messages](#commit-messages)
            - [Developers within the NHS](#developers-within-the-nhs-1)
            - [Developers outside of the NHS](#developers-outside-of-the-nhs-1)

## Raising an Issue

If you raise an issue against this repository, please include as much information as possible to reproduce any bugs,
or specific locations in the case of content errors.

## Contributing code

To contribute code, please fork the repository and raise a pull request.

Ideally pull requests should be fairly granular and aim to solve one problem each. It would also be helpful if they
linked to an issue. If the maintainers cannot understand why a pull request was raised, it will be rejected,
so please explain why the changes need to be made (unless it is self-evident).

### Merge responsibility

- It is the responsibility of the reviewer to merge branches they have approved.
- It is the responsibility of the author of the merge to ensure their merge is in a mergeable state.
- It is the responsibility of the maintainers to ensure the merge process is unambiguous and automated where possible.

### Branch naming

#### Developers within the NHS

Branch names should be of the format:

`NPA-nnnn_short_issue_description`
e.g. `NPA-1234_update_readme`

Multiple branches are permitted for the same ticket.

#### Developers outside of the NHS

Branch names should be of the format:

`short_issue_description`

### Commit messages

#### Developers within the NHS

Commit messages should be formatted as follows:

```
APM-NNN Summary of changes

Longer description of changes if explaining rationale is necessary,
limited to 80 columns and spanning as many lines as you need.
```

#### Developers outside of the NHS

Commit messages should be formatted as follows:

```
Summary of changes

Longer description of changes if explaining rationale is necessary,
limited to 80 columns and spanning as many lines as you need.
```

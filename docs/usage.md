# Usage

This is a command line tool only to copy the files.

This was designed to be used in a course where the instructor has a public GitHub repository with examples organized in subfolders. The instructor can then share the command to copy the relevant example for each lesson, without students needing to clone the entire repository.

## One off copying of a single example:

Specify the `--repo` and `--out-folder` flags to copy a specific folder from a GitHub repository to a local folder:

```bash
instructor_examples folder_in_repo_url --repo=https://github.com//somerepository/ --out-folder=./your_local_folder
```
The default of the `--out-folder` flag is the current working directory, so if you want to copy the folder to your current location, you can omit that flag.

## Running a course with a public Repo

Get students to created a `instructor_examples_settings.json` file in the folder where they want the examples copied to, with the following content:

```json
{
    "repo": "GITHUB_REPO_URL",
}
```

Then they can run the following command to copy the examples for each lesson:

```bash
instructor_examples 23-multi-user-rest-api-start
```

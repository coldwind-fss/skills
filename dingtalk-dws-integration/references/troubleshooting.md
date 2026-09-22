# Troubleshooting guide

## Group missing from a selector

First query the groups endpoint and inspect the DWS conversation count, `singleChat` filtering, and pagination flags. If the group is absent from DWS, have the authorized user join the group and confirm that user can open its history and attachments in DingTalk. Refresh the selector after permissions propagate. Do not substitute the web-login user or silently switch DWS profiles.

## Authorization appears to change users

Check the service's actual process `HOME`, `DWS_CONFIG_DIR`, and explicit `DWS_PROFILE`. A hand-run command succeeding under a different user or directory does not validate the systemd runtime. Pin the profile in every command and keep credential directories private.

## `RESOURCE_NOT_FOUND` or `GET_FIELDS_ERROR`

Check, in order: exact profile; user access in the DingTalk client; IDs belonging to the same real target; DWS product/PAT permission; team-space root invocation without a root folder argument; and only then a tested CLI version update. Do not solve a name mismatch by fuzzy-matching another resource.

## Download or attachment failures

Downloads can emit progress text and therefore must not go through a JSON parser. Attachments require prepare, binary PUT, and record create. Verify file size, content type, returned token, and record response at each step.

## Local versus production Python

A broken local virtual environment is a development issue, not evidence that production is broken. Inspect the production service's executable and Python version first. Prefer a side-by-side local environment for tests; do not rebuild or replace a healthy production environment merely to repair local tooling. Capture dependency versions before any intentional production runtime change.

# Using Capsule CRM at RethinkDB

Capsule CRM lets us keep track of our users, including:

  - who each of our users are
  - how they're using RethinkDB
  - how they participate in our community
  - a history of when we've contacted the user
  - what we should do to make the user feel valued and special

...and anything else that helps us quickly understand what a user's position is within our community, and what we can do to get them more involved.
 

### Logging into Capsule: 

To get started, access Capsule here: https://rethinkdb.capsulecrm.com/


## Concepts in Capsule

Before getting started with Capsule, it's important to understand a few core concepts.

### People and organizations
Capsule tracks __people__ and __organizations__ (generically referred to as _parties_).

Multiple people can be part of an organization, but each person can only belong to one organization (usually the person's company or university).

### Custom fields and tags
Besides the basic fields that are tracked by Capsule for people and organizations, __custom fields__ can also be added to track other useful data on users -- for example, we track the shirt size and GitHub ID of each user using a custom field.

People and organizations can be tagged with __tags__ and __DataTags__. DataTags are tags that also add a set of custom fields to a particular party. For example, you could add a DataTag called "RethinkDB speaker" that adds a custom field for the name of their talk.

### Opportunities and cases

We don't use the sales pipeline feature of Capsule yet, but you can define a sales pipeline with a set of __milestones__ that a prospective opportunity would follow. Capsule helps keep everyone informed on the status and progress of a deal, bid, or any other opportunity in the pipeline.

Capsule also lets you track __cases__ for issues that don't relate to a sales pipeline -- for example, a customer support request, a user that needs a T-shirt, or any other event that involves detailed requests, responses, and an order of tasks to follow. Cases are tied to a specific per on or organization.

You can already add __tasks__ to any person or organization on a one-off basis (and assign them to anyone on our team), but cases let you collect a set of tasks and notes in one location. Cases can be based on a particular __track__: a track is a set of sequential tasks (basically, a numbered checklist of tasks) that define a process.

Here's an example: if you want to send David, one of our contributors, a T-shirt to thank him for his hard work, you can go to David's profile, attach a case from the top-right, choose the "Send a T-shirt" track, and assign it to yourself. You'll automatically get a list of tasks that relate to sending that shirt (send an initial email, find the shirt size, write a note, package the shirt, send a follow-up email) with dates in your calendar and dashboard. Cases and tracks make it easy to juggle tasks and share your progress with the rest of the team.

### History and notes

People, organizations, opportunities, and cases all have a history, which tracks relevant notes and emails.

When interacting with a user, it's important to note that event in the history so everyone on the team can instantly tell what the user's relationship with RethinkDB. 

### The Capsule dropbox

The history includes all relevant emails: those emails can be attached by bcc'ing a specific email address when sending an email to a user (or if necessary, simply forwarding the email). That specific email is the __Capsule dropbox__, which you can find by going to _Settings -> Mail Drop Box_.

It's good practice to _always_ bcc the Capsule dropbox when emailing a user. Doing so lets everyone else on the team know what's been communicated to the user.

## Adding a user to capsule

### When should you add a user to capsule? 

_Whenever you have a meaningful interaction with a user._

If a user tweets something relevant (how happy they are with RethinkDB, what they're building with it, a blog post they just wrote, a question that indicates a real use case, etc.), add them to Capsule.

If you meet someone at an event who says they're a user or potential user of RethinkDB, add them to Capsule.

If you get an unsolicited email from a user for a support request, add them to Capsule (and bcc your reply to the Capsule dropbox).


### Some users are automatically added to Capsule

A set of scripts in the `rethinkdb/community` repository on GitHub add the following set of users:

- Users who have signed the CLA
- Users who have submitted a story for Shirts for Stories
- Any user who has opened or commented on an issue on GitHub

These users are added periodically using these scripts. The last date/time the scripts were run is recorded in the GitHub repository.

When users are automatically added to Capsule, if the user already exists it will never overwrite data in existing fields, but will supplement information gathered from a user's GitHub profile.

The _Unreviewed_ and _Imported_ tags are also attached users that are automatically added, as well as a tag that indicates where the user came from (e.g. _Signed CLA_ or _GitHub issues_.)

### Adding a user to Capsule manually

If the user doesn't already exist in Capsule (make sure to search for them by both name and GitHub ID), then you'll have to manually add them.

Make sure all the checklist items mentioned below (_Checklist for reviewing a Capsule user_) are complete before adding them (or add an _Unreviewed_ tag so someone else will complete their profile.)

## Capsule workflow guidelines

### Checklist for reviewing a Capsule user

Before the _Unreviewed_ tag is removed, make sure the following is true for a user's profile:

- The name should be filled and split across the _first name_, _last name_ fields (some scripts dump the entire name in the _first name_ field). If the name is unknown, substitute the GitHub ID for the first name.
- Research the user to fill in and make sure the _job title_ and _organization_ fields are accurate. If these exist, still make sure to research the user and update it accordingly: people often change jobs, and don't update GitHub, or other profiles. If the organization changes, and no other users are a part of it, delete the organization from Capsule unless it has strategic value.
- Make sure the following fields are accurate and up to date (even if they're already filled in):
    * _Email address_: add a work email address or personal email address if available
    * _Website_: add a personal website if relevant
    * _Blog_: add a blog if relevant (and exclusively their blog, as opposed to their personal website)
    * _Twitter_: add their Twitter handle
    * _GitHub_: add their GitHub handle
    * _Skype_: add their Skype handle
    * _Address_: if we've mailed them something in the past, make sure to include their mailing address. Check that the _city_ field is accurate; scripts will automatically place their location in the _city_ field, but their location isn't necessarily just the city.
- Note the _About_ section: this field is sometimes automatically populated from GitHub. Add any relevant information that makes it easy to understand who the person is at a glance, such as:
  * anything they've contributed to the RethinkDB ecosystem (e.g. a community driver, framework)
  * what project they're building with RethinkDB
  * if their job is interesting and relevant to understanding the user better, what they do at their company / organization
  * what their passion is, what side projects they have
  * if they're a VIP, why they are a VIP
  * anything else that would help someone else on our team understand that user at a moment's glance
- If you're just adding the user, or if a significant event is worth noting, add a note in their history. What makes for a good note? Anything that relates to an event and helps build a snapshot of who the user is, and how they relate to our community (e.g. "John wrote a blog post titled 'RethinkDB in ten minutes', located here: http://johnsblog.com/rethinkdb-post".)
- If there's a follow-up task or case that applies to the user, make sure to add it to their profile immediately: don't save it for later.

### Tags used in Capsule

Here's a list of tags we use in Capsule, and what they mean:

- *__system*: System DataTag that is used for one user, also named *__system*. Neither should be changed by a human -- it's used for bookkeeping by our import scripts (e.g. to record the last date of import for a particular set of users.)
- _Blogger_: Users that blog regularly and are good writers, and may be good candidates for a future RethinkDB-related blog post.
- _Contributor_:  Users that contribute to any part of the RethinkDB ecosystem.
- _Gift sent_: DataTag that notes if a gift has been sent to the user. Attaches a custom field for the date that the last gift was sent.
- _GitHub issues_: Users that have opened an issue or commented on an issue on GitHub.
- _Imported_: System tag that notes the set of users automatically imported or updated by a script, rather than a human being. Should be removed once the import process is complete.
- _Job applicant_: Users that have applied for a position on the RethinkDB team in the past.
- _Research_: Notes if someone on our team need needs to add additional information on the user, because minimal information was found in the initial review. If you add the research tag, add either:
  *  a task if it requires a specific follow-up from a person on our team (e.g. "Slava should forward all emails from this user in his inbox."), and assign it to that person.
  *  a note if more research is required, and not specific to a particular person (e.g. "We need to find out the name and organization of this unknown GitHub user.")
- _RethinkDB Team_: Users that are actually on our team.
- _Shirts for stories_: Users that have submitted a story to S4S.
- _Signed CLA_: User that have signed the contributor license agreement, which is a necessary prerequisite before contributing to the core RethinkDB project or documentation.
- _Speaker_: Users that speak at events or meetups regularly, and may be good candidates for a future RethinkDB-related talk.
- _Unreviewed_: Notes if a human being hasn't examined the profile yet. Should be removed once a user has been reviewed (and merged if necessary.)
- _VIP_: Users that requires additional attention, or should be checked in with regularly.
- _vipreview_: Notes users that may be VIPs, but should be reviewed by a human first.

## Open questions about our Capsule process

- Should we add a tag to organizations to ensure that they've been reviewed by hand, since Capsule auto-creates them if they don't exist? (which leads to lots of bad companies)

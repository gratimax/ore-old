# Ore Roadmap

Ore is a web application that will host user-created projects and plugins, along with any
necessary documentation, files, or discussion; as well as provide facilities to review and search
these projects.

It is designed for Sponge plugins in mind and for the Sponge ecosystem; however, it should be
able to be extended for more general use with plugins/mods related to Minecraft in general.

## Vision

While developers are able to host their Sponge-related projects on GitHub, the Sponge Forums, or
their own custom websites, there currently exists no centralized solution that provides the
necessary project-hosting capabilities that these developers, as well as any potential plugin
consumers, require.
The Sponge project also has a unique opportunity to create a plugin-hosting system that iterates
upon previous systems (like DevBukkit), yet is completely free (as in speech) and open for
contributions.

As a "free" system that is open-source, Ore will be able to service developers and consumers and
cater to their needs better than any proprietary system.
Ore will also be able to evolve in order to fit needs and "get better" with time as more plugins
are created and more users of Sponge appear.

Ore's vision comes in two parts.

For the plugin developer, it should maximize productivity and make plugin hosting and community
management less time-intensive processes.
For a developer, the ideal state is working actively on a plugin, not wrestling with managing
aspects related to how a plugin is hosted, used, or understood.

For the server admin, it should make useful plugins easy to find, and make help easy to ask for and
obtain.
It should also enable server admins to 'give back' in terms of feature suggestions or bug reports.

On a grander scale, designing Ore as an extensible system allows for many more opportunities in the
future.

Eventually, Ore can be consumed by some sort of "package manager" to make plugin management easier
for admins.
In the further future, Ore can provide a safe repository for Sponge client mods to be seamlessly
downloaded for eventual end-users, the players.

If Ore's features can apply to domains outside of Minecraft modding, it can be applied as some
sort of hosted or installable service to those domains.

## Essential Conditions

Seeing as how Ore is a completely free project, its primary goals are to satisfy its users.
These users are mostly developers (the primary producers) and server admins (the primary
consumers).

The primary pain points that Sponge plugin developers currently have are to do with hosting
discussion, documentation, and files, as well as distributing their plugins.

Git and services like GitHub (or private ones like GitLab) have already solved the problem of code
hosting and source control.
Build systems, either hosted instances or provided ones like Travis CI provide a good-enough
method for building and testing plugins, not to mention producing artifacts.

The last developer-centric problems are file hosting, documentation, discussion.
File hosting is the problem with the most immediacy; developers need places to store their
artifacts, and Sponge is in the position to provide the necessary resources to do so.
Documentation and discussion are also important problems, but are already solved by systems like
GitHub wikis, GitHub issues, or subtopics on the Sponge forums.
While a centralized place to gather documentation and discuss plugins is desirable, these features
are not as important since they are already solved to a certain extent.

Ore needs to cater to the consumer in the best possible manner.
This means providing search that is more intuitive and productive, providing a method to obtain
or download a plugin, providing ways to "watch" plugins in order to check for updates, and
providing ways to report bugs or ask for features.
Reporting bugs and asking for features are mostly covered by GitHub issues and similar issue
trackers, and so are not as important as search, download, and watching.

In line with previous systems (DevBukkit in particular), Ore needs to provide some way for
moderators to review plugins for safety concerns and malicious intent.
Unfortunately, Minecraft plugins have a higher incidence of malicious intent than software posted
on GitHub or uploaded to Maven Central, requiring some form of review in order to ensure safety.

## Features

To summarize the essential conditions into a required feature list:

- Project hosting (hosting the "identity" of a project, including owner, name, and descirption)
- File hosting (hosting the artifacts of a project
- Search (providing a method to discover and filter projects)
- Project review (by a team of moderators, helped along by source analyzation and collaboration
  tools)

As well as nonessential, but still interesting features:

- Home pages (potentially more customizable ways for developers to show the uniqueness of their
  projects)
- Documentation (sets of pages that are modifiable by project contributors)
- Project discussion (issue tracking, feature requests, reviews, or related forum-like discussion)
- Team collaboration (including organizations, or more granular project-level team management)
- A REST API (exposed over HTTP, documented, and sane to use for those who wish to extend Ore)
- Metrics (for developers to measure demand and success of their projects)

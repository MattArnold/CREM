# CREM
###Convention Resource Event Management

##Purpose

This web app will help a small team of convention organizers schedule a huge number of events for a highly-diverse multi-track convention, such as Penguicon, identifying all resource conflicts.

Penguicon has about 500 events over a single weekend, in about seventeen different tracks, each track with its own organizer.

For years, Penguicon has planned its schedule using two systems, and kept them in sync manually.

In a spreadsheet, we represented rooms as columns, and times as rows, so we can catch conflicts. But that doesn't store the event description, the topics, whether or not it is "just an idea"/"probably happening"/"confirmed", and other important data.

A database allowed us to store and present a schedule with all the details associated with each event. But the databases we have used could not catch conflicts in which two events are scheduled in the same room at the same time, or a presenter in two places at one time, or duplicated events or presenters.

We are creating C.R.E.M. because we need one solution which stores all the data we use, and also alerts us to conflicts.

##Prerequisites

To develop for this project, you will need `node`, `grunt`, and `bower`. Download `node` from `https://nodejs.org/en/download/` and install it.

Then use this on the command line for node package manager (npm) to install bower and grunt: `npm install -g bower grunt-cli`

##Installation

In the project directory, execute `install.sh` or `install.bat` depending on your operating system. This step only needs to be
performed once.

This will do two things. First it will create a Python virtual environment called *venv* and install a version of Python in it.

The second thing will be to run `bower install` which will install a folder `app/static/lib` full of Javascript third-party dependencies.

Avoid committing the two above directories, which are created by this process. Open `CREM/.git/info/include` which determines which files Git will ignore. Paste in this pattern:

```
app/static/lib/
venv/
```

We won't change the contents of third-party dependencies; instead we will only edit `bower.json` which determines which versions of dependencies we will use, managed by Bower.

##Running the Application

Activate virtual environment by executing the Linux command:

    source venv/bin/activate

or the Windows command:

    venv\bin\activate

Start the application with the command:

    python run.py

The application will now appear at [http://localhost:5000](http://localhost:5000).



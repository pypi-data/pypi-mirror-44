.. _beat-editor-development:

=============
 Development
=============

This section is a compilation of notes and advice about how to develop the ``beat.editor`` project, aimed at those less familiar with web development but familiar with Python.

Preparing the package for development
=====================================

The requirements for installing and preparing the ``beat.editor`` package for development are as following:

#. Linux or MacOS
#. Working internet connection
#. Useable Conda setup (see `Bob's documentation on it <https://www.idiap.ch/software/bob/docs/bob/bob/master/install.html>`_)
#. Up-to-date Firefox and Chrome browsers (both need headless support, a relatively recent feature)
#. Docker installed and available to the current user
#. `NodeJS version 9.x & the associated NPM version <http://nodejs.org/>`_.

Installation Steps
------------------

#. Clone the ``beat.editor`` repository: ::

   $ git clone git@gitlab.idiap.ch:beat/beat.editor.git
   $ cd beat.editor

#. Create a generic development Conda environment for the BEAT/Bob ecosystem using `the Bob/BEAT CLI tool <https://www.idiap.ch/software/bob/docs/bob/bob.devtools/master/install.html>`_: ::

   $ conda create -n bdt -c https://www.idiap.ch/software/bob/conda/label/beta -c https://www.idiap.ch/software/bob/conda bob.devtools python=3.6


#. Activate the created environment and use the ``bdt`` command from ``bob.devtools`` to create a Conda environment for the ``beat.editor`` package: ::

   $ conda activate bdt
   $ bdt create -vv beat_editor
   $ conda activate beat_editor

#. For development, we want to generate all our CLI tools in the ``beat.editor`` project folder. Add the line ``dependent-scripts = true`` to ``buildout.cfg`` under the ``[scripts]`` section and use the ``buildout`` command to generate all the package's executables in ``bin/``: ::

   $ buildout

#. In ``bin/`` you should several executables for the project, including a ``beat`` executable that is the entry point to the server. The Python setup is now complete, but the Javascript environment needs to be similarly set up for development work.

#. Go into the root folder for the Javascript and install the dependencies via NPM (this will take a few minutes): ::

   $ cd conda/js
   $ npm install

#. Test the JS to make sure everything is working properly: ::

   $ npm test

#. Assuming the tests pass, you can start the development webpack server: ::

   $ npm start

#. In a separate terminal tab/window, go back to the root of the ``beat.editor`` project and run the web server in development mode using that ``beat`` executable: ::

   $ ./bin/beat editor serve --dev

#. You should now be able to go ``localhost:9101`` in your browser to see the ``beat.editor`` web app, now served by the webpack dev server. This dev server will watch the Javascript/JSX files on disk and rebuild the web app when any of the files change.


Important Concepts
==================

Before developing for ``beat.editor``, you'll need to familiarize yourself with at least the following concepts/tools:

* Flask & RESTful APIs
* JSON
* JSON-schema, v4
* Node.js
* NPM
* HTML
* CSS
* The DOM & browser APIs
* Javascript
* ES6
* JSX
* React
* Redux
* Bootstrap
* D3 & SVG in general
* Flow typings
* Webpack
* Babel
* Karma
* Mocha

Configuring Your Editor
-----------------------

Your editor is probably adequately configured for editing Python code; it won't be properly configured for the JS part of ``beat.editor`` unless you do modern web development.

* Make sure to pick up JS & JSX syntax highlighting for your editor! Make sure your highlighting supports "ES6" (a landmark JS verion released a couple years ago) and "Flow" (the static typing language extension we are using).
* The configuration files for various linters/static analysis tools are found as dotfiles in the root folder for the JS (next to ``package.json``).
* The provided ``.tern-project`` file is configuration for Tern.js, a JS code analysis tool (autocompletion, etc.). If you're using a popular editor, it'll probably have a plugin for Tern.js.
* There's a few diferent linters available for the different code types (JS, HTML, CSS, JSX). I would suggest installing a linting engine that picks up the available linters for you, like "Syntastic" or "ALE" for Vim. If you aren't using a linting engine, here's some additional notes to get linting working:

  - Linting via ESLint should be configured to use the local installation (from ``node_modules/``) - *not* a global installation. This lets ESLint properly find all the plugins on a per-project basis.

  - Linting CSS via Stylelint should be configured similarly to ESLint. Since this linter is relatively new, your linting engine/editor might not pick it up automatically.

* Linting using Flow needs more configuration regardless of how you set up linting. You need to install the ``flow-typed`` package from NPM globally and pull the types for dependencies: ::

  $ npm i -g flow-typed
  $ cd conda/js
  $ flow-typed update

Development Notes
-----------------

- You'll probably want the `React devtools <https://github.com/facebook/react-devtools>`_ and `Redux devtools <https://github.com/zalmoxisus/redux-devtools-extension>`_ browser plugins to sanely debug and inspect React/Redux code.
- You might need to enable/configure sourcemaps in your browser manually.
- The Python server can be run in dev mode (doesn't try to launch a browser tab) via the ``--dev`` flag.
- You'll probably want Webpack's dev server (``npm start``) running in a separate terminal window/tab, as Webpack will automatically rebuild/update your project when files change (served at ``localhost:9101``. However, changes to the webpack config or other configuration files may not be watched. In general, anything under ``conda/js/src/`` should be hot-reloaded, while anything else may not be. If there's issues with the app when running the dev server that you don't expect or don't make sense (especially if the issue came up after a hot reload), try refreshing the page - sometimes the hot reloader doesn't properly handle complex changes (such as state management or async functionality).
- When changing/updating dependencies, you'll want to install/update flow types for them. Run ``flow-typed update`` again whenever you add JS dependencies.
- If you're quickly iterating test code, you can run the testing daemon in a terminal tab/pane with the ``test-start`` npm script. This lets you quickly trigger tests again with ``karma run`` (via a global ``karma-cli`` installation through npm) since it won't have to start up the daemon each time you want to run the tests. It will also rerun tests when the files change (this is configurable). The daemon is a bit buggy, so if you are getting unexpected errors, try restarting it.

JS Project Structure
--------------------

All JS is stored under ``conda/js``. Unless otherwise noted, all future paths given in this section are relative to that one.

* All dependencies are stored in ``node_modules/``.
* All source is stored in ``src/``.
* All ``*.spec.*`` files are test files. They should be next to the file/component they are testing, which has the same name minus the ``.spec`` infix.
* All this source code is pulled together by ``main.jsx``, which is processed by Webpack via the ``webpack.config.js`` config file.
* ``test/`` holds test data and configures and runs the tests.
* There are 3 different folders in ``src/``, ``components/``, ``helpers``, and ``store/``. These three different folders are discussed further below.

components/
***********

``components/`` holds the UX components, written in a mix of HTML & JSX & CSS, and their associated processing code. Non-generic components (components related to a specific editor) are stored in their respective sub-folders, broken up by BEAT entity type:

* ``algorithm/`` holds the Algorithm Editor code.
* ``database/`` holds the Database Editor code.
* ``dataformat/`` holds the Dataformat Editor code.
* ``experiment/`` holds the Experiment Editor code, which also uses code from the toolchain editor.
* ``library/``: holds the Library Editor code.
* ``plotter/``: holds the Plotter Editor code, which is very similar to the Algorithm Editor.
* ``plotterparameter/``: holds the Plotterparameter code.
* ``toolchain/``: holds the Toolchain Editor code, which is by far the most complex module. The "Graphical Editor" files and the "ToolchainConnection" and "ToolchainBlock" hold most of the code concerned with actual SVG drawing/interaction, while the other files hold the processing code and methods to connect the Graphical Editor to the data.

Generic components, such as the components for the list views, navigation (using `react-router v4 <https://reacttraining.com/react-router/web/guides/philosophy>`_, or common sub-components are just stored in ``components/``.

helpers/
********

``helpers/`` holds code used in many different places or generic utility code. The ``helpers/schema/`` subfolder holds the code & schemas for validating BEAT objects via `JSON schema validation <http://json-schema.org/>`_ (BEAT uses Draft-04). There's a schema for each entity type.

To talk to the ``beat.editor`` REST server, one would use the contents in the ``api`` helper file. For BEAT-wide helpers, see the ``beat`` helper.

store/
******

``store/`` holds all the code for the Redux store, including the reducers, actions, and selectors. We use `reselect <https://github.com/reduxjs/reselect>`_ to write memoized composable selectors, in ``selectors.js``.

REST API
--------

How does the webapp operate on the local BEAT prefix? Through the small Python REST API server provided in ``beat/editor/`` in this project. This is a bare-bones REST API server using `Flask <http://flask.pocoo.org/>`_ that exposes the following API on ``localhost:5000``:

* ``/`` or ``/index.html``: Serves the production/distributable version of the webapp.
* ``<plural BEAT entity name>/``: For each type of BEAT object, there is an endpoint for it. This endpoint is the pluralized version of the type - to operate on databases, use ``/databases``, to operate on libraries, use ``/libraries``, etc. Each endpoint accepts the following HTTP verbs:

  - ``GET``: GET requests fetch all the objects of the given type from the prefix.
  - ``POST``: POST requests create an object given the ``obj`` field, the object to create, and the ``copiedObjName`` field, which is an optional field to specify the object being copied.
  - ``PUT``: PUT requests update objects, overwriting the objects in the prefix with the given objects (matched by name).
  - ``DELETE``: DELETE requests delete objects from the prefix.

* ``settings/``: Only accepts GET requests - fetches settings (not currently being used).
* ``environments/``: Only accepts GET requests - fetches the docker environments (can be slow because ``beat.core`` needs to query every docker container).
* ``layout/``: Only accepts POST requests - given the toolchain as the request body, generates a layout for the toolchain using Graphviz's ``dot`` layout algorithm and returns it.

.. automodule:: beat.editor

E2E Testing
-----------

There are selenium tests found in ``conda/js/test/``. These tests are set up to be ran in Firefox in headless mode with the REST server running locally. To run these tests:

* A relatively recent version of Firefox with headless support
* You need the contents of the tutorial's prefix in your local BEAT prefix (find it at ``https://gitlab.idiap.ch/beat/beat.tutorial.prefix``)
* A recent version of `the Geckodriver executable <https://github.com/mozilla/geckodriver/releases/>`_ available in your path for Selenium to use
* The ``beat.editor`` REST server running locally

Just do ``node conda/js/test/<selenium test>`` to run the test. Please see inside the tests for additional notes.

The tests should always be cleaning up test artifacts in your prefix after the test finishes. If tests do not finish successfully, some of these artifacts may still be present in your prefix and will cause future runs of that test to fail. So, if a test doesn't finish successfully, you will have to delete the test artifacts manually. To make it easier, all BEAT objects created by these tests have the username "selenium" so you know what to delete.

Developing E2E Tests
********************

The webdriver & all its functionality is `well documented <http://seleniumhq.github.io/selenium/docs/api/javascript/module/selenium-webdriver/>`_.

It's recommended to debug tests by not using headless mode and inserting plenty of long pauses via ``driver.sleep()``. You'll need to know the modern ``async``/``await`` pattern as well as be comfortable with CSS selector syntax. See the ``selenium_tutorial_test.js`` test file for working examples of these concepts and how to use selenium's API.

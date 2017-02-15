# django-bare-bones
Start up configuration for Django based projects.

The projects is configured to use [Vagrant](https://www.vagrantup.com/) for local development and [fabric](http://www.fabfile.org/) for deployment. The project also has some default templates based on [Foundation](http://foundation.zurb.com/) and it uses [RequireJS](http://www.requirejs.org/) for JavaScript loading and optimisation.

# Release 0.2.5
* flake8 pre-commit hook added to git during provisioning

# Release 0.2.4
* Removed Modernizr
* Cleaned up Foundation dependencies
* Added comments to set up scss for Foundation and FontAwesome

# Release 0.2.3
* Added more default Python requirements

# Release 0.2.2
* Fixed ansible deprecation issues
* Fixed issues setting postgres authentication

# Release 0.2.1
* Added missing reference to requirejs script from the base template
* Removed references to wagtail/wagtailbase

# Release 0.2
* Updated requirejs configuration to work with babeljs
* Updated the fabric script to work with git
* Added CI configuration files for tox and travis

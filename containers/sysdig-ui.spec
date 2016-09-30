# https://github.com/draios/flame-ui

%define debug_package %{nil}
#
# automatically generate requires and provides from package.json
#
%{?nodejs_find_provides_and_requires}

#
# filter out any false provides created due to dependencies with native components
#
%{?nodejs_default_filter}

#
# name of zip file containing source without .zip extension
#
%define modname myapp

Summary: A nodejs app with a systemd daemon
Name:    nodejs-%{modname}
Group:   Applications/Tools
Version: 0.1
Release: 1
License: Unlicense
URL:     https://github.com/myuser/myapp
Source0: %{modname}-%{version}.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
ExclusiveArch: %{nodejs_arches} noarch
BuildRequires: nodejs-packaging
BuildRequires: systemd

%description
A nodejs app that installs as a systemd service

%prep
%setup -q -n %{modname}-%{version}

%build

%{__rm} -f .gitignore
#
# Fedora guidlines do not allow bundled modules
# use nodejs_symlink_deps in the install section to generate
# links based on package.json contents
#
%{__rm} -rf node_modules

%install
rm -rf $RPM_BUILD_ROOT

#
# copy in the module source
#
%{__install} -d  $RPM_BUILD_ROOT%{nodejs_sitelib}
%{__cp} -r $RPM_BUILD_DIR/%{modname}-%{version} $RPM_BUILD_ROOT%{nodejs_sitelib}/%{modname}
#
# link the daemon binaries into sbindir
#
%{__install} -d  $RPM_BUILD_ROOT%{_sbindir}
%{__ln_s} %{nodejs_sitelib}/%{modname}/bin/myappd $RPM_BUILD_ROOT%{_sbindir}/myappd

#
# link in any dependent nodejs modules referenced in package.json
#
%nodejs_symlink_deps

#
# documents will be handled by %doc, so remove them from buildroot
#
%{__rm} -rf $RPM_BUILD_ROOT%{nodejs_sitelib}/%{modname}{CHANGELOG.md,LICENSE.md,README.md,docs}

#
# Create a systemd unit file
#
cat << __EOF > $RPM_BUILD_ROOT%{_unitdir}/myappd.service
[Unit]
Description=MyApp provides the best API
Documentation=man:myapp.service(8)

[Service]
Type=simple
ExecStart=/usr/sbin/myappd

[Install]
WantedBy=multi-user.target
__EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGELOG.md LICENSE.md README.md docs
%{nodejs_sitelib}/%{modname}
%{_sbindir}/myappd
%{_unitdir}/myappd.service

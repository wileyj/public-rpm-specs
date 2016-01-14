%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-opts
Version:    1.2.2
Release:    3.%{dist}
Summary:    Javascript Command Line Options for Node.js
License:    BSD
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        http://joey.mazzarelli.com/2010/04/09/javascript-command-line-options-for-node-js/
Source0:    http://registry.npmjs.org/opts/-/opts-1.2.2.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel


Requires:       nodejs


%description
js-opts is a library for parsing command line options in javascript.

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/opts
cp -pr js package.json %{buildroot}%{nodejs_libdir}/opts

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/opts
%doc LICENSE README examples/

%changelog

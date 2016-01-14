%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-fstream-npm
Version:    0.0.6
Release:    3.%{dist}
Summary:    An fstream class for creating npm packages
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/fstream-npm
Source0:    http://registry.npmjs.org/fstream-npm/-/fstream-npm-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel


Requires:       nodejs
Requires:       nodejs-fstream-ignore nodejs-inherits

%description
An fstream class for creating npm packages

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/fstream-npm
cp -pr fstream-npm.js package.json %{buildroot}%{nodejs_libdir}/fstream-npm

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/fstream-npm
%doc README.md example

%changelog

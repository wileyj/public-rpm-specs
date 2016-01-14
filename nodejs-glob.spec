%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-glob
Version:    3.1.9
Release:    3.%{dist}
Summary:    A little globber
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/node-glob
Source0:    http://registry.npmjs.org/glob/-/glob-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

Requires:       nodejs
Requires:       nodejs-minimatch nodejs-graceful-fs nodejs-inherits

%description
This is a glob implementation in JavaScript. It uses the minimatch library
to do its matching.

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/glob
cp -pr glob.js package.json %{buildroot}%{nodejs_libdir}/glob

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/glob
%doc README.md examples

%changelog
